from control_variables import *

def fits_format(game):
    for condition in GAME_ATTRIBUTES:
        if not game[condition] in GAME_ATTRIBUTES[condition]:
            return False
    return True

def is_useless_abandonment(o_json):
    #currently eliminates all abandoned games. this will be changed 
    if o_json["result"] == "abandoned":
        return True
    return False

def get_move_count(pgn_string):
    return len(pgn_string.split("..."))-1

def game_filter(game, source_username, wins = True):
    '''Determines whether a game can be used for path.
    
    Returns:
        tuple(Bool for usabilty, json_dict of opponent, url of game)
    '''
    source_json, opponent_json, is_white = (
        (game["black"], game["white"], False)
        if game["white"]["username"].lower() != source_username 
        else (game["white"], game["black"], True)
    )
    
    if (
        not fits_format(game)
        or (source_json["result"] if wins else opponent_json["result"]) != "win"
        or is_useless_abandonment(opponent_json)
    ):
        return False, None, None
    return True, source_json, opponent_json

    
    
