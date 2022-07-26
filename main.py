from email import message
from itertools import count
from random import randrange
from sqlite3.dbapi2 import _SingleParamWindowAggregateClass


class Ship:
    def __init__(self, coords: list) -> None:
        self.coords: list = coords
        self.hit_count = 0

    @property
    def size(self):
        return len(self.coords)
    
    @property
    def status(self):
        if self.hit_count <= 0:
            return "целый"
        elif self.hit_count >= self.size:
            return "умер"
        else:
            return "ранен"


class Field:
    """
        0 - свободное поле
        1 - корабль
        2 - ход мимо 
        3 - ход корабель ранен
        4 - ход корабель убит
    """
    def __init__(self, name) -> None:
        self.name: str = name
        self.N: int = 6
        self.cells: list = self.FieldFactory()
        self.ships: list[Ship]  = []


    #find and return ship or None
    def find_ship(self, x, y):
        for ship in self.ships:
            for coord in ship.coords:
                if (x, y) == coord:
                    return ship
        return None


    def ships_alive(self):
        count = 0
        for ship in self.ships:
            if ship.status != "умер":
                count += 1
        return count


    def cells_available_for_shut(self):
        count = 0
        for cell in self.cells:
            if cell == 0:
                count += 1
        return count


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
        print('x\\y 0   1   2   3   4   5')
        line = ""
        for i in range(self.N):
            line = ' | '.join(map(str, self.cells[i]))
            line = line.replace('1', '■')
            line = line.replace('0', '.')
            print(i, '|', line, '|')
        print('=========================')


    #True если в эту ячейку можно стрелять (0, 1)
    def is_cell_availavle_for_shut(self, x, y) -> bool:
        val = self.cells[x][y]

        return val == 0 or val == 1


    # True if cell and cells around are empty
    def is_cell_availavle_for_ship(self, x, y) -> bool:
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
            if not self.is_cell_availavle_for_ship(x, y):
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


    #в случае выстрела
    #проверяем ячейку
    #ищем корабль
    #меняем статус корабля
    #меняем статус ячейки
    #return status 2, 3, 4 / мимо, ранен, убит
    def Shut(self, x, y):
        status = 0
        if not self.is_cell_availavle_for_shut():
            raise Exception("Ячейка не доступна для выстрела")
        
        ship = self.find_ship(x, y)
        if ship is None:
            status = 2 #мимо
            self.cells[x][y] = 2
        else:
            #попал
            if ship.status == 'умер':
                raise Exception("Корабль уже был убит")
            
            ship.hit_count += 1
            if ship.status == 'ранен':
                status = 3 #мимо
                self.cells[x][y] = 3
            elif ship.status == 'ранен':
                status = 4 #мимо
                self.cells[x][y] = 4
            else:
                raise Exception("Неизвесное состояние корабля")
        return status


#запросить координаты в формате 
def user_input(f: Field):
    user_input = []
    while True:
        user_input = list(map(int, list(input("Ваш ход, укажите координаты поля второго игрока, формат (строка колонка): ").split())))
        if len(user_input) == 2 and all(list(map(lambda x: x in range(f.N), user_input))):
            x, y = user_input[0], user_input[1]
            if f.is_cell_availavle_for_shut(x, y):
                print("Ваш выбор: ", user_input)
                return user_input
            else:
                print("Ячейка уже занята, попробуй еще")
        else:
            print("Ваш ввод не распознан, попробуй еще")


def user_input_auto(f: Field):
    user_input = []
    cells_count = randrange(0, f.cells_available_for_shut())
    for x in range(f.N):
        for y in range(f.N):
            if cells_count > 0:
                if f.is_cell_availavle_for_shut(x, y):
                    cells_count -= 1
            else:
                    return (x, y)


#Игровая логика
#Генерация поля Игрок 1
field_user1 = Field("Игрок 1 - людь")
field_user1.GenerateShipsOnBoard()

#Генерация поля Игрок 2
field_user2 = Field("Игрок 2 - компьютер")
field_user2.GenerateShipsOnBoard()

#Игровой цикл пока есть корабли или свободные для выстрела ячейки

count = 1

field_user1.print_nice()
field_user2.print_nice()

user_input = user_input(field_user1)
field_user2.Shut(user_input[0], user_input[1])



