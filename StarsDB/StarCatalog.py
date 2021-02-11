import motor.motor_asyncio
import pandas as pd
import json

from pymongo import MongoClient


class StarCatalog:
    def __init__(self, connection, dbName=None, collectionName=None):
        self.dbName = dbName
        self.collectionName = collectionName

        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection)
        self.db = self.client[self.dbName]
        self.collection = self.db[self.collectionName]

    async def importCsvToDatabase(self, path):
        print('bd')
        content = pd.read_csv(path)
        content_json = json.loads(content.to_json(orient='records'))

        await self.collection.insert_many(content_json)
        print('edn bd')

