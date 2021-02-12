class Star:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.brightness = 0
        self.cartesian = []

    def __repr__(self):
        return '\nx:{} - y:{} - r:{} - br:{}'.format(self.x, self.y, self.r, self.brightness)
