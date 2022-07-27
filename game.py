from random import randint


from player import AI, User
from board import Board
from ship import Ship
from dot import Dot
from exception import *

class Game:
    def __init__(self, size = 6):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
        
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        board = Board(size = self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    def print_board_v(self):
        print("-"*20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-"*20)
        print("Доска компьютера:")
        print(self.ai.board)

    def print_board_h(self):
        col_len = 35

        us_string = self.us.board.__str__().split('\n')
        ai_string = self.ai.board.__str__().split('\n')
        
       
        print('='.join([str('-'*20).center(col_len), str('-'*20).center(col_len)]))
        print('='.join(["Доска пользователя:".center(col_len), "Доска компьютера:".center(col_len)]))
        print('='.join([str('-'*20).center(col_len), str('-'*20).center(col_len)]))
        for a, b in zip(us_string, ai_string):
            print('='.join([a.center(col_len), b.center(col_len)]))

    def loop(self):
        num = 0
        while True:
            self.print_board_h()
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                self.print_board_h()
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                self.ai.board.hid = False
                self.print_board_h()
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()