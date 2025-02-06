from player_node import PlayerNode

class MultiSet:
    def __init__(self):
        self.winner_set = set()
        self.loser_set = set()

    def add(self, node: PlayerNode):
        if node.winning:
            self.winner_set.add(node)
        else:
            self.loser_set.add(node)

    def __contains__(self, node):
        if node.winning:
            return node in self.winner_set
        return node in self.loser_set


    def __repr__(self):
        return f"MultiSet\n\t<win: {self.winner_set}>\n\t<los: {self.loser_set}>"
