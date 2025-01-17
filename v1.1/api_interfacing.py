import requests

def make_request(url):
    # print(f"making request: {url}")
    headers = {"User-Agent": "BTM1.1 (jonasbartels8@gmail.com)"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def get_games_since_date(player, start_date):
    # print(f"retrieving games for {player}")
    all_games = []
    existing_archives = make_request(f"https://api.chess.com/pub/player/{player}/games/archives")["archives"]

    for url in existing_archives:
        if start_date <= tuple(url.split("/")[-2:]):
            all_games += make_request(url)["games"]

    # print(f"found {len(all_games)} games")
    return all_games

def get_player_info(username):
    data = make_request(f"https://api.chess.com/pub/player/{username}")
    return data

def get_player_stats(username):
    data = make_request(f"https://api.chess.com/pub/player/{username}/stats")
    return data



