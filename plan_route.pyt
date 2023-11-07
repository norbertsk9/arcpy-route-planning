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
