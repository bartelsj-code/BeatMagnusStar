class PlayerNode:
    username: str
    rating: float
    rating_type: str
    parent_game: str
    
    
    def __init__(self, username, rating, pg):
        self.username = username
        self.rating = rating   #dict of time controls to ratings
        self.parent_game = pg
        self.parent = None
        self.g = float('inf')
        self.h: float = 0
        self.f = float('inf')


    def __lt__(self, other):
        return self.f < other.f
    
    def __repr__(self):
        return f"<{self.username}, {self.rating}, {self.g}, {self.f}>"

