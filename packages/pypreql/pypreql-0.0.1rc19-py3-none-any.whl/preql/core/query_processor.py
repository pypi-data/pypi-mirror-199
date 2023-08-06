from collections import defaultdict
from typing import List, Optional, Dict, Tuple, Union, Set

from preql.constants import logger
from preql.core.env_processor import generate_graph
from preql.core.graph_models import ReferenceGraph
from preql.core.hooks import BaseProcessingHook
from preql.core.models import (
    Environment,
    Select,
    CTE,
    Join,
    JoinKey,
    ProcessedQuery,
    QueryDatasource,
    Datasource,
    Concept,
    JoinType,
    BaseJoin,
    merge_ctes,
)
from preql.core.processing.concept_strategies import get_datasource_by_concept_and_grain
from preql.utility import string_to_hash, unique

LOGGER_PREFIX = "[QUERY BUILD]"


def base_join_to_join(base_join: BaseJoin, ctes: List[CTE]) -> Join:
    left_cte = [
        cte
        for cte in ctes
        if (
            cte.source.datasources[0].identifier == base_join.left_datasource.identifier
            or cte.source.identifier == base_join.left_datasource.identifier
        )
    ][0]
    right_cte = [
        cte
        for cte in ctes
        if (
            cte.source.datasources[0].identifier
            == base_join.right_datasource.identifier
            or cte.source.identifier == base_join.right_datasource.identifier
        )
    ][0]

    return Join(
        left_cte=left_cte,
        right_cte=right_cte,
        joinkeys=[JoinKey(concept=concept) for concept in base_join.concepts],
        jointype=base_join.join_type,
    )


def datasource_to_ctes(query_datasource: QueryDatasource) -> List[CTE]:
    int_id = string_to_hash(query_datasource.identifier)
    output = []
    children = []
    if len(query_datasource.datasources) > 1 or any(
        [isinstance(x, QueryDatasource) for x in query_datasource.datasources]
    ):
        source_map = {}
        for datasource in query_datasource.datasources:
            if isinstance(datasource, QueryDatasource):
                sub_datasource = datasource
            else:
                sub_select: Dict[str, Set[Union[Datasource, QueryDatasource]]] = {
                    key: item
                    for key, item in query_datasource.source_map.items()
                    if datasource in item
                }
                sub_select = {
                    **sub_select,
                    **{c.address: {datasource} for c in datasource.concepts},
                }
                concepts = [
                    c for c in datasource.concepts  # if c.address in sub_select.keys()
                ]
                concepts = unique(concepts, "address")
                sub_datasource = QueryDatasource(
                    output_concepts=concepts,
                    input_concepts=concepts,
                    source_map=sub_select,
                    grain=datasource.grain,
                    datasources=[datasource],
                    joins=[],
                )
            sub_cte = datasource_to_ctes(sub_datasource)
            children += sub_cte
            output += sub_cte
            for cte in sub_cte:
                for value in cte.output_columns:
                    source_map[value.address] = cte.name
    else:
        source = query_datasource.datasources[0]
        source_map = {
            concept.address: source.identifier
            for concept in query_datasource.output_concepts
        }
        source_map = {
            **source_map,
            **{
                concept.address: source.identifier
                for concept in query_datasource.input_concepts
            },
        }
    human_id = (
        query_datasource.identifier.replace("<", "").replace(">", "").replace(",", "_")
    )

    cte = CTE(
        name=f"cte_{human_id}_{int_id}",
        source=query_datasource,
        # output columns are what are selected/grouped by
        output_columns=[
            c.with_grain(query_datasource.grain)
            for c in query_datasource.output_concepts
        ],
        source_map=source_map,
        # related columns include all referenced columns, such as filtering
        # related_columns=datasource.concepts,
        joins=[base_join_to_join(join, output) for join in query_datasource.joins],
        related_columns=query_datasource.input_concepts,
        filter_columns=query_datasource.filter_concepts,
        grain=query_datasource.grain,
        group_to_grain=query_datasource.group_required,
        # we restrict parent_ctes to one level
        # as this set is used as the base for rendering the query
        parent_ctes=children,
        condition=query_datasource.condition,
    )
    if cte.grain != query_datasource.grain:
        raise ValueError("Grain was corrupted in CTE generation")
    output.append(cte)
    return output


def get_disconnected_components(
    concept_map: Dict[str, Set[Concept]]
) -> Tuple[int, List]:
    """Find if any of the datasources are not linked"""
    import networkx as nx

    graph = nx.Graph()
    for datasource, concepts in concept_map.items():
        graph.add_node(datasource)
        for concept in concepts:
            graph.add_edge(datasource, concept.address)
    sub_graphs = list(nx.connected_components(graph))
    return len(sub_graphs), sub_graphs


def get_query_datasources(
    environment: Environment, statement: Select, graph: Optional[ReferenceGraph] = None
) -> Tuple[Dict[str, set[Concept]], Dict[str, Union[Datasource, QueryDatasource]]]:
    concept_map: Dict[str, Set[Concept]] = defaultdict(set)
    graph = graph or generate_graph(environment)
    datasource_map: Dict[str, Union[Datasource, QueryDatasource]] = {}
    # if statement.where_clause:
    #     # TODO: figure out right place to group to do predicate pushdown
    #     statement.grain = statement.grain + Grain(components =statement.where_clause.input)
    components = {
        False: unique(
            statement.output_components + statement.grain.components_copy, "address"
        )
    }

    for key, concept_list in components.items():
        # TODO - identify if concept is already available on a datasource, and skip further search
        for concept in concept_list:
            logger.debug(
                f"{LOGGER_PREFIX} Beginning search for {concept.address} at {str(statement.grain)}"
            )
            datasource = get_datasource_by_concept_and_grain(
                concept, statement.grain, environment, graph, whole_grain=key
            )
            logger.debug(
                f"{LOGGER_PREFIX} Finished search for {concept.address} from {datasource.name} "
            )
            if concept not in concept_map[datasource.identifier]:
                concept_map[datasource.identifier].add(concept)
            # add in the rest of our outptu concepts to the map
            for item in datasource.output_concepts:
                concept_map[datasource.identifier].add(item)
            if datasource.identifier in datasource_map:
                # concatenate to add new fields
                datasource_map[datasource.identifier] = (
                    datasource_map[datasource.identifier] + datasource
                )
            else:
                datasource_map[datasource.identifier] = datasource
    disconnected, disco_lists = get_disconnected_components(concept_map)
    # if not all datasources can ultimately be merged
    if disconnected > 1:
        logger.debug(f"{LOGGER_PREFIX} Disconnected nodes found, have {disco_lists}, need to do subgrain search")
        components = {True: statement.output_components + statement.grain.components}
        for key, concept_list in components.items():
            for concept in concept_list:
                datasource = get_datasource_by_concept_and_grain(
                    concept, statement.grain, environment, graph, whole_grain=key
                )

                logger.debug(
                    f"{LOGGER_PREFIX} finished search for {concept.address} at {str(statement.grain)} from {datasource.identifier}"
                )

                if concept not in concept_map[datasource.identifier]:
                    concept_map[datasource.identifier].add(concept)
                if datasource.identifier in datasource_map:
                    # concatenate to add new fields
                    datasource_map[datasource.identifier] = (
                        datasource_map[datasource.identifier] + datasource
                    )
                else:
                    datasource_map[datasource.identifier] = datasource
            # when we have a unified graph, break the execution
            if get_disconnected_components(concept_map) == 1:
                logger.debug(
                    f"{LOGGER_PREFIX} graph is now connected, exiting "
                )
                break
    return concept_map, datasource_map


def process_query(
    environment: Environment,
    statement: Select,
    hooks: Optional[List[BaseProcessingHook]] = None,
) -> ProcessedQuery:
    """Turn the raw query input into an instantiated execution tree."""
    graph = generate_graph(environment)
    concepts, datasources = get_query_datasources(
        environment=environment, graph=graph, statement=statement
    )
    ctes = []
    joins = []
    for datasource in datasources.values():
        if isinstance(datasource, Datasource):
            raise ValueError("Unexpected base datasource")
        ctes += datasource_to_ctes(datasource)
    final_ctes = merge_ctes(ctes)
    base_list: List[CTE] = [cte for cte in final_ctes if cte.grain == statement.grain]
    if base_list:
        base = base_list[0]
    else:
        base_list = sorted(
            [cte for cte in ctes if cte.grain.issubset(statement.grain)],
            key=lambda cte: -len(
                [
                    x
                    for x in cte.output_columns
                    if x.address in [g.address for g in statement.grain.components]
                ]
            ),
        )
        if not base_list:
            cte_grain = [str(cte.grain) for cte in final_ctes]
            raise ValueError(
                f"No eligible output CTEs created for target grain {statement.grain}, have {','.join(cte_grain)}"
            )
        base = base_list[0]
    others: List[CTE] = [cte for cte in final_ctes if cte != base]

    for cte in others:
        # we do the with_grain here to fix an issue
        # where a query with a grain of properties has the components of the grain
        # with the default key grain rather than the grain of the select
        # TODO - evaluate if we can fix this in select definition

        joinkeys = [
            JoinKey(c)
            for c in statement.grain.components
            if c.with_grain(cte.grain) in cte.output_columns
            and c.with_grain(base.grain) in base.output_columns
            and cte.grain.issubset(statement.grain)
        ]
        if joinkeys:
            joins.append(
                Join(
                    left_cte=base,
                    right_cte=cte,
                    joinkeys=joinkeys,
                    jointype=JoinType.LEFT_OUTER,
                )
            )
    return ProcessedQuery(
        order_by=statement.order_by,
        grain=statement.grain,
        limit=statement.limit,
        where_clause=statement.where_clause,
        output_columns=statement.output_components,
        ctes=final_ctes,
        base=base,
        joins=joins,
    )
