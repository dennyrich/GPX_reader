import xml.etree.ElementTree as ET
import queue
from World import World


drawingFactor = 0.1
file = "circle_run_five_speed.gpx"
fileName = "../../../Downloads/" + file
tree = ET.parse(fileName)
root = tree.getroot()
#print(root.attrib)
trk = root[1]
trkseg = trk[2]

data_points = []
for data_packet in trkseg:
    data_points.append((float(data_packet.attrib.get('lat')),
                    float(data_packet.attrib.get('lon')),
                    float(data_packet[0].text), #elev
                    (data_packet[1].text[11:-1]))) #time
#print(data_points)
running_world = World(data_points)
running_world.run()
