from tkinter import *
import queue

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

animation = Tk()
c = Canvas(animation, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
c.pack()


def display_road(road_cords):
    c.create_polygon(*road_cords)
    c.update()

#testing, only shows center of road
def display_center_test(cords):
    x, y = 0, 1
    for cord in cords:
        c.create_rectangle(cord[x] - 10, cord[y] + 10, cord[x] + 10, cord[y] - 10)
    c.update()

def clear_canvas():
    c.delete("all")
