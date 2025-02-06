import heapq

class MultiQueue:
    def __init__(self):
        self.total_length = 0
        self.winner_queue = []
        self.loser_queue = []

    def pop(self):
        self.total_length -= 1
        if not self.winner_queue:
            return heapq.heappop(self.loser_queue)
        if not self.loser_queue or self.winner_queue[0] < self.loser_queue[0]:
            return heapq.heappop(self.winner_queue)
        return heapq.heappop(self.loser_queue)
    
    def push(self, node):
        self.total_length += 1
        if node.winning:
            heapq.heappush(self.winner_queue, node)
        else:
            heapq.heappush(self.loser_queue, node)

    def __bool__(self):
        return self.total_length > 0
    
    def get_queue_str(self):
        w = [] if not self.winner_queue else f"{self.winner_queue[0].username}  {self.winner_queue[0].total_cost:.3f}"
        l = [] if not self.loser_queue else f"{self.loser_queue[0].username}  {self.loser_queue[0].total_cost:.3f}"
        return w,l
    
    def __repr__(self):
        w, l = self.get_queue_str()
        return f"〈 <win: {w}> Queue <los: {l}> 〉"
        return f"{self.total_length}"
        
        print(w, l)
        
    
    def __iter__(self):
        return iter(self.winner_queue + self.loser_queue)
    
    def clean(self):
        
        heapq.heapify(self.winner_queue)
        heapq.heapify(self.loser_queue)
