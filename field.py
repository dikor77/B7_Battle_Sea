from random import randrange

from ship import Ship

class Field:
    """
    Класс Field - игровое поле
    cells - ячейки, список строк, строка - список солонок. [[row1],[row2]]
    Статус ячейки\n
        0 - свободное поле\n
        1 - корабль\n
        2 - ход мимо\n 
        3 - ход корабель ранен\n
        4 - ход корабель убит\n
    """
    def __init__(self, name, type = 'auto') -> None:
        self.name: str = name
        self.N: int = 6
        self.cells: list = self.ffactory()
        self.ships: list[Ship]  = []
        self.type: str = type
        """auto or any"""

    def clear(self):
        self.cells = self.ffactory()
        self.ships = []

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


    def ffactory(self) -> list:
        """Field factory"""
        return [[0 for _ in range(self.N)] for _ in range(self.N)]


    def print(self):
        print('x\\y 0   1   2   3   4   5')
        for i in range(self.N):
            print(i, ' ', ' | '.join(map(str, self.cells[i])))


    def print_nice(self):
        print('===========================')
        print('=', self.name, "режим: ", self.type)
        print('===========================')
        print('x\\y 0   1   2   3   4   5')
        print('===========================')
        line = ""
        for i in range(self.N):
            line = ' | '.join(map(str, self.cells[i]))
            line = line.replace('0', '.')
            line = line.replace('1', '.' if self.type == 'auto' else '■') 
            line = line.replace('2', 'o')
            line = line.replace('3', 'x')
            line = line.replace('4', 'X')
            print(i, '|', line, '|')
        print('===========================')


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
