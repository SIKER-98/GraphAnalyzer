import operator
from functools import reduce

from fastapi import APIRouter

from app.db import Neo4j
from .model import NodeModel

router = APIRouter(
    prefix='/nodes',
    tags=['nodes']
)


@router.get('/get_nodes/{user_id}/{graph_id}')
async def node_get(user_id: int, graph_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(n:NODE)
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        RETURN n
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'data': result
    }


@router.post('/create/{user_id}/{graph_id}')
async def node_create(node: NodeModel, graph_id: int, user_id: int):
    attributes = ""
    for item in node.text_attributes:
        for key, value in item.items():
            attributes += f"{key}:'{value}',"
    for item in node.number_attributes:
        for key, value in item.items():
            attributes += f"{key}:{value},"

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)
        WHERE id(g)={graph_id} AND
            id(u)={user_id}
        CREATE (g)<-[r:AFFILIATION]-(n:NODE{{
            tags:{node.tags},
            {attributes}
            name:'{node.name}'
        }})
        SET n.id=id(n)
        RETURN n
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'response': 'Node Created',
        'data': result
    }


@router.delete('/delete/{user_id}/{graph_id}/{node_id}')
async def node_delete(node_id: int, graph_id: int, user_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-()-[r:RELATION]-(n:NODE)
        WHERE id(n)={node_id} AND
            id(u)={user_id} AND
            id(g)={graph_id}
        DELETE r,n
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'result': 'Node Deleted',
        'data': result
    }


@router.put('/edit/{user_id}/{graph_id}')
async def node_edit(node: NodeModel, graph_id: int, user_id: int):
    attributes = ""
    for item in node.text_attributes:
        for key, value in item.items():
            attributes += f"{key}:'{value}',"
    for item in node.number_attributes:
        for key, value in item.items():
            attributes += f"{key}:{value},"

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(n:NODE)
        WHERE id(n)={node.id} AND
            id(g)={graph_id} AND
            id(u)={user_id}
        SET n = {{}},
            n.id=id(n),
            n.name='{node.name}',
            {attributes}
            n.tags={node.tags}
        RETURN n
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'result': 'Node Updated',
        'data': result
    }


@router.get('/tags/{user_id}/{graph_id}')
async def node_tags(user_id: int, graph_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(n:NODE)
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        WITH n
        UNWIND n.tags as tag
        RETURN COLLECT(DISTINCT tag)
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'data': result
    }


@router.get('/attributes/{user_id}/{graph_id}')
async def node_attributes(user_id: int, graph_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(n:NODE)
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        WITH n
        UNWIND keys(n) as x
        RETURN COLLECT(DISTINCT x)
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'data': result
    }
