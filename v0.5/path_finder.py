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
        if user_username == dest_username:
            raise Exception("start username and destination username are the same")
        self.start_date = start_date
        self.game_filter = game_filter
        self.all_nodes: dict[str, PlayerNode] = {}
        self.threshold = jump[0]
        self.jump_above = jump[1]
        self.jump_below = jump[2]
        self.dest_set = set()

    def init_ratings(self):
        relevant_games = self.db.get_matching_games(username=       self.user_node.username, 
                                                    start_date=     self.start_date, 
                                                    is_winning=     self.user_node.winning,
                                                    filter=         self.game_filter)
        if len(relevant_games) == 0:
            raise Exception(f"No usable games found for {self.user_node.username}")
        for game in relevant_games:
            source_tup, opp_tup = game.source_opp(self.user_node.username)
            self.user_node.update_ratings(source_tup[1], game.time_control)
        self.user_node.set_comp_rating()
 

    def get_valid_neighbors(self, source_node: PlayerNode):
        '''
        Goes through relevant games played by source and finds all valid neighbors. 
        Returns:
            a list nodes
        '''
        source_username = source_node.username
        is_winning = source_node.winning
        relevant_games = self.db.get_matching_games(username=       source_username, 
                                                    start_date=     self.start_date,
                                                    is_winning=     is_winning,
                                                    filter=         self.game_filter)
        opponent_nodes = set()
        for game in relevant_games:
            source_tup, opp_tup = game.source_opp(source_username)
            opponent_username = opp_tup[0]
            if opponent_username not in self.all_nodes:
                self.all_nodes[opponent_username] = PlayerNode(opponent_username, source_node, game.url, is_winning)
        
            opponent_node = self.all_nodes[opponent_username]
            if opponent_node in self.dest_set:
                self.db.prepare_player_data(opponent_node.username)
                if self.db.is_player_closed(opponent_node.username):
                    print("\t^ at connection a cheater or speedrun account detected (not included)")
                    continue
                else:
                    return (opponent_node, game)
                
            opponent_nodes.add(opponent_node)
            source_node.update_ratings(source_tup[1], game.time_control)
            opponent_node.update_ratings(opp_tup[1], game.time_control)

        for opp in opponent_nodes:
            opp.set_comp_rating()
        source_node.set_comp_rating()
        
        return list(opponent_nodes)
        
    def set_up_initial(self, username, winning):
        node = PlayerNode(username, None, None, winning)
        node.steps_taken = 0
        self.all_nodes[username] = node
        return node
    
    def generate_dest_set(self, node, explore_limit):
        print("!") #check for cheats
        '''
        takes in the destination node and finds all valid nodes within a certain radius (which has to be determined dynamically)

        radius is determined after the number of nodes to be searched for the next iteration exceeds the explore limit
        '''
        skipping = False
        prog_length = 60
        depth = 1
        visited = set()
        completed_set = set([node])
        while not skipping and depth < 7:
            print(f"searching depth: {depth}")
            set_being_built = set([])
            for element in completed_set:
                visited.add(element)
            
            for i, element in enumerate(completed_set):
                self.db.prepare_player_data(element.username)
                if self.db.is_player_closed(element.username):
                    continue
                
                bar_length = int(prog_length*(i+1)/len(completed_set))
                bar = "#"*bar_length+" "*(prog_length-bar_length)
                bar_frame = f"[{bar}]"
                
                for neighbor in self.get_valid_neighbors(element):
                    if neighbor == self.user_node:
                        self.consolodate_path(
                            element, 
                            self.user_node,
                            self.db.get_matching_games(
                                username = self.user_node.username,
                                start_date= self.start_date,
                                is_winning=True,
                                filter=self.game_filter,
                                loser=element.username
                            )[0])
                        return self.extract_path()
                    
                
                    if neighbor not in visited:
                        fill = " "*(len(neighbor.username) + 16)
                        print(f"{bar_frame} adding: {fill}", end = "\r")
                        print(f"{bar_frame} adding: {neighbor.username}", end = "\r")
                        set_being_built.add(neighbor)

                if self.db.request_counter >= explore_limit:
                    print("    Search cancelled, data logged.                                                                       ")
                    skipping = True
                    break
            if not skipping:
                print(f"{bar_frame} {len(set_being_built)} depth {depth} users added                 ")
                        
            completed_set = set_being_built
            depth += 1
            
        self.dest_set = completed_set

    def calculate_heuristic(self, node):
        
        goal_rating = self.dest_node.comp_rating

        if node.comp_rating == goal_rating:
            return 0

        if node.comp_rating < goal_rating:
            return (min(self.threshold, goal_rating) - node.comp_rating) / self.jump_below + max(0, goal_rating - self.threshold) / self.jump_above

        return (node.comp_rating - max(self.threshold, goal_rating)) / self.jump_above + max(0, self.threshold - goal_rating) / self.jump_below

    def consolodate_path(self, far_node, close_node = None, game = None):

        
        far_nodes = []
        current = far_node
        while current.parent!= None:
            
            far_nodes.append(current)
            current = current.parent
        far_nodes.append(current)
        
        flipped = far_nodes[::-1]

        for i in range(len(flipped)-1):
            flipped[i].parent = flipped[i+1]
            flipped[i].game_url = flipped[i+1].game_url
        far_nodes[0].parent = close_node
        far_nodes[0].game_url = game.url
                    

    def extract_path(self):
        players = []
        games = []


        current = self.dest_node
        while current.parent != None:
            players.append(current.username)
            games.append(current.game_url)
            current = current.parent
        players.append(current.username)
        return players[::-1], games[::-1]

        



    def find_path(self, exploration_limit):
        
        '''
        Finds Path from User to Dest by first finding all nodes within a certain distance from the destination (like maybe two)
        and using these in a set as a target for A* starting from the user.
        
        '''
        
        self.user_node = self.set_up_initial(self.user_username, winning = True)
        self.init_ratings() #to update ratings
        self.dest_node = self.set_up_initial(self.dest_username, winning = False)
        res = self.generate_dest_set(self.dest_node, exploration_limit)
        if res is not None:
            return res
        
        to_be_visited = []
        visited = set()
        appeared = set()

        self.user_node.steps_taken = 0
        self.user_node.heuristic = self.calculate_heuristic(self.user_node)
        self.user_node.set_cost()
        heapq.heappush(to_be_visited, self.user_node)
        appeared.add(self.user_node)

        while to_be_visited:
            current = heapq.heappop(to_be_visited)
            
            if current in visited:
                raise Exception(f"duplicate found!!   {current}")
            visited.add(current)

            print(current)

            self.db.prepare_player_data(current.username)

            if self.db.is_player_closed(current.username):
                print("\t^ cheater or speedrun account (not included)")
                continue
            
            neighbors = self.get_valid_neighbors(current)
            if type(neighbors) != list:
                rels = (current, neighbors)
                break
            
            for neighbor in neighbors:
                if neighbor in appeared:
                    continue
                neighbor.set_comp_rating()
                neighbor.steps_taken = min(neighbor.steps_taken, current.steps_taken + 1)
                neighbor.heuristic = self.calculate_heuristic(neighbor)
                neighbor.set_cost()
                appeared.add(neighbor)
                heapq.heappush(to_be_visited, neighbor)
            heapq.heapify(to_be_visited)
        
        close_side_node = rels[0]
        far_side_node = rels[1][0]
        connecting_game = rels[1][1]
        self.consolodate_path(far_side_node, close_side_node, connecting_game)
        return self.extract_path()


       


            

            
            

