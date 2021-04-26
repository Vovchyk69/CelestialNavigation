from pymongo import GEOSPHERE, MongoClient
import pymongo
from Models.SkyImage import SkyImage
import time
import asyncio
from StarsDB.StarCatalog import StarCatalog
from dotenv import load_dotenv
import os
import copy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
import sys
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

    # connect = MongoClient(os.getenv("CONNECTION_STRING"))
    # db = connect.Catalog
    # # collection = db.Stars
    # # collection.delete_one({'id':17062})
    # table = db.LT2
    # table.update_one(
    #     {'Nq': 46},
    #     {
    #         '$addToSet': {
    #             'Indexes': 36744
    #         }
    #     })
    # 90 99 16 19 46