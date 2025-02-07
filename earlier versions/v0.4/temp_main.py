from path_finder import PathFinder
from control_variables import *
from game_filter import game_filter
from caching import prep_data

prep_data()
g = PathFinder(USER, DESTINATION, (START_YEAR, START_MONTH), game_filter, JUMP)
g.find_path(EXPLORATION_LIMIT, TARGET_PLACEMENT)
