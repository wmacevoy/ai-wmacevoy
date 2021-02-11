from agent import Agent
from game import Game
from const import Const
from move import Move
import random

class AggressiveTigerAgent(Agent):
    def __init__(self,game : Game, side : int):
        super(AggressiveTigerAgent, self).__init__(game,side)
        if side != Const.MARK_TIGER:
            raise ValueError("side must be tiger")

    def propose(self) -> Move:
        moves = self.game.tigerMoves()
        for move in moves:
            if move.capture:
                return move
        return random.choice(moves)
