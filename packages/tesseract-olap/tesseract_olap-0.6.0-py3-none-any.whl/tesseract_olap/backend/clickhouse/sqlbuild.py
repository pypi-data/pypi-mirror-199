"""ClickHouse SQL generation module.

Comprises all the functions which generate SQL code, through the pypika library.
"""

from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

from pypika import functions as fn
from pypika.dialects import ClickHouseQuery, QueryBuilder
from pypika.enums import Order
from pypika.queries import Selectable, Table
from pypika.terms import Criterion, Field, Function, PyformatParameter

from tesseract_olap.backend import ParamManager
from tesseract_olap.query import (Comparison, DataQuery, HierarchyField,
                                  LogicOperator, MeasureField, MembersQuery,
                                  NumericConstraint, RestrictionAge)
from tesseract_olap.schema import MemberType, models

from .dialect import TopK, ArrayElement


def dataquery_sql(
    query: DataQuery,
) -> Tuple[QueryBuilder, Dict[str, str], List[models.InlineTable]]:
    """Build the query which will retrieve an aggregated dataset from the
    database.

    The construction of this query has three main parts:
    - The Core Query,
        which retrieves the primary keys and data rows needed for later steps
    - The Grouping Query,
        which applies the calculations/aggregations over the data
    - The Enriching Query,
        which retrieves the IDs, labels and extra data for the grouped data

    The returned query is the third, which contains the other two as subqueries.
    """
    pman = ParamManager()
    external_tables: List[models.InlineTable] = []

    def _convert_table(table: Union[models.Table, models.InlineTable], alias: Optional[str]):
        if isinstance(table, models.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            external_tables.append(table)
            return Table(table.name, alias=alias)

    def _get_table(
        table: Union[models.Table, models.InlineTable, None],
        *,
        alias: Optional[str] = None,
    ) -> Table:
        return table_fact if table is None else _convert_table(table, alias)

    locale = query.locale
    table_fact = _convert_table(query.cube.table, "tfact")

    def dataquery_tcore_sql() -> QueryBuilder:
        """
        Build the query which will create the `core_table`, an intermediate query
        which contains all data from the Dimension Tables and the Fact Table the
        cube is associated to.

        This query also retrieves the row for all associated dimensions used in
        drilldowns and cuts, through a LEFT JOIN using the foreign key.
        """
        qb: QueryBuilder = ClickHouseQuery.from_(table_fact)

        def _get_closest_field(field: HierarchyField):
            """Prevents SELECTing fields from table_dim if the column used as
            primary key is the same one being SELECTed, thus avoiding an
            unnecessary LEFT JOIN operation.
            """
            column = field.deepest_level.key_column
            alias = f"lv_{field.deepest_level.alias}"
            table_dim = _get_table(field.table)
            if table_dim is not table_fact and column == field.primary_key:
                return Field(field.foreign_key, alias=alias, table=table_fact)
            return Field(column, alias=alias, table=table_dim)

        select_fields = chain((
            # from the fact table, get the fields which contain the values
            # to aggregate and filter; ensure to not duplicate key_columns
            Field(item.measure.key_column, alias=f"ms_{item.key_alias}", table=table_fact)
            for item in dict(
                (obj.key_alias, obj) for obj in query.fields_quantitative
            ).values()
        ), (
            # from the dimension tables, get the fields which contain the primary
            # key of the lowest level in each hierarchy, whether it's used as a
            # drilldown or as a cut
            _get_closest_field(item) for item in query.fields_qualitative
        ))

        qb = qb.select(*select_fields)

        for field in query.fields_qualitative:
            table = _get_table(field.table)
            if (
                table is table_fact or \
                # if optimized by _get_closest_field()
                field.deepest_level.key_column == field.primary_key
            ):
                continue

            qb = qb.left_join(table)\
                   .on(table_fact.field(field.foreign_key)\
                       == table.field(field.primary_key))

        return qb.as_("tcore")

    def dataquery_tgroup_sql(tcore: QueryBuilder) -> QueryBuilder:
        """
        Builds the query which will perform the grouping by drilldown members, and
        then the aggregation over the resulting groups.
        """
        qb: QueryBuilder = ClickHouseQuery.from_(tcore)

        select_fields = chain(
            # Apply aggregations over quantitative fields to get measures
            (_get_aggregate(tcore, item) for item in query.fields_quantitative),

            # Pass the representative level columns to later use to enrich
            (Field(f"lv_{field.deepest_level.alias}",
                   alias=f"dd_{field.deepest_level.alias}", table=tcore)
            for field in query.fields_qualitative
            if field.is_drilldown),
        )
        qb = qb.select(*select_fields)

        # Use the representative levels, so the data gets aggregated
        groupby_fields = (
            tcore.field(f"lv_{field.deepest_level.alias}")
            for field in query.fields_qualitative
            if field.is_drilldown
        )
        qb = qb.groupby(*groupby_fields)

        for field in query.fields_qualitative:
            for item in field.columns:
                # transform the member keys to their MemberType set by the user
                caster = item.level.key_type.get_caster()
                # apply cuts' include/exclude restrictions
                if len(item.members_include) > 0:
                    members = sorted(caster(mem) for mem in item.members_include)
                    qb = qb.where(
                        tcore.field(f"lv_{item.alias}").isin(members)
                    )
                if len(item.members_exclude) > 0:
                    members = sorted(caster(mem) for mem in item.members_exclude)
                    qb = qb.where(
                        tcore.field(f"lv_{item.alias}").notin(members)
                    )
                # apply arbitrary time restrictions
                if item.time_restriction is not None:
                    # this is equivalent to having a cut set on this level,
                    # for the members that match the time scale
                    table_time = _get_table(field.table, alias=f"ttime_{item.alias}")
                    order = Order.asc \
                            if item.time_restriction.age == RestrictionAge.OLDEST else \
                            Order.desc

                    # we intend to create a subquery on the fact table for all
                    # possible members of the relevant level/timescale, using
                    # distinct unify, and get the first in the defined order
                    # which translates into latest/oldest
                    # TODO: use EXPLAIN to see if DISTINCT improves or worsens the query
                    qb_time: QueryBuilder = ClickHouseQuery.from_(table_fact)\
                                                           .distinct()\
                                                           .limit(1)
                    if table_time is table_fact:
                        # Hierarchy is defined in the fact table -> direct query
                        qb_time = qb_time\
                            .select(table_fact.field(item.key_column))\
                            .orderby(table_fact.field(item.key_column), order=order)
                    else:
                        # Hierarchy lives in its own dimension table -> innerjoin
                        qb_time = qb_time\
                            .select(table_time.field(item.key_column))\
                            .inner_join(table_time).on(
                                table_fact.field(field.foreign_key)\
                                == table_time.field(field.primary_key)
                            )\
                            .orderby(table_time.field(item.key_column), order=order)
                    # apply the time restriction cut
                    qb = qb.where(
                        tcore.field(f"lv_{item.alias}").isin(qb_time)
                    )

        return qb.as_("tgroup")

    def dataquery_tdata_sql(tgroup: QueryBuilder) -> QueryBuilder:
        """
        Enriches the table to final outcome, using the primary keys of the associated
        dimensions to get the relevant columns.
        """
        qb: QueryBuilder = ClickHouseQuery.from_(tgroup)

        # Default sorting directions
        # The results are sorted by the ID column of each drilldown
        order = Order.asc
        orderby = (
            tgroup.field(f"dd_{field.deepest_level.alias}")
            for field in query.fields_qualitative
            if field.is_drilldown
        )
        # Flag to know an user-defined sorting field hasn't been set
        sort_field = None

        # Select Measure columns from tgroup
        measure_fields = (
            Field(f"ag_{item.alias}", alias=item.measure.name, table=tgroup)
            for item in query.fields_quantitative
        )
        qb = qb.select(*measure_fields).distinct()

        # Apply user-defined filters on aggregated data
        for field in query.fields_quantitative:
            # skip field if no filter is defined
            if not field.constraint1:
                continue

            # create criterion for first constraint
            column = Field(f"ag_{field.alias}", table=tgroup)
            criterion = _get_filter_criterion(column, field.constraint1)
            # add second constraint to criterion if defined
            if field.constraint2:
                criterion2 = _get_filter_criterion(column, field.constraint2)
                if field.joint == LogicOperator.AND:
                    criterion &= criterion2
                elif field.joint == LogicOperator.OR:
                    criterion |= criterion2
            qb = qb.where(criterion)

        # Apply enrichment LEFT JOIN for drilldown labels
        for field in query.fields_qualitative:
            # skip field if is not a drilldown
            if not field.is_drilldown:
                continue

            # enrichment LEFT JOIN is done against a DISTINCT,
            # column-specified subquery to reduce memory usage
            field_columns = tuple(_yield_drilldown_columns(field, locale))

            # don't do LEFT JOIN if this field only requests the column for its PK
            if len(field_columns) == 1 and (
                field_columns[0][0] == field.deepest_level.key_column and
                field_columns[0][1] == field.deepest_level.name
            ):
                column, alias = field_columns[0]
                qb = qb.select(
                    Field(f"dd_{field.deepest_level.alias}", alias=alias, table=tgroup)
                )

            # do LEFT JOIN with dim_table if this field is requesting properties,
            # parents, or the level has a name_column defined
            else:
                table_target = _get_table(field.table)
                fields_left = (table_target.field(item) for item, _ in field_columns)
                table_left: QueryBuilder = \
                    ClickHouseQuery.from_(table_target)\
                                   .select(*fields_left)\
                                   .distinct()
                # replace fact_table with subquery
                table_enrich = table_left

                # compose the pypika.Field list for each drilldown, drilldown ID & propty
                drilldown_fields = (Field(column, alias=alias, table=table_enrich)
                                    for column, alias in field_columns)

                qb = qb.select(*drilldown_fields)\
                       .left_join(table_left).on(
                    tgroup.field(f"dd_{field.deepest_level.alias}")
                    == table_left.field(field.deepest_level.key_column)
                )

                # User-defined sorting directions for Properties
                if sort_field is None and query.sorting:
                    sort_field, sort_order = query.sorting
                    # TODO: this method could still use a drilldown for sorting, check
                    field_finder = (Field(column, table=table_enrich)
                                    for column, alias in field_columns
                                    if alias == sort_field)
                    sort_field = next(field_finder, None)
                    if sort_field is not None:
                        order = Order.asc if sort_order == "asc" else Order.desc
                        orderby = chain((sort_field,), orderby)

        # User-defined sorting directions for Measures
        if sort_field is None and query.sorting:
            sort_field, sort_order = query.sorting
            field_finder = (Field(f"ag_{field.alias}", table=tgroup)
                            for field in query.fields_quantitative
                            if field.name == sort_field)
            sort_field = next(field_finder, None)
            if sort_field is not None:
                order = Order.asc if sort_order == "asc" else Order.desc
                orderby = chain((sort_field,), orderby)

        qb = qb.orderby(*orderby, order=order)

        # apply pagination parameters if values are higher than zero
        pag_limit, pag_offset = query.pagination
        if pag_limit > 0:
            qb = qb.limit(pag_limit)
        if pag_offset > 0:
            qb = qb.offset(pag_offset)

        return qb.as_("tdata")

    table_core = dataquery_tcore_sql()
    table_group = dataquery_tgroup_sql(table_core)
    table_data = dataquery_tdata_sql(table_group)

    return table_data, pman.params, external_tables


def membersquery_sql(
    query: MembersQuery,
) -> Tuple[QueryBuilder, Dict[str, str], List[models.InlineTable]]:
    """Build the query which will list all the members of a Level in a dimension
    table.

    Depending on the filtering parameters set by the user, this list can also
    be limited by pagination, search terms, or members observed in a fact table.
    """
    pman = ParamManager()
    external_tables: List[models.InlineTable] = []

    def _convert_table(table: Union[models.Table, models.InlineTable], alias: Optional[str]):
        if isinstance(table, models.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            external_tables.append(table)
            return Table(table.name, alias=alias)

    locale = query.locale
    field = query.hiefield

    table_fact = _convert_table(query.cube.table, "tfact")

    table_dim = table_fact \
                if field.table is None else \
                _convert_table(field.table, "tdim")

    level_columns = tuple(
        (alias, column_name)
        for column in field.columns
        for alias, column_name in (
            ("ID", column.level.key_column),
            ("Label", column.level.get_name_column(locale)),
        )
        if column_name is not None
    )

    # if the level's primary key doesn't match its hierarchy's primary key
    # the lookup must be done against a subquery
    if field.deepest_level.key_column != field.primary_key:
        fields_left = (column_name for _, column_name in level_columns)
        table_left = ClickHouseQuery.from_(table_dim)\
                                    .select(*fields_left)\
                                    .distinct()
    else:
        table_left = table_dim

    level_fields = tuple(
        Field(column_name, alias=alias, table=table_left)
        for alias, column_name in level_columns
    )

    qb: QueryBuilder = ClickHouseQuery.from_(table_dim)\
                                      .select(*level_fields)\
                                      .distinct()\
                                      .orderby(*level_fields, order=Order.asc)

    pagination = query.pagination
    if pagination.limit > 0:
        qb = qb.limit(pagination.limit)
    if pagination.offset > 0:
        qb = qb.offset(pagination.offset)

    if query.search is not None:
        pname = pman.register(f"%{query.search}%")
        param = PyformatParameter(pname)
        search_criterion = Criterion.any(
            Field(field).ilike(param) # type: ignore
            for lvlfield in query.hiefield.columns
            for field in (
                lvlfield.level.key_column if lvlfield.level.key_type == MemberType.STRING else None,
                lvlfield.level.get_name_column(locale),
            )
            if field is not None
        )
        qb = qb.where(search_criterion)

    return qb, pman.params, external_tables


def _get_aggregate(table: Selectable, item: MeasureField) -> Function:
    """Generates an AggregateFunction instance from a measure, including all its
    parameters, to be used in the SQL query.
    """
    field = table.field(f"ms_{item.key_alias}")
    alias = f"ag_{item.alias}"

    if item.aggregator_type == "Sum":
        return fn.Sum(field, alias=alias)

    elif item.aggregator_type == "Count":
        return fn.Count(field, alias=alias)

    elif item.aggregator_type == "Average":
        return fn.Avg(field, alias=alias)

    elif item.aggregator_type == "Max":
        return fn.Max(field, alias=alias)

    elif item.aggregator_type == "Min":
        return fn.Min(field, alias=alias)

    elif item.aggregator_type == "Mode":
        return ArrayElement(TopK(1, field), 1, alias=alias)

    # elif item.aggregator_type == "BasicGroupedMedian":
    #     return fn.Abs()

    # elif item.aggregator_type == "WeightedSum":
    #     return fn.Abs()

    # elif item.aggregator_type == "WeightedAverage":
    #     return fn.Abs()

    # elif item.aggregator_type == "ReplicateWeightMoe":
    #     return fn.Abs()

    # elif item.aggregator_type == "CalculatedMoe":
    #     return fn.Abs()

    # elif item.aggregator_type == "WeightedAverageMoe":
    #     return fn.Abs()

    raise NameError(
        f"Clickhouse module not prepared to handle aggregation type: "
        f"{item.aggregator_type}"
    )


def _get_filter_criterion(field: Field, constr: NumericConstraint):
    comparison, scalar = constr

    if comparison == Comparison.GT:
        return field.gt(scalar)
    elif comparison == Comparison.GTE:
        return field.gte(scalar)
    elif comparison == Comparison.LT:
        return field.lt(scalar)
    elif comparison == Comparison.LTE:
        return field.lte(scalar)
    elif comparison == Comparison.EQ:
        return field.eq(scalar)
    elif comparison == Comparison.NEQ:
        return field.ne(scalar)

    raise NameError(f"Invalid criterion type: {comparison}")


def _yield_drilldown_columns(field: HierarchyField, locale: str):
    """Generates pairs of (column name, column alias) for all fields related to
    a HierarchyField object.

    This comprises Drilldown Labels and IDs, and its requested Properties.
    """
    for item in field.columns_drilldown:
        name = item.level.name
        key_column = item.level.key_column
        name_column = item.level.get_name_column(locale)
        if name_column is None:
            yield key_column, name
        else:
            yield key_column, f"{name} ID"
            yield name_column, name
        for propty in item.properties:
            propty_column = propty.get_key_column(locale)
            yield propty_column, propty.name
