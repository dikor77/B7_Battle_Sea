from random import randint, choice
from board import Board

from dot import Dot
from ship import Ship

dots = []
for x in range(3):
    for y in range(3):
        dots.append(Dot(x,y))

print(dots)
print(choice(dots))

dots.remove(Dot(0, 0))

try:
    dots.remove(Dot(0, 0))
except ValueError:
    pass

print(dots)








