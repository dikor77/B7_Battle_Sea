import os
import time
from random import randrange

from ship import Ship
from field import Field
from ship_factory import GenerateShipsOnBoard

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')


#запросить координаты в формате 
def user_input(f: Field, type):
    if type == 'auto':
        time.sleep(2)
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
user_shutter = Field("Игрок 1 - людь", type='auto')
GenerateShipsOnBoard(user_shutter)

#Генерация поля Игрок 2
user_target = Field("Игрок 2 - компьютер", type='auto')
GenerateShipsOnBoard(user_target)

step_count = 1

#Игровой цикл пока есть корабли или свободные для выстрела ячейки
while True:
    clear_console()
    msg  = "|=======================================================|\n"
    msg += "| Начало хода, состояние полей                          |\n"
    msg += "| . - неоткрытое поле, пустое или там спрятался корабль |\n"
    msg += "| ■ - корабль                                           |\n"
    msg += "| o - ход мимо                                          |\n"
    msg += "| x - корабль ранен                                     |\n"
    msg += "| X - корабль Убит                                      |\n"
    msg += "|=======================================================|\n"
    print(msg)
    #рисую поля
    user_shutter.print_nice()
    user_target.print_nice()

    #пишу текущий статус
    msg = f"Номер хода: {step_count}\n"
    msg += "Состояние кораблей: \n"
    msg += f"     У {user_shutter.name} осталось {user_shutter.ships_alive()} кораблей\n"
    msg += f"     У {user_target.name} осталось {user_target.ships_alive()} кораблей\n"
    msg += f"Выстрел делает {user_shutter.name}"
    print(msg)

    #check user_target has cells
    if user_target.cells_available_for_shut() == 0:
        print("Некуда ходить, видимо ничья")
        break

    #user_shutter shut to user_target
    x, y = user_input(user_target, user_shutter.type)
    print(f"Выстрел в ячейку x={x} y={y}")
    res = user_target.Shut(x, y)
    print(f"{user_shutter.name} выстрел результат: {status[res]}")

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
    print(msg)

    input("Нажми Enter для продолжения")

    step_count += 1
    if res == 0:
        user_shutter, user_target = user_target, user_shutter

#рисую поля
user_shutter.print_nice()
user_target.print_nice()

msg  = "=========================================\n"
msg += "==             Конец игры              ==\n"
msg += "=========================================\n"
print(msg)


