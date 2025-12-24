class Position:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return chr(self.x + ord('a') - 1) + str(self.y)