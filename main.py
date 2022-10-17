import math
import gmplot as gm
from collections import deque
import pandas as pd
from dijkstra import shortest_path, generate_path
from map_visual import mark_route, open_gmap

"""
El codigo para la segunda entrega está mas avanzado de lo requerido (practicamente completo)
Abajo se encuentra un ejemplo random para probar el correcto funcionamiento del código
"""

medellin_full = pd.read_csv("medellin_full.csv", sep=';')

def main():
    
    """
    Apikey for the gmplot
    """
    apikey = 'AIzaSyCJfnE-UzN0Hc89l89kxl6D8MkVopUYtO4'
    
    unique_origins = medellin_full.origin.unique()
    graph = {}

    """
    The graph (dictionary) is initialized with all unique sources pointing to an empty dictionary.
    """
    for og in unique_origins:
        graph[og] = {}

    """
    We traverse all medelllin_full with .iterrows()
    Initialize the corresponding variables using row['column'] to access the data
    We create the dictionary (new_destination) where the key=destination and the value=(length, harassment)
    we use the .update to add this new_destination to the network
    """
    for _, row in medellin_full.iterrows():
        origin = row["origin"]
        destination = row['destination']
        length = row['length']
        harassment = row['harassmentRisk']
        oneway = row['oneway']
        
        if oneway == True:
            new_destination = { destination: (length, harassment) }
            graph[origin].update(new_destination)
            try:
                other_side = { origin: (length, harassment) }
                graph[destination].update(other_side)
            except KeyError:
                graph[destination] = other_side

        new_destination = { destination: (length, harassment) }
        graph[origin].update(new_destination)
    
    #! Random example to test the algorithms
    
    source = "(-75.5705202, 6.2106275)"
    destination = "(-75.5613081, 6.2357138)" 
    
    source_split = source.split()
    source_lat = float(source_split[1].strip().strip(')'))
    source_lon = float(source_split[0].strip('(').strip(','))
    
    """
    Using gmplot to open the map on google maps
    The map always opens on the source coordinates 
    """
    gmap = gm.GoogleMapPlotter(source_lat, source_lon, 17, apikey=apikey, map_type="roadmap")
    
    """
    Route for the shortest path by length*harassment
    """
    prev1 = shortest_path(graph, source, destination, lambda length, harassment: length*harassment)
    route1 = deque()
    path1 = generate_path(prev1, destination, route1)
    mark_route(path1, 'red', gmap)
    
    """
    Route for the shortest path by length+(80*harassment)
    """
    prev2 = shortest_path(graph, source, destination, lambda length, harassment: length+(80*harassment))
    route2 = deque()
    path2 = generate_path(prev2, destination, route2)
    mark_route(path2, 'yellow', gmap)
    
    """
    Route for the shortest path by length^(2*harassment)
    """
    prev3 = shortest_path(graph, source, destination, lambda length, harassment: math.pow(length, 10*harassment))
    route3 = deque()
    path3 = generate_path(prev3, destination, route3)
    mark_route(path3, 'blue', gmap)
    
    open_gmap(gmap)
    
main()
