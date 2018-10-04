from aiHelper import *
from tile import *
import random


class Queue:
    def __init__(self):
        self.queue = list()

    def enqueue(self, data):
        self.queue.insert(0, data)

    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return None

    def size(self):
        return len(self.queue)


class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def find_closest_resource(self, gameMap):
        self.PlayerInfo.Position.visited = False

        q = Queue()
        q.enqueue(self.PlayerInfo.Position)
        while q.size() > 0:
            current = q.dequeue()
            current.visited = True

            if gameMap.get_tile_at(Point(current.x, current.y)) == TileContent.Resource:
                return current

            left = gameMap.get_real_tile_at(Point(current.x - 1, current.y))
            if left is not None and left.Position.visited is False\
                    and Point.Distance(left.Position, self.PlayerInfo.Position) < gameMap.visibleDistance\
                    and left.TileContent != TileContent.Wall:
                q.enqueue(left.Position)

            right = gameMap.get_real_tile_at(Point(current.x + 1, current.y))
            if right is not None and right.Position.visited is False\
                    and Point.Distance(right.Position, self.PlayerInfo.Position) < gameMap.visibleDistance\
                    and right.TileContent != TileContent.Wall:
                q.enqueue(right.Position)

            up = gameMap.get_real_tile_at(Point(current.x, current.y + 1))
            if up is not None and up.Position.visited is False\
                    and Point.Distance(up.Position, self.PlayerInfo.Position) < gameMap.visibleDistance\
                    and up.TileContent != TileContent.Wall:
                q.enqueue(up.Position)

            down = gameMap.get_real_tile_at(Point(current.x, current.y - 1))
            if down is not None and down.Position.visited is False\
                    and Point.Distance(down.Position, self.PlayerInfo.Position) < gameMap.visibleDistance\
                    and down.TileContent != TileContent.Wall:
                q.enqueue(down.Position)

        return None

    def resource_around(self, gameMap, point):
        # Left
        if gameMap.get_tile_at(Point(point.x - 1, point.y)) == TileContent.Resource:
            return Point(-1, 0)

        # Right
        if gameMap.get_tile_at(Point(point.x + 1, point.y)) == TileContent.Resource:
            return Point(1, 0)

        # Up
        if gameMap.get_tile_at(Point(point.x, point.y + 1)) == TileContent.Resource:
            return Point(0, 1)

        # Down
        if gameMap.get_tile_at(Point(point.x, point.y - 1)) == TileContent.Resource:
            return Point(0, -1)

        return None

    def random_move(self):
        if bool(random.getrandbits(1)):
            if bool(random.getrandbits(1)):
                return create_move_action(Point(-1, 0))
            return create_move_action(Point(1, 0))
        if bool(random.getrandbits(1)):
            return create_move_action(Point(0, -1))
        return create_move_action(Point(0, 1))

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        # Full? Run!
        if self.PlayerInfo.CarriedResources == self.PlayerInfo.CarryingCapacity:
            x_distance = self.PlayerInfo.HouseLocation.x - self.PlayerInfo.Position.x
            y_distance = self.PlayerInfo.HouseLocation.y - self.PlayerInfo.Position.y

            if abs(x_distance) > abs(y_distance):
                print("Moving to house in X.")
                if x_distance > 0:
                    return create_move_action(Point(1, 0))
                return create_move_action(Point(-1, 0))

            print("Moving to house in Y.")
            if y_distance > 0:
                return create_move_action(Point(0, 1))
            return create_move_action(Point(0, -1))

        direction = self.resource_around(gameMap, self.PlayerInfo.Position)
        if direction is not None:
            print("Collecting resource.")
            return create_collect_action(direction)

        closest = self.find_closest_resource(gameMap)
        if closest is not None:
            x_distance = closest.x - self.PlayerInfo.Position.x
            y_distance = closest.y - self.PlayerInfo.Position.y

            if abs(x_distance) > abs(y_distance):
                print("Moving to resource in X.")
                if x_distance > 0:
                    return create_move_action(Point(1, 0))
                return create_move_action(Point(-1, 0))

            print("Moving to resource in Y.")
            if y_distance > 0:
                return create_move_action(Point(0, 1))
            return create_move_action(Point(0, -1))

        print("Moving randomly.")
        return self.random_move()

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
