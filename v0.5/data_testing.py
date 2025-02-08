from data_access import DataAccess
from control_variables import *

username = USER
start_date = (START_YEAR, START_MONTH)

g = DataAccess()

games = g.get_matching_games(username, start_date)


