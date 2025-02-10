import requests

def make_api_request(url):
    headers = {"User-Agent": "BM0.4 (jonasbartels8@gmail.com)"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"\tRequest: {url}")
        return None

def get_month_games(username, date):
    year = date[0]
    month = str(date[1]).zfill(2)
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    result = make_api_request(url)
    if result is None:
        return None
    return result["games"]

def get_player_start_date(username):
    return tuple(make_api_request(f"https://api.chess.com/pub/player/{username}/games/archives")["archives"][0].split("/")[-2:])

def get_player_closed(username):
    return make_api_request(f"https://api.chess.com/pub/player/{username}")["status"] in ["closed:fair_play_violations","closed"]

def get_player_info(username):
    return make_api_request(f"https://api.chess.com/pub/player/{username}")

def get_player_stats(username):
    return make_api_request(f"https://api.chess.com/pub/player/{username}/stats")



