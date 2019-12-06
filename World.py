from time import sleep
import math
from tkinter import *
import queue
from display import display_road, display_center_test, clear_canvas, draw_person
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import numpy as np 

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

# 2 attributes: x coordinate and y coordinate
class Vector2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    #calculates horizontal and vertical components with respect to self
    def projectX_and_Y(self, other_vector):
        angle = self.angle_between(other_vector)
        # x = other_vector.x * self.angle_between(other_vector)
        # y = other_vector.y * self.angle_between(other_vector)
        #perp_vector_clock_wise = Vector2D(self.y, -1*self.x)

        x = other_vector.magnitude() * math.sin(angle * 1.2) 
        y = other_vector.magnitude() * math.cos(angle * 1.2)
        return Vector2D(x, y)

    def angle_between(self, other_vector):
        dot = self.x * other_vector.x + self.y * other_vector.y
        self_magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        other_magnitude = math.sqrt(other_vector.x ** 2 + other_vector.y ** 2)
        cos_angle = round(dot / (self_magnitude * other_magnitude), 6)
        print("cos angle", cos_angle)
        return math.acos(cos_angle)

    def scale(self, factor):
        self.x *= factor
        self.y *= factor 

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)    

    def print_vector(self):
        print("the vector is: <", self.x, self.y, ">")

class Runner(object):
    def __init__(self):
        self.state = 0

    def draw(self):
        draw_person(self.state)




#attrubutes: a data_queue("list" of coordinates from gpx file)
class World(object):
    """have queue of sides that get higher or lower
    trkseg is list of coordinates
    data points are (lat, lon, elev, time).
    """
    #curr_axis = Vector2D(1, 1)

    def __init__(self, data_queue):
        self.data_queue = data_queue
    """ sends queue to create points, displays the points, then removes the first
    data point from the queue... repeat until all have been removed
    """
    def run(self):
        prevTime = self.data_queue[0][3] #hh:mm:ss
        prevHours = int(prevTime[0:2])
        prevMins = int(prevTime[3:5])
        prevSecs = int(prevTime[6:])
        while len(self.data_queue) > 1:
            #clear_canvas()
            print(len(self.data_queue), " +++++++++++++++++++++++++++ ")
            road_points = self.create_points()
            #self.interpolate(road_points)
            del self.data_queue[0] #removes first position (as if passing that position)
            time = self.data_queue[0][3]

            changeHours = int(time[0:2]) - prevHours
            changeMins = int(time[3:5]) - prevMins
            changeSecs = int(time[6:]) - prevSecs
            changeTime = changeHours * 3600 + changeMins * 60 + changeSecs

            prevHours = int(time[0:2])
            prevMins = int(time[3:5])
            prevSecs = int(time[6:])

            clear_canvas()
            display_road(road_points)
            sleep(.1)
            

            #sleep(0.01)
            

    """keeps track of angle with respect to x axis.
    also keeps track of elevation and zoom factor increases
    as the bars move up.
    """


    def display_speed(self, pos_1, pos_2, delta_t):
        radius_earth = 6378.137
        delta_lat_meters = (pos_2[0] - pos_1[0])
        dist = math.sqrt((pos_2[0] - pos_1[0]) ** 2 + (pos_2[1] - pos_1[0]) ** 2)
        speed_coord_per_sec = dist / delta_t
        c.create_rectangle(10, 10, 200, 200, fill = "yellow")
        c.create_text(100, 100, text = str(speed))
    """***************************************************************************
    """

    def interpolate(self, points):
        # def transpose(p):
        #     points = p[:]
        #     for i in range(0, len(points) - 1, 2):
        #         temp = points[i]
        #         points[i] = points[i + 1]
        #         points[i + 1] = temp
        #     return points 

        degree = len(points) - 1
        # transposed = transpose(points)
        xk = [p[0] for p in points]
        print(xk)
        yk = [p[1] for p in points]
        print(yk)
        plt.plot(xk, yk)
        plt.show()
        xnew = [i for i in range(0, 800, 10)] #0 to 800, increment by 10
        ynew = spline(yk, xk, xnew, order=degree)

        xnew, ynew = ynew, xnew #switch the coordinates back

        plt.plot(xnew, ynew)
        plt.show()
        sleep(5)



    def create_points(self):
        elev_factor = 1
        distance_factor = 1000000 #or change in lat/lon


        """insures position is on screen. pos is an array of length 2: [x, y]
        """
        def update_pos(curr_pos, vector, change_elev):
            new_pos = curr_pos[:] #make a copy
            new_pos[0] += vector.x
            new_pos[1] -= (vector.y + change_elev * elev_factor) #since "up" is the negative direction in the canvas
            return new_pos

        def validate_pos(pos):
            return pos[0] >= 0 and pos[0] <= CANVAS_WIDTH and pos[1] >= 0 and pos[1] <= CANVAS_HEIGHT

        def calc_width(distance_from_start):
            #print("width: ", 400 - ((distance_from_start ** 2) * 0.0005))
            return 800 - (distance_from_start * 0.9)

        def calc_distance(pos):
            #print(math.sqrt((pos[0] - 400) ** 2 + pos[1] ** 2))
            return math.sqrt((pos[0] - 400) ** 2 + (CANVAS_HEIGHT - pos[1]) ** 2)

        def get_distance_factor(rep):
            return 6000000 - rep * 25000

        """insures lines of polygon do not cross, forming a bad figure
        """

        def plot_points_test(arr):
            for i in range(0, len(arr) - 1, 2):
                x = arr[i]
                y = arr[i + 1]
                c.create_rectangle(x - 10, y + 10, x + 10, y - 10 , fill = "blue")
                c.update()
            sleep(.1)

        #starting points on canvas
        curr_pos = [CANVAS_WIDTH / 2, CANVAS_HEIGHT] #starts at bottom center
        distance_from_start = 0
        bottom_leftX, bottom_rightX = 400 - calc_width(0)/2, 400 + calc_width(0)/2
        bottom_leftY, bottom_rightY = CANVAS_HEIGHT, CANVAS_HEIGHT

        #before going in loop, need to calculate current vector
        first_x = self.data_queue[0][0]
        first_y = self.data_queue[0][1]
        second_x = self.data_queue[1][0]
        second_y = self.data_queue[1][1]

        curr_direction = Vector2D(second_x - first_x, second_y - first_y)
        curr_direction.scale(distance_factor)

        prevX_abs = first_x
        prevY_abs = first_y
        prev_elev = self.data_queue[0][2]

        #initialize the array
        positions_left = [bottom_leftX, bottom_leftY]
        positions_right = [bottom_rightX, bottom_rightY]
        line_array = [[CANVAS_WIDTH / 2, bottom_leftY]] #road without width

        rep = 0 #used for calculating distance factor

        for data in self.data_queue[1:]:
            #calculate absolute distance in x and y components
            changeX_abs = data[0] - prevX_abs #abs means absolute; not scaled
            changeY_abs = data[1] - prevY_abs
            elev = data[2]
            change_elev = elev - prev_elev #in absolute terms
            vector_abs = Vector2D(changeX_abs, changeY_abs) #vector in terms of standard basis, not scaled
            distance_factor = get_distance_factor(rep)
            rep += 1
            vector_abs.scale(distance_factor)
    
            vector_abs.print_vector()
            vector_rel = vector_abs.projectX_and_Y(curr_direction)
            vector_rel.print_vector()
            #scale it to world of canvas

            #step_len = math.sqrt(changeX_abs**2 + changeY_abs**2)


            curr_pos = update_pos(curr_pos, vector_rel, change_elev)

            #for testing without width:
            line_array.append(curr_pos)

            #gives the road width
            #****** need to uncomment when ready
            distance_from_start = calc_distance(curr_pos)
            l_width = calc_width(distance_from_start)


            new_leftX = curr_pos[0] - l_width / 2
            new_leftY = curr_pos[1]
            new_rightX = curr_pos[0] + l_width / 2
            new_rightY = curr_pos[1]

            if not validate_pos(curr_pos):
                print("done")
                break


            last_pos_l = positions_left[-2:]
            last_pos_r = positions_right[0:2] #these are added to the front of array
            if True:#is_good_coord(new_leftX, new_leftY, curr_pos, prev_pos, last_pos_l):
                positions_left.extend([new_leftX, new_leftY])
            if True:#is_good_coord(new_rightX, new_rightY, curr_pos, prev_pos, last_pos_r):
                positions_right = [new_rightX, new_rightY] + positions_right


            #for the next iteration (below)
            prevX_abs = data[0]
            prevY_abs = data[1]
            prev_elev = data[2]


        poses = positions_left + positions_right
        print(line_array, "-------")
        display_center_test(line_array)
        #return line_array
        return poses 


        
        print("********")

    def testing(self):
        return
