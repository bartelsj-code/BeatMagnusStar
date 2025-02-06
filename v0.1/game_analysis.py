from control_variables import ABANDONMENT_CUTOFF, GAME_ATTRIBUTES, TIME_CONTROLS

def get_move_count(pgn_string):
    return len(pgn_string.split("..."))-1

def analyze_game(game, player_name):
    fast_conditions = GAME_ATTRIBUTES
    game_link = game["url"]
    
    user, opponent, is_white = (game["black"], game["white"], False) if game["white"]["username"].lower() != player_name else (game["white"], game["black"], True)

    for condition in fast_conditions:
        if game[condition] != fast_conditions[condition]:
            # print(f"game removed because: {condition} was {game[condition]}, not {fast_conditions[condition]}")
            return False, None, None
        
    # if game["time_class"] not in TIME_CONTROLS:
    #     return False, None


    #if user Loses
    if user["result"] != "win":
        return False, None, None

    #if user wins by opponent's abandonment of the game
    if opponent["result"] == "abandoned":
        try: 
            #if opponent was already losing...
            if game["accuracies"]["white"] - game["accuracies"]["black"] > 0:
                return is_white, opponent if is_white else None, game_link

        except:
            #...or the game lasted longer than 5 moves, count the game.
            if get_move_count(game["pgn"]) <= ABANDONMENT_CUTOFF:
                return False, None, None        

    return True, opponent, game_link