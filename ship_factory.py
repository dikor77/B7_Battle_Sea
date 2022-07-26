from random import randrange
from field import Field
from ship import Ship


def ShipFactory(f: Field, size) -> Ship:
    """
    Ship factory, generate random location for f field\n
    size - size of ship 1-3
    """
    ship_coords = []
    if size < 1:
        size = 1
    if size > 3:
        size = 3
    # first point
    x, y = randrange(0, f.N - size + 1), randrange(0, f.N - size + 1)
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


def GenerateShipsOnBoard(f: Field):
    """
    Generate 7 ships:\n
        3 cells ship - 1\n
        2 cells ship - 2\n
        1 cell  ship - 4\n
    """
    def GenAttempt() -> bool:
        count = 0
        ships_cfg = [3, 2, 2, 1, 1, 1, 1]
        # reset field and ships
        f.clear()
        for n in ships_cfg: 
            while not f.AddShip(ShipFactory(f, n)):
                count += 1
                if count > 1000:
                    return False
        return True

    count_attempts = 0
    while not GenAttempt():
        count_attempts += 1
        if count_attempts > 1000:
            raise Exception("Не получилось расставить корабли")
