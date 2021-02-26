from randomagent import RandomAgent
from agent import Agent
from game import Game
from const import Const
from move import Move
from typing import Optional, List, Tuple
import random

class MetaAgent(Agent):
    def __init__(self,game : Game, side : int):
        super(MetaAgent, self).__init__(game,side)
        self._goat : Agent = RandomAgent(game,Const.MARK_GOAT)
        self._tiger : Agent = RandomAgent(game,Const.MARK_TIGER)
        self._maxDepth = 2

    @property
    def maxDepth(self):
        return self._maxDepth

    @maxDepth.setter
    def maxDepth(self,value):
        self._maxDepth=value

    @property
    def goat(self):
        return self._goat
    @goat.setter
    def goat(self,value):
        self._goat = value
        self._goat.game = self._game

    @property
    def tiger(self):
        return self._tiger
    @tiger.setter
    def tiger(self,value):
        self._tiger = value
        self._tiger.game = self._game
    @property
    def game(self) -> Game:
        return self._game

    @game.setter
    def game(self,value) -> None:
        self._game = value
        self._goat.game = value
        self._tiger.game = value


    def heuristic(self):
        moves : List[Move] = []
        turns = 1
        while not self.game.over:
            turns += 1
            if self.game.state == Const.STATE_TURN_GOAT:
                move=self.goat.propose()
                moves.append(move)
                self.game.play(move)
            else:
                move=self.tiger.propose()
                moves.append(move)
                self.game.play(move)
        value = self.value() // turns
        while len(moves) > 0:
            move = moves.pop()
            self.game.unplay(move)
        return value

    def value(self, depth : int = 0)-> int:
        if self.game.over:
            if self.side == Const.MARK_GOAT:
                if self.state == Const.STATE_WIN_GOAT:
                    return 1_000_000_000
                elif self.state == Const.STATE_DRAW:
                    return 0
                else:
                    return -1_000_000_000
            else:
                if self.state == Const.STATE_WIN_TIGER:
                    return 1_000_000_000
                elif self.state == Const.STATE_DRAW:
                    return 0
                else:
                    return -1_000_000_000
        else:
            if depth >= self._maxDepth:
                return self.heuristic()
            moves=self.game.moves
            bestValue=None
            for move in moves:
                self.game.play(move)
                moveValue = self.value(depth+1)
                self.game.unplay(move)
                if self.onside():
                    if bestValue == None or bestValue < moveValue:
                        bestValue = moveValue
                else:
                    if bestValue == None or bestValue > moveValue:
                        bestValue = moveValue
            if bestValue == None:
                raise RuntimeError("game state error")
            else:
                return bestValue    


    def onside(self) -> bool:
        if self.game.state == Const.STATE_TURN_GOAT and self.game.side == Const.MARK_GOAT:
            return True
        if self.game.state == Const.STATE_TURN_TIGER and self.game.side == Const.MARK_TIGER:
            return True
        return False

    def propose(self) -> Move:
            moves=self.game.moves
            bestValue=None
            bestMoves=[]
            for move in moves:
                self.game.play(move)
                moveValue = self.value(depth+1)
                self.game.unplay(move)
                if self.onside():
                    if bestValue == None or bestValue < moveValue:
                        bestValue = moveValue
                        bestMoves = [move]
                    elif bestValue == moveValue:
                        bestMoves.append(move)
                else:
                    if bestValue == None or bestValue > moveValue:
                        bestValue = moveValue
                        bestMoves = [move]
                    elif bestValue == moveValue:
                        bestMoves.append(move)
            return random.choice(bestMoves)
