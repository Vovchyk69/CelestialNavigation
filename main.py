import motor
from pymongo import MongoClient

from Models.SkyImage import SkyImage
import time
import asyncio
from StarsDB.StarCatalog import StarCatalog
from dotenv import load_dotenv
import os


async def process():
    print('i am processing image')
    image = "Static/Images/sky.png"
    sky = SkyImage(image)
    print('end processing image')
    sky.show(image)


if __name__ == "__main__":
    load_dotenv()

    catalog = StarCatalog(os.getenv("CONNECTION_STRING"), dbName='Catalog', collectionName='Stars')
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(catalog.importCsvToDatabase('hygdata_v3.csv')), loop.create_task(process())]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)

    end = time.time()
    print(f'Finished in {end - start} seconds')

    loop.close()
