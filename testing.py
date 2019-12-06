import math
from World import *

def test_vector():
    v1 = Vector2D(3,3)
    v2 = Vector2D(3,-3)
    v3 = v1.projectX_and_Y(v2)
    v3.print_vector()
    print(v2.angle_between(v1))
    print(v1.magnitude())

def test_draw_person():
    person = Runner()
    person.draw()


test_draw_person()

