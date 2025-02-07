from typing import *
from api_interfacing import get_games_since_date, get_player_info, get_player_stats
from player_node import PlayerNode
from multi_queue import MultiQueue
import time, webbrowser
import os

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
        

    # def get_valid_neighbors(self, source_node: PlayerNode):
    #     '''goes through games played by source and finds all valid neighbors. 
        
    #     Returns:
    #         a list nodes
    #     '''
    #     source_username = source_node.username
    #     wins = source_node.winning
    #     all_games_played = get_games_since_date(source_username, self.start_date)
    #     opponent_nodes = set()
    #     for game in all_games_played:
    #         usable, source_json, opponent_json = self.game_filter(game, source_username, wins)
    #         if usable:
    #             opponent_json['username'] = opponent_json['username'].lower()
    #             opponent_username = opponent_json['username']
    #             if not opponent_username in self.all_nodes:
    #                 node = PlayerNode(opponent_username, source_node, game['url'], wins)
    #                 self.all_nodes[opponent_username] = node
    #             node = self.all_nodes[opponent_username]
    #             if node.winning != source_node.winning:
    #                 source_node.missing_link = game['url']
    #                 return [node]
    #             opponent_nodes.add(node)
    #             source_node.update_ratings(source_json['rating'], game['time_class'])
    #             node.update_ratings(opponent_json['rating'], game['time_class'])
    #     return list(opponent_nodes)
    
    # def get_heuristic(self, current_rating, goal_rating):
    #     # return 0
    #     return abs((goal_rating - current_rating)-SPACER)/AVERAGE_JUMP
    
    def set_up_initial(self, username, winning):
        node = PlayerNode(username, None, None, winning)
        node.steps_taken = 0
        return node
    
    def assign_cost(self, node: PlayerNode):
        if node.winning:
            rating_difference = node.get_distance(self.last_losing)
        else:
            rating_difference = node.get_distance(self.last_winning)
        node.total_cost = node.steps_taken + self.get_heuristic(node, rating_difference)

    # def reconstruct_path(self, node1: PlayerNode, node2: PlayerNode):
    #     n1 = node1  #missing link
    #     n2 = node2  #must pass down, then recieve

    #     part1 = []
    #     while n1 != None:
    #         part1.append(n1)
    #         n1 = n1.parent

    #     part2 = []
    #     while n2 != None:

    #         part2.append(n2)
    #         n2 = n2.parent

    #     for i in range(len(part2)-1, 0, -1):
    #         part2[i].game = part2[i-1].game
    #     part2[0].game = node1.missing_link

    #     if node2.winning:
    #         path = part2[::-1] + part1
    #     else:
    #         path = part1[::-1] + part2


    #     print(path)

    #     for node in path:
    #         time.sleep(0.1)
    #         try:
    #             webbrowser.open(node.game, new=2)
    #         except:
    #             pass
   


       
    # def account_closed(self, node):
    #     info = get_player_info(node.username)
    #     return info['status'] in ["closed:fair_play_violations","closed"]
    
    # def display_exploration(self):
    #     cols, lines = os.get_terminal_size()
    #     filler = " "
        
    #     w = f"{self.last_winning.chain_rep()} {self.last_winning.g_rating:.2f}"
    #     l = f"{self.last_losing.g_rating:.2f} {self.last_losing.chain_rep()}"
    #     middle = f"---"

    #     fill_space = cols-(len(w)+len(l)) - 3
    #     center = f"{middle:{filler}^{fill_space}}"

    #     line = w + center + l

    #     print(line)

    # def display_queue(self):
    #     cols, lines = os.get_terminal_size()
    #     fill_space = cols - 3
    #     filler = " "
    #     center = f"{str(self.mq):{filler}^{fill_space}}"
    #     print(center)

            



    def find_path(self) -> list[PlayerNode]:
        
        '''
        Finds Path from User to Destination using A* in two directions.
        Once, from user going towards destination, once from destination going towards user. 

        There are two sets, user_visited and dest_visited, that represent the each origin's respective explored territory.
        '''

        self.user_node = self.set_up_initial(self.user_username, winning = True)
        self.dest_node = self.set_up_initial(self.dest_username, winning = False)

        self.last_losing = self.dest_node
        self.last_winning = self.user_node

        multi_queue = MultiQueue()

        for node in (self.user_node, self.dest_node):
            self.assign_cost(node)
            multi_queue.push(node)

        # self.mq = multi_queue

        

        # while multi_queue:
        #     current_node: PlayerNode = multi_queue.pop()
        #     if current_node.winning:
        #         self.last_winning = current_node
        #     else:
        #         self.last_losing = current_node

        #     self.display_exploration()
            
        #     if self.account_closed(current_node):
        #         print("\t^ cheater or speedrun account (ignored)")
        #         continue
            
        #     neighbor_nodes = self.get_valid_neighbors(current_node)
            
        #     if len(neighbor_nodes) == 0:
        #         continue
        #     if neighbor_nodes[0].winning != current_node.winning:
        #         return self.reconstruct_path(current_node, neighbor_nodes[0])
        #     for neighbor_node in neighbor_nodes:
        #         neighbor_node.steps_taken = min(neighbor_node.steps_taken,  current_node.steps_taken + 1)
        #         self.assign_cost(neighbor_node)
        #         if not neighbor_node.visited:
        #             multi_queue.push(neighbor_node)
        #             neighbor_node.visited = True

        #     for node in multi_queue:
        #         self.assign_cost(node)
        #     multi_queue.clean()

        #     self.display_queue()



            



