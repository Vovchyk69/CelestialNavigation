import time
import motor.motor_asyncio
import pandas as pd
import json
from bson import SON
from pymongo import MongoClient, GEO2D, GEOSPHERE


# a class to work with star database
class StarCatalog:
    def __init__(self, connection, dbName=None, collectionName=None):
        self.dbName = dbName
        self.collectionName = collectionName

        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection)
        self.db = self.client[self.dbName]
        self.collection = self.db[self.collectionName]

    async def importCsvToDatabaseAsync(self, path):
        """
        Import csv file to mongodb database as json
        :param path: Path to csv file
        :return: None
        """
        content = pd.read_csv(path)
        content['location'] = content[['dec', 'ra']].values.tolist()
        content_json = json.loads(content.to_json(orient='records'))
        await self.collection.insert_many(content_json)

    def createIndex(self, field):
        self.collection.create_index([(field, GEO2D)])

    async def findNearStars(self, eps=0.3):
        """
        Searching stars in the vicinity of each star in catalog
        :param eps: vicinity
        :return: None
        """
        start = time.time()
        async for element in self.collection.find():
            query = {'location': SON([("$near", [element['dec'], element['ra']]), ("$maxDistance", eps)])}
            result = self.collection.find(query)

        end = time.time()
        print(f"Time of searching star {end - start} s")
