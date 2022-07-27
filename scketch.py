from ntpath import join
from random import randint, choice
from board import Board
from game import Game

from dot import Dot
from ship import Ship

g = Game()

g.print_board_v()

print("=====================")
print(g.us.board.__str__().split('\n'))
print(g.ai.board.__str__().split('\n'))

for a, b in zip(g.us.board.__str__().split('\n'), g.ai.board.__str__().split('\n')):
    print(''.join([a.ljust(30), b.rjust(30)]))



