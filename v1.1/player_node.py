
class PlayerNode:
    username: str
    ratings: float
    parent_game: str
    
    def __init__(self, username, parent, parent_game, winning):
        self.visited = False
        self.winning = winning
        self.username = username
        self.g_rating = 0
        self.ratings = {
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
        self.parent = parent
        self.missing_link = None
        self.steps_taken: int = 0
        self.heuristic: float = 0
        self.total_cost = float('inf')
        
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

        self.g_rating = sum(rates)/len(rates)
        self.lock = True

    def update_general(self):
        div, num = 0, 0
        for r_type, count in self.rating_counts.items():
            div += count
            num += self.ratings[r_type] * count
        self.g_rating = num/div

    def update_ratings(self, rating, rating_type):
        if not self.lock:
            b = (self.ratings[rating_type] * self.rating_counts[rating_type] + rating)
            self.rating_counts[rating_type] += 1
            self.ratings[rating_type] = b/self.rating_counts[rating_type]
            self.update_general()

    def __lt__(self, other):
        return self.total_cost < other.total_cost
    
    def get_rating_string(self, short):
        return f"{self.g_rating:.1f}"
    
    def assign_parent(self, node):
        if self.parent == None:
            self.parent = node
    
    def get_parent(self):
        try:
            return self.parent.username
        except:
            return None
        
    def chain_rep(self):
        if self.parent == None:
            return self.username
        if self.winning:
            return f"{self.parent.chain_rep()} > {self.username}"
        return f"{self.username} > {self.parent.chain_rep()}"
 
    def __repr__(self):
        return (f"<{self.username}, "  
                f"{self.get_rating_string(short = True)}, "
                f"{'winning' if self.winning else 'losing'}, "
                f"{self.total_cost:.3f}, "
                f"{self.get_parent()}>")
    