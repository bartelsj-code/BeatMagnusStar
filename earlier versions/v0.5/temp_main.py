from path_finder import PathFinder
from control_variables import *
import webbrowser
import time


date = (START_YEAR, START_MONTH)
filtering_conditions = GAME_ATTRIBUTES
g = PathFinder(USER, DESTINATION, date, filtering_conditions)
player_usernames, game_urls = g.find_path(EXPLORATION_LIMIT)

print(player_usernames)
# webbrowser.open_new_tab(game_urls[0])
# time.sleep(0.4)
# for url in game_urls[1:]:
#     webbrowser.open(url, new=2)
#     time.sleep(0.1)


