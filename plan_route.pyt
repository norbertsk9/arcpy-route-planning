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

nodes_dict = {}

# Check if coordinates already exist in the dictionary
def if_exists(x, y, nodes_dict):
    if (x, y) in nodes_dict.keys():
        return nodes_dict[(x, y)]
    return -1

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

nodes = {}
edges = {}

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

# Adjacency list
def adjacency_list():
    adjacency_dict = {}
    for i in edges:
        if edges[i].fr not in adjacency_dict.keys() and edges[i].direction != 2:
            adjacency_dict[edges[i].fr] = []
        if edges[i].direction != 2:
            adjacency_dict[edges[i].fr].append(edges[i].to)
            adjacency_dict[edges[i].fr].append(edges[i].cost)
        if edges[i].to not in adjacency_dict.keys() and edges[i].direction != 1:
            adjacency_dict[edges[i].to] = []
        if edges[i].direction != 1:
            adjacency_dict[edges[i].to].append(edges[i].fr)
            adjacency_dict[edges[i].to].append(edges[i].cost)
    return adjacency_dict

def a_star_algorithm(start, end, adjacency_dict):
    print("Calculating the best route using the A* algorithm")
    arcpy.AddMessage("Calculating the best route using the A* algorithm")
    min_heap = []
    S = {start}
    Q = set()
    x = start

    def min_f(q, s):
        t = False
        for i in q:
            if i[1] not in s and not t:
                new_node_nr = i[1]
                min_f_val = i[0]
                t = True
            if i[1] not in s and t and i[0] < min_f_val:
                min_f_val = i[0]
                new_node_nr = i[1]
        return new_node_nr, min_f_val

    iteration = 0
    while True:
        if iteration != 0:
            new_node_nr, min_f_val1 = min_f(min_heap, S)
            S.add(new_node_nr)
            x = new_node_nr
            if new_node_nr == end:
                break
        n = 0
        for i in adjacency_dict[x]:
            if isinstance(i, int) and i not in S:
                cost = adjacency_dict[x][n + 1]
                if nodes[i].nr not in Q:
                    nodes[i].g = nodes[x].g + cost
                    nodes[i].f = nodes[i].h + nodes[i].g
                    nodes[i].predecessor = x
                if i in Q and nodes[x].g + cost < nodes[i].g:
                    nodes[i].g = nodes[x].g + cost
                    nodes[i].f = nodes[i].h + nodes[i].g
                heapq.heappush(min_heap, (nodes[i].f, i))
                Q.add(i)
            n += 1
        iteration += 1

def find_edges(route, edges_dict, end_node):
    edges_set = set()
    edges_dict_result = {}

    for i in edges_dict:
        if edges_dict[i].fr in route and edges_dict[i].fr != end_node:
            index_start = route.index(edges_dict[i].fr)
            if edges_dict[i].to == route[index_start + 1]:
                if edges_dict[i].fr not in edges_dict_result.keys():
                    edges_set.add(edges_dict[i].road_id)
                    edges_dict_result[edges_dict[i].fr] = [edges_dict[i].road_id, edges_dict[i].cost]
                if edges_dict[i].fr in edges_dict_result.keys() and edges_dict[i].cost < edges_dict_result[edges_dict[i].fr][1]:
                    id_road = edges_dict_result[edges_dict[i].fr][0]
                    edges_set.remove(id_road)
                    edges_set.add(edges_dict[i].road_id)
                    edges_dict_result[edges_dict[i].fr] = [edges_dict[i].road_id, edges_dict[i].cost]

        if edges_dict[i].to in route and edges_dict[i].to != end_node:
            index_start = route.index(edges_dict[i].to)
            if edges_dict[i].fr == route[index_start + 1]:
                if edges_dict[i].to not in edges_dict_result.keys():
                    edges_set.add(edges_dict[i].road_id)
                    edges_dict_result[edges_dict[i].to] = [edges_dict[i].road_id, edges_dict[i].cost]
                if edges_dict[i].to in edges_dict_result.keys() and edges_dict[i].cost < edges_dict_result[edges_dict[i].to][1]:
                    id_road = edges_dict_result[edges_dict[i].to][0]
                    edges_set.remove(id_road)
                    edges_set.add(edges_dict[i].road_id)
                    edges_dict_result[edges_dict[i].to] = [edges_dict[i].road_id, edges_dict[i].cost]

    return edges_set, edges_dict_result

def export_to_shapefile(data, edges_str, output_path, output_name):
    in_features = data
    where_clause = '"FID" IN ' + edges_str
    arcpy.env.overwriteOutput = True
    arcpy.FeatureClassToFeatureClass_conversion(in_features, output_path, output_name, where_clause)

def handle_traffic_jam(data, edges, start, end, output_path, output_name):
    import random
    edges_list = list(edges)

    if 0 < len(edges_list) < 10:
        selected_edge = random.choice(edges_list)
        print("Traffic jam on road ID: " + str(selected_edge))
        arcpy.AddMessage("Traffic jam on road ID: " + str(selected_edge))
        edges[selected_edge].cost = edges[selected_edge].cost * 100000

    if len(edges_list) >= 10:
        selected_edge1 = random.choice(edges_list)
        selected_edge2 = random.choice(edges_list)
        selected_edge3 = random.choice(edges_list)

        print("Traffic jam on road ID: " + str(selected_edge1))
        arcpy.AddMessage("Traffic jam on road ID: " + str(selected_edge1))
        print("Traffic jam on road ID: " + str(selected_edge2))
        arcpy.AddMessage("Traffic jam on road ID: " + str(selected_edge2))
        print("Traffic jam on road ID: " + str(selected_edge3))
        arcpy.AddMessage("Traffic jam on road ID: " + str(selected_edge3))

        edges[selected_edge1].cost = edges[selected_edge1].cost * 100000
        edges[selected_edge2].cost = edges[selected_edge2].cost * 100000
        edges[selected_edge3].cost = edges[selected_edge3].cost * 100000

    adjacency_dict = adjacency_list()
    a_star_algorithm(start, end, adjacency_dict)
    _, edges_str = find_edges(start, end, edges)
    output_name = output_name + "traffic_jam.shp"
    export_to_shapefile(data, edges_str, output_path, output_name)
    print(nodes[end].g)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Find the most optimal route"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_features = arcpy.Parameter(
            displayName="Road Layers:",
            name="in_features",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )

        in_features.filter.list = ["Polyline"]

        coord_start = arcpy.Parameter(
            displayName='Enter the starting point coordinates:',
            name='coord_start',
            datatype='GPPoint',
            parameterType='Required',
            direction='Input'
        )

        coord_end = arcpy.Parameter(
            displayName='Enter the ending point coordinates:',
            name='coord_end',
            datatype='GPPoint',
            parameterType='Required',
            direction='Input'
        )

        fastest_shortest = arcpy.Parameter(
            displayName='Select the route type:',
            name='fastest_shortest',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        )
        fastest_shortest.filter.type = "ValueList"
        fastest_shortest.filter.list = ['FASTEST', 'SHORTEST']

        output_path = arcpy.Parameter(
            displayName='Enter the output path for layers:',
            name='output_path',
            datatype='DEFolder',
            parameterType='Required',
            direction='Input'
        )

        output_name = arcpy.Parameter(
            displayName='Enter the name of the route layer:',
            name='output_name',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        )

        traffic_jam = arcpy.Parameter(
            displayName='Is there a traffic jam on this route?',
            name='traffic_jam',
            datatype='GPString',
            parameterType='Optional',
            direction='Input'
        )
        traffic_jam.filter.type = "ValueList"
        traffic_jam.filter.list = ['YES', 'NO']

        parameters = [in_features, coord_start, coord_end, fastest_shortest, output_path, output_name, traffic_jam]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    
    def execute(self, parameters, messages):
        try:
            in_features = parameters[0].values
            coord_start = parameters[1].value
            coord_end = parameters[2].value
            fastest_shortest = parameters[3].value
            output_path = parameters[4].valueAsText
            output_name = parameters[5].valueAsText
            traffic_jam = parameters[6].value

            load_graph(in_features, fastest_shortest == 'FASTEST', coord_end.X, coord_end.Y)

            start = find_node(coord_start.X, coord_start.Y, nodes_dict)
            end = find_node(coord_end.X, coord_end.Y, nodes_dict)

            if traffic_jam == 'YES':
                handle_traffic_jam(in_features, edges, start, end, output_path, output_name)
            else:
                adjacency_dict = adjacency_list()
                a_star_algorithm(start, end, adjacency_dict)
                _, edges_str = find_edges(start, end, edges)
                export_to_shapefile(in_features, edges_str, output_path, output_name)

        except Exception as e:
            messages.addErrorMessage(f"An error occurred: {str(e)}")
