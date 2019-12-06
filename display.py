from tkinter import *
import time
import queue
import matplotlib



CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

animation = Tk()
c = Canvas(animation, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
c.pack()


def display_road(road_cords):
    c.create_polygon(*road_cords)
    c.update()
    c.update_idletasks()

#testing, only shows center of road
def display_center_test(cords):
    x, y = 0, 1
    for cord in cords:
        c.create_rectangle(cord[x] - 10, cord[y] + 10, cord[x] + 10, cord[y] - 10)
    c.update()

def clear_canvas():
    c.delete("all")

def draw_person(state):
	c.create_oval(380, 550, 420, 590) #40 x 40
	c.create_rectangle(365, 590, 435, 660) #70 x 80
	if state == 0:
		#right arm
		c.create_line(435, 590, 465, 580)
		c.create_line(380, 590, 365, 630) #left arm
		c.create_line(365, 660, 355, 720) #left leg
		c.create_line(435, 660, 435, 730)
	mainloop()
