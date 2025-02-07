from data_access import DataAccess
from control_variables import *

username = USER
start_date = (START_YEAR, START_MONTH)

g = DataAccess()
g.prepare_player_data(username)

