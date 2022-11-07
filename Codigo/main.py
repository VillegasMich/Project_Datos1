import math
import time
import gmplot as gm
from collections import deque
import pandas as pd
from dijkstra import shortest_path, generate_path
from map_visual import mark_route, open_gmap

medellin_full = pd.read_csv("medellin_full.csv", sep=';')
medellin_full.harassmentRisk = medellin_full.harassmentRisk.fillna(medellin_full.harassmentRisk.mean())

"""
With the generated path and the graph we collect the total length and harassment risk
"""

def get_length_harassmentRisk(graph, path):
    length = 0
    harassment = 0
    visited = []
    
    for node in path:
        for neighbor, weight in graph[node].items():
            if neighbor in path and neighbor not in visited:
                length += weight[0]
                harassment += weight[1]
                visited.append(neighbor)
    
    harassment = harassment/len(path)
    return length, harassment


"""
The main method to run the program
"""

def main():
    
    """
    Apikey for the gmplot
    """
    apikey = 'AIzaSyBY5YTpkQusJ2LUqk2U3TzhJChS9p8_yqM'

    """
    The graph (dictionary) is initialized with all unique sources pointing to an empty dictionary.
    """
    unique_origins = medellin_full.origin.unique()
    graph = {}
    
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
    
    # EAFIT to UNAL 
    
    source = "(-75.5778046, 6.2029412)" 
    destination = "(-75.5762232, 6.266327)" 
    
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
    time_r1_start = time.perf_counter()
    prev1 = shortest_path(graph, source, destination, lambda length, harassment: length*harassment)
    route1 = deque()
    path1 = generate_path(prev1, destination, route1)
    length1, harassment1 = get_length_harassmentRisk(graph, path1)
    time_r1_end = time.perf_counter()
    mark_route(path1, 'red', gmap)
    
    print(" ")
    print(f'length of the first path: {length1}')
    print(f'Harassment risk of the first path: {harassment1/len(path1)}')
    print(f"The fist route was generated in {time_r1_end-time_r1_start:0.4f} seconds\n")
    
    """
    Route for the shortest path by length+(80*harassment)
    """
    time_r2_start = time.perf_counter()
    prev2 = shortest_path(graph, source, destination, lambda length, harassment: length+(80*harassment))
    route2 = deque()
    path2 = generate_path(prev2, destination, route2)
    length2, harassment2 = get_length_harassmentRisk(graph, path2)
    time_r2_end = time.perf_counter()
    mark_route(path2, 'yellow', gmap)
    
    print(f'length of the second path: {length2}')
    print(f'Harassment risk of the second path: {harassment2}')
    print(f"The second route was generated in {time_r2_end-time_r2_start:0.4f} seconds\n")
    
    """
    Route for the shortest path by length^(2*harassment)
    """
    time_r3_start = time.perf_counter()
    prev3 = shortest_path(graph, source, destination, lambda length, harassment: math.pow(length, 10*harassment))
    route3 = deque()
    path3 = generate_path(prev3, destination, route3)
    length3, harassment3 = get_length_harassmentRisk(graph, path3)
    time_r3_end = time.perf_counter()
    mark_route(path3, 'blue', gmap)
    
    print(f'length of the third path: {length3}')
    print(f'Harassment risk of the third path: {harassment3}')
    print(f"The third route was generated in {time_r3_end-time_r3_start:0.4f} seconds\n")
    
    open_gmap(gmap)
    
main()
