class Game:
    def __init__(self, tup):
        self.white_username = tup[3]
        self.white_rating = tup[4]
        self.white_result = tup[5]
        self.black_username = tup[6]
        self.black_rating = tup[7]
        self.black_result = tup[8]
        self.time_control = tup[9]
        self.url = tup[12]

    def source_opp(self, username):
        w_tup = (self.white_username, self.white_rating, self.white_result)
        b_tup = (self.black_username, self.black_rating, self.black_result)
        if username == self.white_username:
            return w_tup, b_tup
        return b_tup, w_tup
