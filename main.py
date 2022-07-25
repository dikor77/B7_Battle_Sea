from itertools import count
from random import randrange


class Ship:
    def __init__(self, coords: list) -> None:
        self.coords = coords

    @property
    def size(self):
        return len(self.coords)


class Field:
    """
        0 - свободное поле
        1 - ship
    """
    def __init__(self, name) -> None:
        self.name = name
        self.N = 6
        self.cells = self.FieldFactory()
        self.ships = []

    def FieldFactory(self) -> list:
        return [[0 for _ in range(self.N)] for _ in range(self.N)]

    def print(self):
        print('x\\y 0   1   2   3   4   5')
        for i in range(self.N):
            print(i, ' ', ' | '.join(map(str, self.cells[i])))

    def print_nice(self):
        print('===========================')
        print('=', self.name)
        print('===========================')
        print('x\\y 1   2   3   4   5   6')
        line = ""
        for i in range(self.N):
            line = ' | '.join(map(str, self.cells[i]))
            line = line.replace('1', '■')
            line = line.replace('0', '.')
            print(i + 1, '|', line, '|')
        print('=========================')

    # True if cell and cells around are empty
    def is_cell_empty(self, x, y) -> bool:
        val = self.cells[x][y]
        val += self.cells[max(x - 1, 0)][y]  # left cell
        val += self.cells[min(x + 1, self.N - 1)][y]  # right cell
        val += self.cells[x][max(y - 1, 0)]  # upper cell
        val += self.cells[x][min(y + 1, self.N - 1)]  # bottom cell

        val += self.cells[max(x - 1, 0)][max(y - 1, 0)]  # upper-left cell
        val += self.cells[min(x + 1, self.N - 1)][max(y - 1, 0)]  # upper-right cell
        val += self.cells[max(x - 1, 0)][min(y + 1, self.N - 1)]  # bottom-left cell
        val += self.cells[min(x + 1, self.N - 1)][min(y + 1, self.N - 1)]  # bottom-right cell

        return val == 0

    # Check if can add ship to the field
    # return True if suxessfull
    # return False if location is busy
    def CanAddShip(self, ship: Ship) -> bool:
        for cell in ship.coords:
            x, y = cell[0], cell[1]
            if not self.is_cell_empty(x, y):
                return False
        return True

        # Add ship if coords available

    # return True/False
    def AddShip(self, ship: Ship) -> bool:
        if self.CanAddShip(ship):
            for cell in ship.coords:
                x, y = cell[0], cell[1]
                self.cells[x][y] = 1
            self.ships.append(ship)
            return True
        return False

    # ship factory, generate random location on field
    # size - size of ship 1-3
    def ShipFactory(self, size) -> Ship:
        ship_coords = []
        if size < 1:
            size = 1
        if size > 3:
            size = 3
        # first point
        x, y = randrange(0, self.N - size + 1), randrange(0, self.N - size + 1)
        # select direction
        if randrange(0, 2):
            # horizontal
            for i in range(size):
                ship_coords.append((x + i, y))
        else:
            # vertical
            for i in range(size):
                ship_coords.append((x, y + i))

        ship = Ship(ship_coords)
        return ship


    def GenerateShipsOnBoard(self):
        """Generate 7 ships:
            3 cells ship - 1
            2 cells ship - 2
            1 cell ship - 4
        """
        def GenAttempt() -> bool:
            count = 0
            ships_cfg = [3, 2, 2, 1, 1, 1, 1]
            # reset field and ships
            self.cells = self.FieldFactory()
            self.ships = []
            for n in ships_cfg:
                while not self.AddShip(self.ShipFactory(n)):
                    count += 1
                    if count > 1000:
                        return False
            return True

        count_attempts = 0
        while not GenAttempt():
            count_attempts += 1
            if count_attempts > 1000:
                raise Exception("Не получилось расставить корабли")


field_user = Field("Игрок 1 - людь")
field_user.GenerateShipsOnBoard()

field_ai = Field("Игрок 2 - компьютер")
field_ai.GenerateShipsOnBoard()

# field_user.print()
field_user.print_nice()
field_ai.print_nice()
