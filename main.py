import pandas as pd
import pprint

medellin_full = pd.read_csv("medellin_full.csv")

def main():
    
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

    pprint.pprint(graph["(-75.5705202, 6.2106275)"]) # Example

main()
