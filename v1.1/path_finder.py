from typing import *
from api_interfacing import get_games_since_date, get_player_info, get_player_stats
from player_node import PlayerNode

class PathFinder:
    user_username: str
    dest_username: str
    start_date: Tuple[str, str]
    def __init__(self, user_username, dest_username, start_date) -> None:
        self.user_username = user_username
        self.dest_username = dest_username
        self.start_date = start_date

    def find_path() -> List[PlayerNode]:
        pass







c


g = PathFinder("blah277", "gothamchess", ("2024", "10"))
g.find_path()
