import asyncpg
import json
from motor.motor_asyncio import AsyncIOMotorClient

class DatabaseConnection:

    def __load_db(self, name_database: str):
        db = ''
        with open('database/config.json', 'r', encoding='utf-8') as file:
            db = json.load(file)
    
        return db[name_database]
    
    async def postgre_db(self):
        return await asyncpg.connect(**self.__load_db('postgre'))
    
    async def mongodb(self):
        db = self.__load_db('mongodb')
        client = AsyncIOMotorClient(db['connection_string'])
        return client[db['database']]