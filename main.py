from Models.SkyImage import SkyImage
import time
import asyncio
from StarsDB.StarCatalog import StarCatalog
from dotenv import load_dotenv
import os


def loadToDB():
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


async def process(image):
    sky = SkyImage(image)
    sky.show(image)


if __name__ == "__main__":
    load_dotenv()
    # loadToDB()
