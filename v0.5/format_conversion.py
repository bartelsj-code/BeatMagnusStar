from game import Game


def game_json_to_tup(game_json, date):

    white_json = game_json["white"]
    w_username = white_json["username"].lower()
    w_rating = white_json["rating"]
    w_result = white_json["result"]

    black_json = game_json["black"]
    b_username = black_json["username"].lower()
    b_rating = black_json["rating"]
    b_result = black_json["result"]

    time_control = game_json["time_class"]

    url = game_json["url"]

    tup = (
        w_username,
        w_rating,
        w_result,
        b_username,
        b_rating,
        b_result,
        time_control,
        date[0],
        date[1],
        url
    )

    return tup

def tup_to_game(tup):
    return Game(tup)
    