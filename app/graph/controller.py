import operator
from functools import reduce

from fastapi import APIRouter

from app.db import Neo4j
from .model import GraphModel

router = APIRouter(
    prefix='/graph',
    tags=['graph']
)


@router.get('/fetch/{user_id}')
async def fetch_graphs(user_id: int = -1):
    if user_id == -1:
        query = "MATCH (graph:GRAPH) SET graph.id=id(graph) return graph"
    else:
        query = f"""
            MATCH (user:USER)<-[r:CREATOR]-(graph:GRAPH) 
            WHERE id(user)={user_id} 
            SET graph.id=id(graph) 
            RETURN graph
        """

    result = Neo4j.query(query)

    return {
        'data': result
    }


@router.post('/create/{user_id}')
async def graph_create(graph: GraphModel, user_id: int):
    query = f"""
        MATCH (n:USER)
        WHERE id(n)={user_id}
        CREATE (g:GRAPH{{name:'{graph.name}',desc:'{graph.description}'}})-[r:CREATOR]->(n)
        SET g.id=id(g)
        return g
    """
    result = Neo4j.query(query)

    return {
        'data': result
    }


@router.delete('/delete/{user_id}/{graph_id}')
async def graph_delete(user_id: int, graph_id: int):
    query = f"""
        MATCH (user:USER)<-[r:CREATOR]-(g:GRAPH)-[r1*]-(n)
        WHERE id(user)={user_id} AND id(g)={graph_id}
        FOREACH (x IN r1 | DELETE x)
        DELETE g, n, r
    """
    result = Neo4j.query(query)

    return {
        'response': 'Graph deleted',
        'data': result
    }


@router.put('/update/{user_id}')
async def graph_update(newGraph: GraphModel, user_id: int):
    if newGraph.id is None:
        return {
            'response': 'GraphID is required'
        }

    query = f"""
        MATCH  (u:USER)<-[r:CREATOR]-(g:GRAPH)
        WHERE id(g)={newGraph.id} AND
            id(u)={user_id}
        SET g.name={newGraph.name},
        g.description={newGraph.description},
        g.id=id(g)
        RETURN g 
    """

    result = Neo4j.query(query)

    return {
        'response': 'Graph updated',
        'data': result
    }


@router.get('/get_graph/{user_id}/{graph_id}')
async def graph_get(user_id: int, graph_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(:NODE)<-[r]-()
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        RETURN r
    """

    result_relations = Neo4j.query(query)
    result_relations = reduce(operator.concat, result_relations)

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(n:NODE)
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        RETURN n
    """

    result_nodes = Neo4j.query(query)
    result_nodes = reduce(operator.concat, result_nodes)

    return {
        'data': {
            "nodes": result_nodes,
            'relations': result_relations
        }
    }
