import asyncpg
from os import getenv
from dotenv import load_dotenv

load_dotenv()


async def create_connect():
    return await asyncpg.connect(
        host=getenv('db_host'),
        database=getenv('db_name'),
        user=getenv('db_user'),
        password=getenv('db_password')
    )
