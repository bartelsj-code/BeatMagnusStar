import typing

class PlayerNode:
    username: str
    ratings: float
    game: str
    
    def __init__(self, username, parent, game_url, winning):
        self.visited = False
        self.winning = winning
        self.username = username
        self.types = ["bullet", "blitz", "rapid", "daily"]
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
        self.game_url = game_url
        self.parent: PlayerNode = parent
        self.missing_link = None
        self.steps_taken = float('inf')
        self.heuristic = float('inf')
        self.total_cost = float('inf')
        self.comp_rating = 0

    def set_comp_rating(self):
        count = 0
        total = 0
        for t in self.types:
            total += self.ratings[t] * self.rating_counts[t]
            count += self.rating_counts[t]
        self.comp_rating = total/count

    def get_distance(self, other_node):
        pass

    def set_cost(self):
        self.total_cost = self.heuristic+self.steps_taken

    def update_ratings(self, rating, rating_type):
        b = (self.ratings[rating_type] * self.rating_counts[rating_type] + rating)
        self.rating_counts[rating_type] += 1
        self.ratings[rating_type] = b/self.rating_counts[rating_type]

    def assign_parent(self, node):
        #
        if self.parent == None:
            self.parent = node
    
    def chain_rep(self):
        # visualization of explored path
        if self.parent == None:
            return self.username
        if self.winning:
            return f"{self.parent.chain_rep()} > {self.username}"
        return f"{self.username} > {self.parent.chain_rep()}"
    
    def __lt__(self, other):
        return self.total_cost <= other.total_cost
    
    def __hash__(self):
        return hash(self.username)
 
    def __repr__(self):
        return (
                "<"

                f"{self.steps_taken}, "
                f"{self.total_cost:.1f}, "
                f"{self.username}, "  
                f"{'W' if self.winning else 'L'}, "
                f"{self.comp_rating:.2f}"
                
                ">"
                
                )
    