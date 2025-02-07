class Game:
    def __init__(self, tup):
        self.white_username = tup[1]
        self.white_rating = tup[2]
        self.white_result = tup[3]
        self.black_username = tup[4]
        self.black_rating = tup[5]
        self.black_result = tup[6]
        self.time_control = tup[7]
        self.url = tup[8]