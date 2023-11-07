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
