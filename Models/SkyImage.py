from matplotlib import pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
import math
import skimage.io
import time
from Models.Star import Star


class SkyImage:
    def __init__(self, image):
        img = skimage.io.imread(image, as_gray=True)

        self.height, self.width = img.shape
        self.stars = self.extractStarsFromImage(img)

        self.convertBrightness()

    def __len__(self):
        return len(self.stars)

    def __getitem__(self, item):
        return self.stars[item]

    @staticmethod
    def extractStarsFromImage(image):
        start_time = time.time()

        stars = blob_dog(image, max_sigma=10, min_sigma=5, threshold=0.1)
        stars[:, 2] *= math.sqrt(2)

        finish_time = time.time()

        print(finish_time - start_time)

        return [Star(star[0], star[1], star[2]) for star in stars]

    def convertBrightness(self):
        stars_max = max(star.r for star in self.stars)

        for star in self.stars:
            star.brightness = float(star.r) / stars_max

    def show(self, image):
        fig, ax = plt.subplots(1, 1)
        for star in self.stars:
            c = plt.Circle((star.y, star.x), star.r + 5, color="red", linewidth=1, fill=False)
            ax.add_patch(c)

        skimage.io.imshow(image)
        skimage.io.show()