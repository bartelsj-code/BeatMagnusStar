from path_finder import PathFinder
from control_variables import *
from game_filter import game_filter

g = PathFinder(USER, DESTINATION, (START_YEAR, START_MONTH), game_filter)
g.find_path()
