from typing import List, Tuple, Optional
from agent import Agent
from game import Game
from const import Const
from move import Move
import random

class ShySideGoatAgent(Agent):
    def __init__(self,game : Game, side : int):
        super(ShySideGoatAgent, self).__init__(game,side)
        if side != Const.MARK_GOAT:
            raise ValueError("side must be goat")
    def isCloseToTiger(self,row : int, col : int):
        game : Game = self.game
        board : List[List[int]] = game.board
        for (dRow,dCol) in Const.DIRS[(row,col)]:
            if board[row+dRow][col+dCol] == Const.MARK_TIGER:
                return True
        return False

    #pulled from safegoatagent.py
    def isWin(self, move : Move) -> bool:
        game : Game = self.game
        game.play(move)
        rval : bool = game.state == Const.STATE_WIN_GOAT or game.state == Const.STATE_DRAW
        game.unplay(move)
        return rval

    def propose(self) -> Move:
        closeToTigerMoves : List[Move] = []
        notCloseToTigerMoves : List[Move] =  []
        notCloseToTigerSideMoves : List[Move] = []
        moves = self.game.goatMoves()
        for move in moves:
            if self.isWin(move):
                return move
            if self.game.anyGoatMoves:
                if not self.isCloseToTiger(move.toRow,move.toCol):
                    if ((move.toCol == 0) or (move.toCol == 4)) and ((move.toRow == 0) or (move.toRow == 4)):
                        notCloseToTigerSideMoves.append(move)
                    else:
                        notCloseToTigerMoves.append(move)
                if len(notCloseToTigerSideMoves) > 0:
                    return random.choice(notCloseToTigerSideMoves)
                if len(notCloseToTigerMoves) > 0:
                    return random.choice(notCloseToTigerMoves)
                if (len(moves) == 0):
                    print(self.game)
                return random.choice(moves)
            else:
                if self.isCloseToTiger(move.toRow,move.toCol):
                    closeToTigerMoves.append(move)
                if len(closeToTigerMoves) > 0:
                    return random.choice(closeToTigerMoves)
                return random.choice(moves)
