import time
import motor.motor_asyncio
import numpy as np
import pandas as pd
import json
import math
from bson import SON
from pymongo import GEO2D, GEOSPHERE


# a class to work with star database
class StarCatalog:
    def __init__(self, connection, dbName=None, collectionName=None):
        self.dbName = dbName
        self.collectionName = collectionName
        self.client = motor.motor_asyncio.AsyncIOMotorClient(connection)
        self.db = self.client[self.dbName]
        self.collection = self.db[self.collectionName]
        self.LookUpTable = self.db["LT2"]
        self.Nq = 100

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
        self.collection.create_index([(field, GEOSPHERE)])

    async def findNearStars(self, eps=6, mag=130):
        """
        Searching stars in the vicinity of each star in catalog
        @param eps: a vicinity
        @param mag: default magnitude for filter stars
        """
        self.createIndex('location')
        start = time.time()
        filteredStars = self.collection.find({"proper": {'$ne': None}})
        async for star in filteredStars:
            query = {'location': SON(
                [("$near", [star['dec'], star['ra']]), ("$maxDistance", eps)]), "dist": {"$lt": mag},
                "lum": {"$gt": 49}}

            cursor = self.collection.find(query)
            await self.buildHash(cursor, star)

        # print(i)
        # end = time.time()
        # print(f"Time of searching star {end - start} s")

    async def buildHash(self, cursor, star, h=6):
        """
        Build hash which contains information about neighbours stars
        @param star: Initial star
        @param cursor: collection of filtered stars
        @param h: a vicinity of star (default 5 degrees)
        @return: None
        """
        i = 0
        hash = ['0'] * self.Nq
        async for item in cursor:
            i += 1
            distance = self.angularDistance(star['ra'], star['dec'], item['ra'], item['dec'])
            hash[int(distance * self.Nq / h)] = '1'

            self.UpdateLT(int(distance * self.Nq / h), item['id'])

        # print(i)
        # print(sum(map(lambda x: x == '1', hash)))
        print("".join(hash))

    def AddLT(self):
        """
        Creating LookUpTable to mongoDb database for star identification
        @return: None
        """

        for value in range(self.Nq):
            element = {"Nq": value, "Indexes": []}
            self.LookUpTable.insert_one(element)

    def UpdateLT(self, nq, index):
        self.LookUpTable.update_one(
            {'Nq': nq},
            {
                '$addToSet': {
                    'Indexes': index
                }
            })

    @staticmethod
    def angularDistance(ra1, dec1, ra2, dec2):
        """
        Find an angular distance between two stars
        :param ra1: right ascension (longitude) of first star
        :param dec1: declination (latitude) of first star
        :param ra2: right ascension (longitude) of first star
        :param dec2: declination (latitude) of first star
        :return: angular distance in degrees
        """
        distance = math.sin(math.radians(dec1)) * math.sin(math.radians(dec2)) + math.cos(
            math.radians(dec1)) * math.cos(math.radians(dec2)) * math.cos(math.radians(ra1 - ra2))
        return math.degrees(math.acos(round(distance, 8)))

    async def identifyStar(self, hash):
        array = []
        for item in enumerate(hash):
            if item[1] == '1':
                star_from_db = await self.LookUpTable.find_one({'Nq': item[0]})
                array += star_from_db['Indexes']

        index = int(np.bincount(array).argmax())
        # counts = np.bincount(array)
        # tolist = list(counts)
        # tolist.sort(reverse=True)
        # print(tolist)
        # print(np.argmax(counts))
        result = await self.collection.find_one({'id': index})
        print(result)
