from queue import PriorityQueue

"""
Dijkstra algorithm with a priority queue from the PriorityQueue module
Prev is a dictionary to keep track of the previous vertex to generate the path
It takes a weight_func (lambda) to determine how to calculate the distances for the algorithm
"""

def shortest_path(graph, source, destination, weight_func):
    dist = {}
    prev = {}
    pq = PriorityQueue()
    
    prev[source] = None
    dist[source] = 0
    pq.put((dist[source], source))
    
    for vertex in graph:
        if vertex != source:
            dist[vertex] = float('infinity')
            prev[vertex] = None
        
    
    while not pq.empty():
        _, node = pq.get()
        
        for neighbor, weight in graph[node].items():
            distance = dist[node] + weight_func(weight[0], weight[1])
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = node
                pq.put((distance, neighbor))
    
    return prev

"""
Using backtracking to select only the necessary vertices from the destination to the source
It returns the path of the algorithm 
"""
def generate_path(prev, curr, path):
    if prev[curr] == None:
        path.appendleft(curr)
        return path
    else:
        path.appendleft(curr)
        return generate_path(prev, prev[curr], path)