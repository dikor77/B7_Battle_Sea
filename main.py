import os
from random import randrange


def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')



class Ship:
    def __init__(self, coords: list) -> None:
        self.coords: list = coords
        self.hit_count = 0

    @property
    def size(self):
        return len(self.coords)
    
    #0 - целый
    #1 - ранен
    #2 - умер
    @property
    def status(self):
        if self.hit_count <= 0:
            return 0
        elif self.hit_count >= self.size:
            return 2
        else:
            return 1


class Field:
    """
        0 - свободное поле
        1 - корабль
        2 - ход мимо 
        3 - ход корабель ранен
        4 - ход корабель убит
    """
    def __init__(self, name, type = 'auto') -> None:
        self.name: str = name
        self.N: int = 6
        self.cells: list = self.FieldFactory()
        self.ships: list[Ship]  = []
        self.type = type


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
            if ship.status != 2:  #если статус не умер
                count += 1
        return count


    def cells_available_for_shut(self):
        count = 0
        for x in range(self.N):
            for y in range(self.N):
                if self.is_cell_availavle_for_shut(x, y):
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
            line = line.replace('0', '.')
            line = line.replace('1', '■')
            line = line.replace('2', 'o')
            line = line.replace('3', 'x')
            line = line.replace('4', 'X')
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
    #return status 0, 1, 2 / мимо, ранен, убит
    def Shut(self, x, y):
        status = 0
        if not self.is_cell_availavle_for_shut(x, y):
            raise Exception("Ячейка не доступна для выстрела")
        
        ship = self.find_ship(x, y)
        if ship is None:
            status = 0 #мимо
            self.cells[x][y] = 2
        else:
            #попал
            if ship.status == 2: #умер
                raise Exception("Корабль уже был убит")
            
            ship.hit_count += 1
            if ship.status == 1: #ранен
                status = 1 #мимо
                self.cells[x][y] = 3
            elif ship.status == 2: #умер
                status = 2 #умер
                self.cells[x][y] = 4
                #надо переписать статус всех ячеек корабля на поле
                for a, b in ship.coords:
                    self.cells[a][b] = 4
            else:
                raise Exception("Неизвесное состояние корабля")
        return status


#запросить координаты в формате 
def user_input(f: Field, type):
    if type == 'auto':
        cells_count = randrange(0, f.cells_available_for_shut())
        for x in range(f.N):
            for y in range(f.N):
                if cells_count > 0:
                    if f.is_cell_availavle_for_shut(x, y):
                        cells_count -= 1
                else:
                    if f.is_cell_availavle_for_shut(x, y):
                        return [x, y]
        raise Exception("Ошибка генерации координат")
    else:
        while True:
            ui = list(map(int, list(input("Ваш ход, укажите координаты поля второго игрока, формат (строка колонка): ").split())))
            if len(ui) == 2 and all(list(map(lambda x: x in range(f.N), ui))):
                x, y = ui[0], ui[1]
                if f.is_cell_availavle_for_shut(x, y):
                    print("Ваш выбор: ", ui)
                    return ui
                else:
                    print("Ячейка уже занята, попробуй еще")
            else:
                print("Ваш ввод не распознан, попробуй еще")


status = ["МИМО", "РАНИЛ", "УБИЛ"]


#Игровая логика
#Генерация поля Игрок 1
user_shutter = Field("Игрок 1 - людь", type='human')
user_shutter.GenerateShipsOnBoard()

#Генерация поля Игрок 2
user_target = Field("Игрок 2 - компьютер", type='auto')
user_target.GenerateShipsOnBoard()

step_count = 1

#Игровой цикл пока есть корабли или свободные для выстрела ячейки
while True:
    clear_console()
    msg  = "=========================================\n"
    msg += "==      Начало хода, состояние полей   ==\n"
    msg += "=========================================\n"
    print(msg)
    #рисую поля
    user_shutter.print_nice()
    user_target.print_nice()

    #пишу текущий статус
    msg = f"Номер хода: {step_count}\n"
    msg += "Состояние кораблей: \n"
    msg += f"Выстрел делает {user_shutter.name}"
    print(msg)
    #input("Нажми Enter для продолжения")

    #check user_target has cells
    if user_target.cells_available_for_shut() == 0:
        print("Некуда ходить, видимо ничья")
        break

    #user_shutter shut to user_target
    x, y = user_input(user_target, user_shutter.type)
    print(f"Выстрел в ячейку x={x} y={y}")
    val = user_target.Shut(x, y)
    print(f"{user_shutter.name} выстрел результат: {status[val]}")

    #check user_target has ships
    if user_target.ships_alive() == 0:
        print(f"Игрок: {user_shutter.name} выиграл")
        break

    #рисую поля
    user_shutter.print_nice()
    user_target.print_nice()

    msg  = "=========================================\n"
    msg += "==             Конец хода              ==\n"
    msg += "=========================================\n"

    step_count += 1
    user_shutter, user_target = user_target, user_shutter

#рисую поля
user_shutter.print_nice()
user_target.print_nice()

msg  = "=========================================\n"
msg += "==             Конец игры              ==\n"
msg += "=========================================\n"


