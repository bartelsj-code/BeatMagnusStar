import heapq

class MultiQueue:
    def __init__(self):
        self.total_length = 0
        self.winner_queue = []
        self.loser_queue = []

    def pop(self):
        if not self:
            print("tried to pop from empty queue")
        if not self.winner_queue:
            return heapq.heappop(self.loser_queue)
        if not self.loser_queue or self.winner_queue[0] < self.loser_queue[0]:
            return heapq.heappop(self.winner_queue)
        return heapq.heappop(self.loser_queue)
    
    def push(self, node, is_winner = True):
        if is_winner:
            heapq.heappush(self.winner_queue, node)
        else:
            heapq.heappush(self.loser_queue, node)

    def __bool__(self):
        return self.total_length > 0
    
    def __repr__(self):
        return f"MultiQueue\n<win: {self.winner_queue}>\n<los: {self.loser_queue}>"