from api_interfacing import get_games_since_date, get_player_info, get_player_stats
from game_analysis import analyze_game
from control_variables import START_MONTH, START_YEAR, DESTINATION, GAME_ATTRIBUTES, AVERAGE_JUMP, USER
from player_node import PlayerNode
import webbrowser
import heapq
import time


def get_valid_neighbors(player_name, start_date):
    all_games_played = get_games_since_date(player_name, start_date)
    opponent_dict = {}  #username: rating
    links = {}
    for game in all_games_played:
        usable, opponent, game_link = analyze_game(game, player_name)
        if usable:
            links[opponent["username"]] = game_link
            if opponent["username"] not in opponent_dict:
                opponent_dict[opponent["username"]] = opponent["rating"]
            else:
                opponent_dict[opponent["username"]] = max(opponent_dict[opponent["username"]],opponent["rating"])
    return [(rating, username, links[username]) for username, rating in opponent_dict.items()]

def get_heuristic(current_rating, dest_rating):
    return abs(dest_rating - current_rating)/AVERAGE_JUMP

def open_path(leaf):
    curr = leaf
    while curr != None:
        time.sleep(0.1)
        try:
            webbrowser.open(curr.parent_game, new=2)
        except:
            pass
        curr = curr.parent


def find_path(user_username, dest_username, start_date):
    user_stats = get_player_stats(user_username)
    dest_stats = get_player_stats(dest_username)
    
    user_rating = user_stats["chess_{}".format(GAME_ATTRIBUTES["time_class"])]["last"]["rating"]
    dest_rating = dest_stats["chess_{}".format(GAME_ATTRIBUTES["time_class"])]["last"]["rating"]
    #using A*
    to_be_visited = []
    visited = set()

    
    start_node = PlayerNode(user_username, user_rating, None)
    start_node.g = 0
    start_node.h = get_heuristic(user_rating, dest_rating)
    start_node.f = start_node.g + start_node.h

    heapq.heappush(to_be_visited, start_node)

    while to_be_visited:
        current = heapq.heappop(to_be_visited)
        # print(visited)
        if current.username in visited:
            print("duplicat found!!")
            break

        else:
            visited.add(current.username)
        
        print(current)
        if current.username.lower() == dest_username:
            open_path(current)
            print("path found!")
            return True
        
        info = get_player_info(current.username)
        if info["status"] in ["closed:fair_play_violations","closed"]:
            print("\t^ cheater or speedrun account (ignored)")
            continue

        visited.add(current.username)
        
        neighbors = get_valid_neighbors(current.username, start_date)
        neighbors.sort(reverse=True)
        for neighbor in neighbors:
            if neighbor[1] in visited:
                continue
            
            neighbor_node = PlayerNode(neighbor[1], neighbor[0], neighbor[2])
            neighbor_node.parent = current
            neighbor_node.g = current.g+1
            neighbor_node.h = get_heuristic(neighbor_node.rating, dest_rating)
            neighbor_node.f = neighbor_node.g+neighbor_node.h
            if neighbor_node.username not in visited:
                heapq.heappush(to_be_visited, neighbor_node)

    print("No path found")

    
def main():
    user_username = USER.lower()
    dest_username = DESTINATION.lower()
    
    start_date = (START_YEAR, START_MONTH)
    find_path(user_username, dest_username, start_date)

main()