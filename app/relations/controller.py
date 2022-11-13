import operator
from functools import reduce

from fastapi import APIRouter

from app.db import Neo4j
from .model import RelationModel

router = APIRouter(
    prefix='/relations',
    tags=['relations']
)


@router.get('/get_relations/{user_id}/{graph_id}')
async def relation_get(user_id: int, graph_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(:NODE)<-[r]-()
        WHERE id(u)={user_id} AND
            id(g)={graph_id}
        RETURN r
    """

    result = Neo4j.query(query)
    result = reduce(operator.concat, result)

    return {
        'data': result
    }


@router.post('/create/{user_id}/{graph_id}')
async def relation_create(relation: RelationModel, graph_id: int, user_id: int):
    attributes = ""
    for item in relation.attributes:
        for key, value in item.items():
            attributes += f"{key}:'{value}',"

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(start:NODE), 
            (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(end:NODE)
        WHERE id(g)={graph_id} AND
            id(start)={relation.start_node} AND
            id(end)={relation.end_node} AND
            id(u)={user_id}
        CREATE (start)-[r:RELATION{{
            tags:{relation.tags},
            start_node:{relation.start_node},
            end_node:{relation.end_node},
            {attributes}
            name:'{relation.name}'
        }}]->(end)
        SET r.id=id(r)
        RETURN r
    """

    result = Neo4j.query(query)

    return {
        'response': 'Relation Created',
        'data': result
    }


@router.delete('/delete/{user_id}/{graph_id}/{relation_id}')
async def relation_delete(graph_id: int, relation_id: int, user_id: int):
    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(start:NODE)
            -[r:RELATION]
            ->(end:NODE)-[:AFFILIATION]->(g:GRAPH)-[:AFFILIATION]->(u:USER), 
        WHERE id(g)={graph_id} AND
            id(r)={relation_id} AND
            id(u)={user_id}
        DELETE r
    """

    result = Neo4j.query(query)

    return {
        'result': 'Relation Deleted',
        'data': result
    }


# start_node and end_node not required
@router.put('/edit/{user_id}/{graph_id}')
async def relation_edit(relation: RelationModel, graph_id: int, user_id: int):
    attributes = ""
    for item in relation.attributes:
        for key, value in item.items():
            attributes += f"r.{key}='{value}',"

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(:NODE)
        -[r:RELATION]
        ->(:NODE)-[:AFFILIATION]->(g:GRAPH)-[:AFFILIATION]->(u:USER)
        WHERE id(g)={graph_id} AND
            id(r)={relation.id} AND
            id(u)={user_id}
        SET r={{}},
            r.id=id(r),
            r.name='{relation.name}',
            {attributes}
            r.tags={relation.tags}
        RETURN r
    """

    result = Neo4j.query(query)

    return {
        'result': 'Relation Updated',
        'data': result
    }


@router.post('/edit/{user_id}/{graph_id}')
async def relation_redirect(relation: RelationModel, graph_id: int, user_id: int):
    attributes = ""
    for item in relation.attributes:
        for key, value in item.items():
            attributes += f"new_r.{key}='{value}',"

    query = f"""
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(old_start:NODE)
            -[r:RELATION]
            ->(old_end:NODE)-[:AFFILIATION]->(g:GRAPH)-[:AFFILIATION]->(u:USER)
        WHERE id(g)={graph_id} AND
            id(r)={relation.id} AND
            id(u)={user_id}
        WITH r
        
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(new_start:NODE)
        WHERE id(g)={graph_id} AND
            id(new_start)={relation.start_node} AND
            id(u)={user_id}
        WITH r, new_start
        
        MATCH (u:USER)<-[:CREATOR]-(g:GRAPH)<-[:AFFILIATION]-(new_end:NODE)
        WHERE id(g)={graph_id} AND
            id(new_end)={relation.end_node} AND
            id(u)={user_id}
        WITH r, new_start, new_end
        
        CREATE (new_start)-[new_r:RELATION]->(new_end)
        SET new_r=r,
            new_r.id=id(new_r),
            new_r.name='{relation.name}',
            new_r.start_node:{relation.start_node},
            new_r.end_node:{relation.end_node},
            {attributes}
            new_r.tags={relation.tags}  
        WITH r, new_r
        DELETE r
        RETURN new_r
    """

    print(query)
    result = Neo4j.query(query)

    return {
        'result': 'Relation Redirected',
        'data': result
    }
