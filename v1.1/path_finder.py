from typing import *
from api_interfacing import get_games_since_date, get_player_info, get_player_stats
from player_node import PlayerNode
from multi_queue import MultiQueue
from multi_set import MultiSet
from control_variables import AVERAGE_JUMP
import time, webbrowser

class PathFinder:
    user_username: str
    dest_username: str
    start_date: tuple[str, str]
    def __init__(self, user_username, dest_username, start_date, game_filter) -> None:
        self.user_username = user_username
        self.dest_username = dest_username
        self.start_date = start_date
        self.game_filter = game_filter
        self.all_nodes: dict[str, PlayerNode] = {}
        

    def get_valid_neighbors(self, source_node: PlayerNode):
        '''goes through games played by source and finds all valid neighbors. 
        
        Returns:
            a list nodes
        '''
        source_username = source_node.username
        wins = source_node.winning
        all_games_played = get_games_since_date(source_username, self.start_date)
        opponent_nodes = set()
        for game in all_games_played:
            usable, opponent_json = self.game_filter(game, source_username, wins)
            if usable:
                opponent_json['username'] = opponent_json['username'].lower()
                opponent_username = opponent_json['username']
                if not opponent_username in self.all_nodes:
                    node = PlayerNode(opponent_username, source_node, game['url'], wins)
                    self.all_nodes[opponent_username] = node
                node = self.all_nodes[opponent_username]
                if node.winning != source_node.winning:
                 
                    source_node.missing_link = game['url']
                    return [node]
                opponent_nodes.add(node)
                node.update_ratings(opponent_json['rating'], game['time_class'])
        return list(opponent_nodes)
    
    def get_heuristic(self, current_rating, goal_rating):
        # return 0
        return abs(goal_rating - current_rating)/AVERAGE_JUMP
    
    def set_up_initial(self, username, winning):
        node = PlayerNode(username, None, None, winning)
        node.set_real_ratings(get_player_stats(username))
        return node
    
    def assign_cost(self, node: PlayerNode):
        if node.winning:
            goal_rating = self.dest_node.g_rating
        else:
            goal_rating = self.user_node.g_rating
        node.heuristic = self.get_heuristic(node.g_rating, goal_rating)
        node.total_cost = node.steps_taken + node.heuristic

    def reconstruct_path(self, node1: PlayerNode, node2: PlayerNode):
        print("building path")
        print(node1.missing_link)

       
    def account_closed(self, node):
        info = get_player_info(node.username)
        return info['status'] in ["closed:fair_play_violations","closed"]


    def find_path(self) -> list[PlayerNode]:
        
        '''
        Finds Path from User to Destination using A* in two directions.
        Once, from user going towards destination, once from destination going towards user. 

        There are two sets, user_visited and dest_visited, that represent the each origin's respective explored territory.
        '''
        
        self.user_node = self.set_up_initial(self.user_username, winning = True)
        self.dest_node = self.set_up_initial(self.dest_username, winning = False)

        self.assign_cost(self.user_node)
        self.assign_cost(self.dest_node)

        multi_queue = MultiQueue()
        multi_queue.push(self.user_node)
        multi_queue.push(self.dest_node)

        while multi_queue:
            current_node: PlayerNode = multi_queue.pop()
            current_node.visited = True
            print(f"{current_node.chain_rep()}")
            
            if self.account_closed(current_node):
                print("\t^ cheater or speedrun account (ignored)")
                continue
            
            neighbor_nodes = self.get_valid_neighbors(current_node)
            if neighbor_nodes[0].winning != current_node.winning:
                    return self.reconstruct_path(current_node, neighbor_node)
            for neighbor_node in neighbor_nodes:
                neighbor_node.steps_taken = current_node.steps_taken + 1
                self.assign_cost(neighbor_node)
                if not neighbor_node.visited:
                    multi_queue.push(neighbor_node)



            



