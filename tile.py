from structs import Point
from enum import Enum


class Tile:
    def __init__(self, tile_content, x, y):
        self.TileContent = tile_content
        self.Position = Point(x, y)
        pass

    def __str__(self):
        return "Content: {0}, Position: {1}".format(self.TileContent.name, str(self.Position))


class ResourceTile(Tile):
    def __init__(self, tile_content, x, y, amount_left, density):
        Tile.__init__(self, tile_content, x, y)
        self.AmountLeft = amount_left
        self.Density = density


class TileContent(Enum):
    Empty = 0
    Wall = 1
    House = 2
    Lava = 3
    Resource = 4
    Shop = 5
    Player = 6

    def symbol(self):
        return self.name[0]
