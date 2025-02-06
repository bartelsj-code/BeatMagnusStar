import typing

class PlayerNode:
    username: str
    ratings: float
    game: str
    
    def __init__(self, username, parent, game, winning):
        self.visited = False
        self.winning = winning
        self.username = username
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
        self.game = game
        self.parent: PlayerNode = parent
        self.missing_link = None
        self.steps_taken = float('inf')
        self.total_cost = float('inf')

    def get_distance(self, other_node):
        pass

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
 
    def __repr__(self):
        return (
                f"<{self.username}, "  
                f"{'w' if self.winning else 'l'}>"
                )
    