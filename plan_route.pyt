import arcpy
import math as m
import heapq

class Node:
    def __init__(self, nr, x, y, h):
        self.nr = nr
        self.x = x
        self.y = y
        self.g = 0
        self.h = h
        self.f = h
        self.predecessor = -1

    def __str__(self):
        return f"nr: {self.nr} x: {self.x} y: {self.y} {self.g} {self.h} {self.f} {self.predecessor}"

class Edge:
    def __init__(self, fr, to, cost, road_id, direction):
        self.fr = fr
        self.to = to
        self.cost = cost
        self.road_id = road_id
        self.direction = direction

    def __str__(self):
        return f"{self.road_id} {self.fr} {self.to} {self.cost} {self.direction}"

def find_node(x, y, nodes_dict):
    min_dist = m.sqrt((x - nodes_dict[0].x) ** 2 + (y - nodes_dict[0].y) ** 2)
    nearest_id = 0
    for i in nodes_dict:
        dist = m.sqrt((x - nodes_dict[i].x) ** 2 + (y - nodes_dict[i].y) ** 2)
        if dist < min_dist:
            min_dist = dist
            nearest_id = nodes_dict[i].nr
    return nearest_id

# Heuristic based on the Euclidean distance
def heuristic(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def add_edge(road_id, start_x, start_y, end_x, end_y, length, direction, end_x_coord, end_y_coord):
    h1 = heuristic(start_x, start_y, end_x_coord, end_y_coord)
    h2 = heuristic(end_x, end_y, end_x_coord, end_y_coord)

    # Add nodes
    node_from = if_exists(start_x, start_y, nodes_dict)
    node_to = if_exists(end_x, end_y, nodes_dict)

    if node_from == -1:
        id_from = len(nodes)
        nodes[id_from] = Node(id_from, start_x, start_y, h1)
        nodes_dict[(start_x, start_y)] = id_from
        node_from_id = id_from
    else:
        node_from_id = node_from

    if node_to == -1:
        id_to = len(nodes)
        nodes[id_to] = Node(id_to, end_x, end_y, h2)
        nodes_dict[(end_x, end_y)] = id_to
        node_to_id = id_to
    else:
        node_to_id = node_to

    # Add edges
    edges[road_id] = Edge(node_from_id, node_to_id, length, road_id, direction)

def cost_fastest(length, road_class):
    average_speed = 0
    if road_class == "A" or road_class == "S":
        average_speed = 110
    elif road_class == "G" or road_class == "GP":
        average_speed = 80
    elif road_class == "Z" or road_class == "L":
        average_speed = 40
    elif road_class == "I" or road_class == "D":
        average_speed = 25

    cost = round(((length / 1000) / average_speed) * 60, 2)
    return cost

def load_graph(data, is_fastest, end_x_coord, end_y_coord):
    id = 0
    print("Loading data")
    arcpy.AddMessage("Loading data")
    fields = ['FID', 'SHAPE@', 'roadClass', 'direction']

    with arcpy.da.SearchCursor(data, fields) as cursor:
        for row in cursor:
            start_point = row[1].firstPoint
            start_x = start_point.X
            start_y = start_point.Y

            end_point = row[1].lastPoint
            end_x = end_point.X
            end_y = end_point.Y

            length = round(row[1].length, 2)
            direction = row[3]
            road_class = row[2]

            if not is_fastest:
                cost = length
            else:
                cost = cost_fastest(length, road_class)

            if direction != 3:
                add_edge(id, start_x, start_y, end_x, end_y, cost, direction, end_x_coord, end_y_coord)

            id += 1
