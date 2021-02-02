class Star:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.brightness = 0

    def __repr__(self):
        return 'x:{} - y:{} - r:{} - br:{}\n'.format(self.x, self.y, self.r, self.brightness)
