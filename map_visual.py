import gmplot as gm
import webbrowser
import os


apikey = 'AIzaSyCJfnE-UzN0Hc89l89kxl6D8MkVopUYtO4' # (your API key here)

gmap = gm.GoogleMapPlotter(6.251786723353367, -75.56793100157581, 14, apikey=apikey, map_type="roadmap")
gmap.draw("map.html")
map_path = os.path.abspath("map.html")

"""
Highlight the limit of the map (medellin_full.csv)
Highlight the path of the algorithm 
"""

webbrowser.open(map_path ,new=1)