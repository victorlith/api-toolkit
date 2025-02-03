import pymongo
import pytz
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import json
import random
import math
from typing import Optional, Union, Tuple, Any
from database.database_conn import DatabaseConnection

async def find_db_collection(collection_name: str):
    client = DatabaseConnection()
    db = await client.mongodb()
    db_collection = db[collection_name]
    return db_collection

async def buscar_usuario(user_id: int):
    db_collection = await find_db_collection('users')
    data_user = await db_collection.find_one({"user_id": user_id}) 
    return data_user

async def buscar_usuario_v2(user_id: int):
    db_collection = await find_db_collection('users')
    data_user = await db_collection.find_one({"user_id": user_id}, {"_id": 0})
    pipeline = [
            {"$setWindowFields": {"sortBy": {"total_exp": -1}, "output": {"rank": {"$rank": {}}}}},
            {"$match": {"user_id": data_user["user_id"]}}
        ]
    rank = await db_collection.aggregate(pipeline).to_list()
    data_user['rank'] = rank[0]['rank']
    return data_user

async def rank_de_usuarios() -> list:
    db_collection = await find_db_collection('users')
    data_users = await db_collection.find({"total_exp": {"$gt": 0}}, {"_id": 0, "user_name": 1, "level": 1, "total_exp": 1}).sort("total_exp", pymongo.DESCENDING).to_list(length=None)
    return data_users