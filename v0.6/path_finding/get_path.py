from path_finding.path_finder import PathFinder
from path_finding.control_variables import *
import os
import sys

def main(user, goal):
    year = YEAR
    month = MONTH
    date = (year, month)
    filtering_conditions = GAME_ATTRIBUTES
    database_path = 'C:\\Users\\jbart\\Desktop\\Projects\\Coding Projects\\BTM\\v0.6\\path_finding\\data.db'
    g = PathFinder(user, goal, date, filtering_conditions, database_path)
    player_usernames, game_urls = g.find_path(EXPLORATION_LIMIT)
    return player_usernames

