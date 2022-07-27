from random import randint
from board import Board

from dot import Dot
from ship import Ship

a=Dot(2,2)
b =Dot(3, 1)

s1 = Ship(a, 4, 0)
s2 = Ship(a, 4, 1)

board = Board(hid=False, size=6)
board.add_ship(s1)
#board.add_ship(s2)

print(board)
#print(board.busy)
print(board.shot(Dot(1,1)))
print(board)







