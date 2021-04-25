from pymongo import GEOSPHERE, MongoClient
import pymongo
from Models.SkyImage import SkyImage
import time
import asyncio
from StarsDB.StarCatalog import StarCatalog
from dotenv import load_dotenv
import os
import copy


async def process(image):
    sky = SkyImage(image)
    sky.show(image)


def loadToDB():
    """
    Load stars to dataBase and extract stars async
    :return: None
    """
    catalog = StarCatalog(os.getenv("CONNECTION_STRING"), os.getenv("dbName"), os.getenv("collectionName"))
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(catalog.importCsvToDatabaseAsync('Static/hygdata_v3.csv')),
             loop.create_task(process("Static/Images/sky.png"))]

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)

    end = time.time()
    print(f'Finished in {end - start} seconds')

    loop.close()


if __name__ == "__main__":
    load_dotenv()
    #
    # # loadToDB()
    # connection = StarCatalog(os.getenv("CONNECTION_STRING"), os.getenv("dbName"), os.getenv("collectionName"))
    # connection.AddLT()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(connection.findNearStars())
    # loop.close()

    # # Nq 12 - 262

    image = "Static/Images/sky2.png"
    sky = SkyImage(image)
    sky.findNearStar()

    sky.show(image)

    # connect = MongoClient(os.getenv("CONNECTION_STRING"))
    # db = connect.Catalog
    # collection = db.LT1
    # # result = collection.find({'Indexes': {'$all': [53905]}})
    # result = collection.find({'Indexes': {'$all': [53905]}})
    # for item in result:
    #     print(item)

    # it is for adding lookup table
    # connection = StarCatalog(os.getenv("CONNECTION_STRING"), os.getenv("dbName"), os.getenv("collectionName"))
    # connection.AddLT()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(connection.findNearStars())
