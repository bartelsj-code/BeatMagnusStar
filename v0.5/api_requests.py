import requests

def make_api_request(url):
    headers = {"User-Agent": "BM0.4 (jonasbartels8@gmail.com)"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"\tFailed to fetch data. Status code: {response.status_code}")
        print(f"\tRequest: {url}")
        return None

def get_month_games(username, date):
    year = date[0]
    month = str(date[1]).zfill(2)
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    return make_api_request(url)["games"]

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



