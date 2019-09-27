class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __str__(self):
        return '{} {}'.format(self.X, self.Y)

    def __repr__(self):
        return str(self)

    def find_dist_sq(self, other):
        x = (self.X - other.X) * (self.X - other.X)
        y = (self.Y - other.Y) * (self.Y - other.Y)
        return x + y
