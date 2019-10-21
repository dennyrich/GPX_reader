from time import sleep
import math
from tkinter import *
import queue
from display import display_road, display_center_test, clear_canvas

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

# animation = Tk()
# c = Canvas(animation, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
# c.pack()

# class Coord(object):
#     def __init__(self, x, y, elev):
#         self.x = x
#         self.y = y
#         self.elev = elev

class Vector2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def change_basis(self, other_vector):
        perpen_x = -1 * self.y
        perpen_y = self.x
        #matrix multiplication
        #[x    perpen_x] [other_x] = [new_x]
        #[y    perpen_y] [otehr_y]   [new_y]
        new_x = self.x * other_vector.x + perpen_x * other_vector.y
        new_y = self.y * other_vector.x + perpen_y * other_vector.y
        return Vector2D(new_x, new_y)
    def scaleX(self, factor):
        self.x *= factor
    def scaleY(self, factor, change_elev, elev_factor):
        self.y *= factor
        self.y += change_elev * elev_factor


class World(object):
    """have queue of sides that get higher or lower
    trkseg is list of coordinates
    data points are (lat, lon, elev, time).
    """
    curr_axis = Vector2D(1, 1)

    def __init__(self, data_queue):
        self.data_queue = data_queue

    def run(self):
        prevTime = self.data_queue[0][3] #hh:mm:ss
        prevHours = int(prevTime[0:2])
        prevMins = int(prevTime[3:5])
        prevSecs = int(prevTime[6:])
        while len(self.data_queue) > 1:
            road_points = self.create_points()
            self.create_points()
            del self.data_queue[0] #removes first position thing
            time = self.data_queue[0][3]

            changeHours = int(time[0:2]) - prevHours
            changeMins = int(time[3:5]) - prevMins
            changeSecs = int(time[6:]) - prevSecs
            changeTime = changeHours * 3600 + changeMins * 60 + changeSecs

            prevHours = int(time[0:2])
            prevMins = int(time[3:5])
            prevSecs = int(time[6:])
            clear_canvas()
            #time.sleep(0.1)

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

    def create_points(self):
        elev_factor = 30
        distance_factor = 50000 #or change in lat/lon
        distance_factorX = 50000

        """insures position is on screne. pos is an array of length 2: [x, y]
        """
        def update_pos(curr_pos, vector):
            curr_pos[0] += vector.x
            curr_pos[1] += vector.y

        def validate_pos(pos):
            return pos[0] >= 0 and pos[0] <= CANVAS_WIDTH and pos[1] >= 0 and pos[1] <= CANVAS_HEIGHT

        def calc_width(distance_from_start):
            #print("width: ", 400 - ((distance_from_start ** 2) * 0.0005))
            return 800 - (distance_from_start * 0.7)

        def calc_distance(pos):
            #print(math.sqrt((pos[0] - 400) ** 2 + pos[1] ** 2))
            return math.sqrt((pos[0] - 400) ** 2 + (CANVAS_HEIGHT - pos[1]) ** 2)

        """insures lines of polygon do not cross, forming a bad figure
        """
        def is_good_coord(x, y, curr_pos, prev_pos, last_pos_in_arr):
            #pos is higher but side extends lower than previous side
            if (curr_pos[1] > prev_pos[1] and y < last_pos_in_arr[1]):
                return False
            #opposite of above
            if (curr_pos[1] < prev_pos[1] and y > last_pos_in_arr[1]):
                return False
            #if pos is to the right of previous but its side extends to the left of previous side
            if (curr_pos[0] > prev_pos[0] and y < last_pos_in_arr[0]):
                return False
            #opposite of above
            if (curr_pos[0] < prev_pos[0] and y > last_pos_in_arr[0]):
                return False
            return True

        def plot_points_test(arr):
            for i in range(0, len(arr) - 1, 2):
                x = arr[i]
                y = arr[i + 1]
                c.create_rectangle(x - 10, y + 10, x + 10, y - 10 , fill = "blue")
                c.update()
            sleep(.1)

        curr_pos = [CANVAS_WIDTH / 2, CANVAS_HEIGHT] #starts at bottom center
        distance_from_start = 0
        bottom_leftX, bottom_rightX = 400 - calc_width(0)/2, 400 + calc_width(0)/2
        bottom_leftY, bottom_rightY = CANVAS_HEIGHT, CANVAS_HEIGHT

        first_x = self.data_queue[0][0]
        first_y = self.data_queue[0][1]
        second_x = self.data_queue[1][0]
        second_y = self.data_queue[1][1]

        curr_vector = Vector2D(second_x - first_x, second_y - first_y)


        prevX_abs = self.data_queue[0][0]
        prevY_abs = self.data_queue[0][1]
        prev_elev = self.data_queue[0][2]

        positions_left = [bottom_leftX, bottom_leftY]
        positions_right = [bottom_rightX, bottom_rightY]
        line_array = [[CANVAS_WIDTH / 2, bottom_leftY]] #road without width

        for data in self.data_queue[1:]:
            #calculate absolute distance in x and y components
            changeX_abs = data[0] - prevX_abs
            changeY_abs = data[1] - prevY_abs
            elev = data[2]
            change_elev = elev - prev_elev
            vector_abs = Vector2D(changeX_abs, changeY_abs)
            vector_rel = curr_vector.change_basis(vector_abs)
            vector_rel.scaleX(distance_factorX)
            vector_rel.scaleY(distance_factor, change_elev, elev_factor)
            step_len = math.sqrt(changeX_abs**2 + changeY_abs**2)

            curr_vector = vector_rel
            prev_elev = elev

            update_pos(curr_pos, vector_rel)

            #for testing without width:
            line_array.append(curr_pos)

            #gives the road width
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
        #plot_points_test(poses)
        print(line_array)
        display_center_test(line_array)

    def testing(self):
        return
