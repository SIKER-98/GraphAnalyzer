import operator
from functools import reduce

from fastapi import APIRouter, HTTPException, status

from .model import UserModel
# from app.db import Neo4j
from ..db import Neo4j

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/')
async def user_get():
    query = " MATCH (n:USER) SET n.id=id(n) return n"
    results = Neo4j.query(query)

    users = reduce(operator.concat, results)

    return {
        'data': users
    }


@router.post('/login')
async def user_login(user: UserModel):
    query = f"""
        MATCH (user:USER) 
        WHERE user.email='{user.email}' 
            AND user.password = '{user.password}'
        SET user.id = id(user)
        RETURN user
    """
    # AND user.password = '{get_hashed_password(user.password)}'

    result = Neo4j.query(query)
    return result

    # if not result:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='Incorrect email or password'
    #     )
    #
    # searched = None
    # for x in result[0]:
    #     searched = x
    # hashed_pass = searched['password']

    # print(user)
    #
    # if searched is None or not verify_password(user.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='Incorrect email or password'
    #     )
    #
    # return {
    #     'access_token': create_access_token(searched['email']),
    #     'refresh_token': create_refresh_token(searched['email']),
    #     'username': searched['username'],
    #     'user_id': searched['id']
    # }


@router.post('/register')
async def user_register(user: UserModel):
    query = f"""
        MERGE (user:USER{{email:'{user.email}'}})
        ON CREATE SET user.password='{user.password}',
            user.username='{user.username}'
        RETURN user
    """

    result = Neo4j.query(query)

    return {
        'data': result
    }
