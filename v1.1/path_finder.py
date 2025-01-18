from typing import *
from api_interfacing import get_games_since_date, get_player_info, get_player_stats
from player_node import PlayerNode
from multi_queue import MultiQueue

class PathFinder:
    user_username: str
    dest_username: str
    start_date: tuple[str, str]
    def __init__(self, user_username, dest_username, start_date, game_filter) -> None:
        self.user_username = user_username
        self.dest_username = dest_username
        self.start_date = start_date
        self.game_filter = game_filter
        self.user_stats = get_player_stats(user_username)   #json dict
        self.dest_stats = get_player_stats(dest_username)   #json dict
        self.all_nodes: dict[str, PlayerNode] = {}

    def get_valid_neighbors(self, source_username, wins):
        '''goes through games played by source and finds all valid neighbors. 
        
        Returns:
            a list nodes
        '''
        all_games_played = get_games_since_date(source_username, self.start_date)
        opponent_nodes = set()
        for game in all_games_played:
            usable, opponent_json = self.game_filter(game, source_username, wins)
            if usable:
                opponent_json['username'] = opponent_json['username'].lower()
                opponent_username = opponent_json['username']
                if not opponent_username in self.all_nodes:
                    node = PlayerNode(opponent_username, game['url'])
                    self.all_nodes[opponent_username] = node
                node = self.all_nodes[opponent_username]
                node.update_ratings(opponent_json['rating'], game['time_class'])
                opponent_nodes.add(node)
        return list(opponent_nodes)
    
    def get_heuristic(self, current_rating, dest_rating):
        return 0
    
    def set_up_initial(self, username):
        node = PlayerNode(username, None)
        node.set_real_ratings(get_player_stats(username))
        return node


    def find_path(self) -> list[PlayerNode]:
        '''
        Finds Path from User to Destination using A* in two directions.
        Once, from user going towards destination, once from destination going towards user. 

        There are two sets, user_visited and dest_visited, that represent the each origin's respective explored territory.
        '''
        user_node = self.set_up_initial(self.user_username)
        dest_node = self.set_up_initial(self.dest_username)

        print(user_node)
        print(dest_node)

        multi_queue = MultiQueue()

        user_visited: set[str] = set()
        dest_visited: set[str] = set()

        print(multi_queue)
        multi_queue.push(user_node, is_winner=True)
        multi_queue.push(dest_node, is_winner=False)
        print(multi_queue)


        neighbors1 = self.get_valid_neighbors(self.user_username, wins = True)
        neighbors2 = self.get_valid_neighbors(self.dest_username, wins =False)
  
