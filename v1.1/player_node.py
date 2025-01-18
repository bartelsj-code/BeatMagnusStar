
class PlayerNode:
    username: str
    ratings: float
    parent_game: str
    
    def __init__(self, username, parent_game):
        self.username = username
        self.ratings = {
                        "general": 0, 
                        "bullet": 0, 
                        "blitz": 0, 
                        "rapid": 0, 
                        "daily": 0
                        }
        self.rating_counts = {
                        "bullet": 0, 
                        "blitz": 0, 
                        "rapid": 0, 
                        "daily": 0
                        }
        self.lock = False
        self.parent_game = parent_game
        self.parent = None
        self.g = float('inf')
        self.h: float = 0
        self.f = float('inf')
        
    def set_real_ratings(self, stats_json):
        for key in self.rating_counts:
            try:
                self.ratings[key] = stats_json[f'chess_{key}']['last']['rating']
            except:
                pass

        rates = []
        for k, v in self.ratings.items():
            if v != 0:
                rates.append(v)

        self.ratings['general'] = sum(rates)/len(rates)
        self.lock = True

    def update_general(self):
        div, num = 0, 0
        for r_type, count in self.rating_counts.items():
            div += count
            num += self.ratings[r_type] * count
        self.ratings['general'] = num/div

    def update_ratings(self, rating, rating_type):
        if not self.lock:
            b = (self.ratings[rating_type] * self.rating_counts[rating_type] + rating)
            self.rating_counts[rating_type] += 1
            self.ratings[rating_type] = b/self.rating_counts[rating_type]
            self.update_general()

    def __lt__(self, other):
        return self.f < other.f
    
    def get_rating_string(self, short):
        if short:
            return f"{self.ratings['general']:.2f}"
        
        r_string = "["
        for t, v in self.ratings.items():
            r_string += f"{t}: {v:.2f}, "

        return r_string[:-2] + "]"
    
    def __repr__(self):
        return f"<{self.username}, {self.get_rating_string(short = False)}>"
    