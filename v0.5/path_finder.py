from typing import *
from player_node import PlayerNode
import heapq
import time, webbrowser
import os
from math import floor
from data_access import DataAccess

class PathFinder:
    user_username: str
    dest_username: str
    start_date: tuple[str, str]
    def __init__(self, user_username, dest_username, start_date, game_filter, jump) -> None:
        self.db = DataAccess()
        self.user_username = user_username
        self.dest_username = dest_username
        self.start_date = start_date
        self.game_filter = game_filter
        self.all_nodes: dict[str, PlayerNode] = {}
        self.jump = jump
        self.dest_set = set()

    def init_ratings(self):
        source_username = self.source_node.username
        is_winning = self.source_node.winning
        relevant_games = self.db.get_matching_games(source_username, self.start_date, is_winning)
        for game in relevant_games[:4]:
            pass

        # for game_json in all_games_played:
        #     usable, source_json, opponent_json = self.game_filter(game_json, source_username, is_winning)
        #     if usable:
        #         self.source_node.update_ratings(source_json['rating'], game_json['time_class'])
        # self.source_node.set_comp_rating()

    # def get_valid_neighbors(self, source_node: PlayerNode):
    #     '''
    #     Goes through games played by source and finds all valid neighbors. 
    #     Returns:
    #         a list nodes

    #     '''
    #     source_username = source_node.username
    #     is_winning = source_node.winning
    #     all_games_played = get_games_since_date(source_username, self.start_date)
    #     opponent_nodes = set()
    #     for game_json in all_games_played:
    #         usable, source_json, opponent_json = self.game_filter(game_json, source_username, is_winning)
    #         if usable:
    #             opponent_username = opponent_json['username'].lower()
    #             if opponent_username not in self.all_nodes:
    #                 self.all_nodes[opponent_username] = PlayerNode(opponent_username, source_node, game_json['url'], is_winning)
    #             opponent_node = self.all_nodes[opponent_username]
    #             if opponent_node in self.dest_set:
    #                 return game_json
    #             opponent_nodes.add(opponent_node)

    #             source_node.update_ratings(source_json['rating'], game_json['time_class'])
    #             opponent_node.update_ratings(opponent_json['rating'], game_json['time_class'])

    #     return list(opponent_nodes)
        


    def set_up_initial(self, username, winning):
        node = PlayerNode(username, None, None, winning)
        node.steps_taken = 0
        self.all_nodes[username] = node
        return node
    
    # # def generate_dest_set(self, node, explore_limit):
    #     raise Exception("reminder you need to eliminate cheaters")
            
        
    #     '''
    #     takes in the destination node and finds all valid nodes within a certain radius (which has to be determined dynamically)

    #     radius is determined after the number of nodes to be searched for the next iteration exceeds the explore limit
    #     '''

    #     prog_length = 60
    #     depth = 1
    #     visited = set()
    #     completed_set = set([node])
    #     while len(completed_set) <= explore_limit and depth < 7:
    #         print(f"searching depth: {depth}")
    #         set_being_built = set([])
    #         for element in completed_set:
    #             visited.add(element)
            
    #         for i, element in enumerate(completed_set):
    #             bar_length = int(prog_length*(i+1)/len(completed_set))
    #             bar = "#"*bar_length+" "*(prog_length-bar_length)
    #             bar_frame = f"[{bar}]"
                
    #             for neighbor in self.get_valid_neighbors(element):
                
    #                 if neighbor not in visited:
    #                     fill = " "*(len(neighbor.username) + 16)
    #                     print(f"{bar_frame} adding: {fill}", end = "\r")
    #                     print(f"{bar_frame} adding: {neighbor.username}", end = "\r")
    #                     time.sleep(0.01)
    #                     set_being_built.add(neighbor)
                
    #         print(f"{bar_frame} {len(set_being_built)} depth {depth} users added                 ")
                        
    #         completed_set = set_being_built
    #         depth += 1

    #     self.dest_set = completed_set
    #     for e in self.dest_set:
    #         e.set_comp_rating()

    # def determine_target_rating(self, tr):
    #     #still needs to be adjusted to search descent
    #     frontier_list = list(self.dest_set)
    #     frontier_list.sort(key = lambda p: p.comp_rating)
    #     target_index = floor(tr*len(frontier_list))
    #     lowered_by = self.jump/3
    #     self.target_rating = frontier_list[target_index].comp_rating - lowered_by

    # def get_heuristic(self, node):
    #     return (abs(self.target_rating-node.comp_rating)/self.jump)
        

    def find_path(self, exploration_limit, target_placement):
        '''
        Finds Path from User to Dest by first finding all nodes within a certain distance from the destination (like maybe two)
        and using these in a set as a target for A* starting from the user.
        
        '''
        self.source_node = self.set_up_initial(self.user_username, winning = True)
        self.init_ratings() #to update ratings
        # self.dest_node = self.set_up_initial(self.dest_username, winning = False)
        # self.generate_dest_set(self.dest_node, exploration_limit)
        # self.determine_target_rating(target_placement)

        # print(self.target_rating)
        # print(self.source_node.comp_rating)
        # to_be_visited = []
        # visited = set()

        # self.source_node.steps_taken = 0
        # self.source_node.heuristic = self.get_heuristic(self.source_node)
        # self.source_node.set_cost()
        # heapq.heappush(to_be_visited, self.source_node)

    #     while to_be_visited:
    #         current = heapq.heappop(to_be_visited)

    #         # if current in visited:
    #         #     print(f"duplicate found!!   {current}")
    #         #     continue
    #         # # else:
    #         #     visited.add(current)

    #         print(current)

    #         info = get_player_info(current.username)
    #         if info["status"] in ["closed:fair_play_violations","closed"]:
    #             print("\t^ cheater or speedrun account (not included)")
    #             continue

    #         neighbors = self.get_valid_neighbors(current)
    #         if type(neighbors) != list:
    #             rels = (current, neighbors)
    #             break
            
            
    #         for neighbor in neighbors:
    #             if neighbor in visited:
    #                 continue
    #             neighbor.set_comp_rating()
    #             neighbor.steps_taken = min(neighbor.steps_taken, current.steps_taken + 1)
    #             neighbor.heuristic = self.get_heuristic(neighbor)
    #             neighbor.set_cost()
    #             if neighbor not in visited:
    #                 visited.add(neighbor)
    #                 heapq.heappush(to_be_visited, neighbor)
    #         heapq.heapify(to_be_visited)

    #     print(rels)
            

            
            

