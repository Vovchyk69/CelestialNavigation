import asyncio
import os

from bson import SON
from matplotlib import pyplot as plt, patches
from pymongo import GEOSPHERE, GEO2D
from skimage.feature import blob_dog, blob_log, blob_doh
import math
import skimage.io
import time
from Models.Star import Star


# a class that extract stars from sky image
from CelestialNavigation.StarsDB.StarCatalog import StarCatalog


class SkyImage:
    def __init__(self, image):
        img = skimage.io.imread(image, as_gray=True)

        self.height, self.width = img.shape
        self.stars = self.extractStarsFromImage(img)
        print(self.height, self.width)
        self.convertToBrightness()
        self.convertToSpherical()
        self.filteredStars = []

    def __len__(self):
        return len(self.stars)

    def __getitem__(self, item):
        return self.stars[item]

    @staticmethod
    def extractStarsFromImage(image):
        """
        Detect stars on image of the night sky
        :param image: Path image
        :return: array of stars
        """
        start_time = time.time()

        stars = blob_log(image, max_sigma=10, min_sigma=3, threshold=0.1)
        stars[:, 2] *= math.sqrt(2)

        finish_time = time.time()
        print(finish_time - start_time)

        return [Star(star[1], star[0], star[2]) for star in stars]

    def convertToBrightness(self):
        """
        Calculates brightness of stars related to the radius of star.
        Brightness can be between 0 and 1
        :return: None
        """
        stars_max = max(star.r for star in self.stars)

        for star in self.stars:
            star.brightness = float(star.r) / stars_max

    def convertToSpherical(self):
        z = 0
        for star in self.stars:
            Q = math.atan2(star.y, star.x)
            alpha = math.atan2(math.sqrt(pow(star.x, 2) + pow(star.y, 2)), z)
            star.cartesian = [Q, alpha]

    def findNearStar(self):
        connection = StarCatalog(os.getenv("CONNECTION_STRING"), os.getenv("dbName"), os.getenv("collectionName"))
        for star in self.stars:
            if star.brightness >= 1:
                self.findStar(star, connection)

    # def buildHash(self, initialStar, h=5.51, eps=5):
    #     """
    #     Build hash which contains information about neighbours stars
    #     @param star: Initial star
    #     @param cursor: collection of filtered stars
    #     @param h: a vicinity of star (default 5 degrees)
    #     @return: None
    #     """
    #     Nq = 100
    #     hash = ['0'] * Nq
    #     i = 0
    #     for star in self.stars:
    #         i += 1
    #         okil = 5 * self.width / h
    #         if math.sqrt(pow((star.x - initialStar.x), 2) + pow((star.y - initialStar.y), 2)) < pow(okil, 2):
    #             distance = math.sqrt(pow((star.x - initialStar.x), 2) + pow((star.y - initialStar.y), 2))
    #             distance = distance / self.width * h
    #
    #         hash[int(distance * Nq / h)] = '1'
    #
    #     # print(i)
    #     # print(sum(map(lambda x: x == '1', hash)))
    #     print("".join(hash))

    def findStar(self, initialStar,connection, eps=43.1, h=5):
        # eps = 43.1 !!!
        hash = ['0'] * 100
        vicinity = self.width / eps * h
        for star in self.stars:
            if pow((star.x - initialStar.x), 2) + pow((star.y - initialStar.y), 2) < pow(vicinity, 2):
                distance = math.sqrt(pow((star.x - initialStar.x), 2) + pow((star.y - initialStar.y), 2))
                distance = distance / self.width * eps
                self.filteredStars.append(star)
                hash[int(distance * 100 / h)] = '1'

        print("".join(hash))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(connection.identifyStar(hash))

    def show(self, image):
        """
        Generates new image with found stars
        :param image: path to image
        :return: None
        """
        fig, ax = plt.subplots(1, 1)
        for star in self.filteredStars:
            if star.brightness >= 0:
                c = patches.Circle((star.x, star.y), star.r + 5, color="red", linewidth=1, fill=False)
                ax.add_patch(c)

        skimage.io.imshow(image)
        skimage.io.show()
