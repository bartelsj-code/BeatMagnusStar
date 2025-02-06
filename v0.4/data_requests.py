import requests
import json

def make_request(url):
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

def get_games_since_date(player, start_date):
    all_games = []
    # print(start_date)

    for url in make_request(f"https://api.chess.com/pub/player/{player}/games/archives")["archives"]:
        
        # print(url)
        if start_date <= tuple(url.split("/")[-2:]):
            archive_json = make_request(url)
            if archive_json == None:
                continue
            else:
                all_games += archive_json["games"]
    # print(f"collected {player} games ({len(all_games)})")
    return all_games

def get_player_info(username):
    data = make_request(f"https://api.chess.com/pub/player/{username}")
    return data

def get_player_stats(username):
    data = make_request(f"https://api.chess.com/pub/player/{username}/stats")
    return data



