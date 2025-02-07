import requests

import json



def make_api_request(url):
    # print(f"making request: {url}")
    
    headers = {"User-Agent": "BM0.4 (jonasbartels8@gmail.com)"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"\tFailed to fetch data. Status code: {response.status_code}")
        print(f"\tRequest: {url}")
        return None

    
def game_json_to_tup(game_json, year, month):

    white_json = game_json["white"]
    w_player = white_json["username"]
    w_rating = white_json["rating"]
    w_result = white_json["result"]

    black_json = game_json["black"]
    b_player = black_json["username"]
    b_rating = black_json["rating"]
    b_result = black_json["result"]

    time_control = game_json["time_class"]


    pass

def games_to_tups(games_json, year, month):
    tups = []
    for game in games_json:
        tup = game_json_to_tup(game)
        tups.append(tup)
    print(tups)

# def get_player_start_date()


def get_games_since_date(player, start_date):
    
    #if already seen, grab avaliable data. if data was updated earlier than 2 hours ago, update most recent month of data

    
    #if not already seen, grab avaliable 
    
    all_games = []
    tups = []
    print(start_date)

    for url in make_api_request(f"https://api.chess.com/pub/player/{player}/games/archives")["archives"]:
        
        # print(url)
        if start_date <= tuple(url.split("/")[-2:]):
            archive_json = make_api_request(url)
            if archive_json == None:
                continue
            else:
                all_games += archive_json["games"]
                tups += games_to_tups(archive_json["games"])

    print(tups)
    # print(f"collected {player} games ({len(all_games)})")
    return all_games

def get_player_start_date(username):
    date = tuple(make_api_request(f"https://api.chess.com/pub/player/{username}/games/archives")["archives"][0].split("/")[-2:])
    return date

def get_player_closed(username):
    if make_api_request(f"https://api.chess.com/pub/player/{username}")["status"] in ["closed:fair_play_violations","closed"]:
        return True
    return False


def get_player_info(username):
    data = make_api_request(f"https://api.chess.com/pub/player/{username}")
    return data

def get_player_stats(username):
    data = make_api_request(f"https://api.chess.com/pub/player/{username}/stats")
    return data



