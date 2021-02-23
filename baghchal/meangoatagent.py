from typing import List, Tuple, Optional
from agent import Agent
from game import Game
from const import Const
from move import Move
import random

class MeanGoatAgent(Agent):
    def __init__(self,game : Game, side : int):
        super(ShyGoatAgent, self).__init__(game,side)
        if side != Const.MARK_GOAT:
            raise ValueError("side must be goat")

    def isCloseToGoat(self,row : int, col : int):
        game : Game = self.game
        board : List[List[int]] = game.board
        for (dRow,dCol) in Const.DIRS[(row,col)]:
            if board[row+dRow][col+dCol] == Const.MARK_GOAT:
                return True
        return False

    def isCloseToTiger(self,row : int, col : int):
        game : Game = self.game
        board : List[List[int]] = game.board
        for (dRow,dCol) in Const.DIRS[(row,col)]:
            if board[row+dRow][col+dCol] == Const.MARK_TIGER:
                return True
        return False
    def bigPlays(self, row : int, col : int):
        game = Game = self.game
        board : List[List[int]] = game.board
        for (dRow, dCol) in Const.DIRS[(row,col)]:
            if board[row + dRow][col+dCol] == game.over:
                return True

    def propose(self) -> Move:
        closeToGoatMoves : List[Move] = []
        notCloseToTigerMoves : List[Move] =  []
        bigPlaysMove : List[Move] = []
        moves = self.game.goatMoves()
        for move in moves:
            if self.bigPlays(move.toRow, move.toCol):
                bigPlaysMove.append(move)
            if self.isCloseToGoat(move.toRow, move.toCol):
                closeToGoatMoves.append(move)
            if self.isCloseToGoat(move.toRow, move.toCol) and not self.isCloseToTiger(move.toRow, move.toCol):
                notCloseToTigerMoves.append(move)  
            if not self.isCloseToTiger(move.toRow,move.toCol):
                notCloseToTigerMoves.append(move)
        if len(notCloseToTigerMoves) > 0:
            return random.choice(notCloseToTigerMoves)
        if (len(moves) == 0):
            print(self.game)
        return random.choice(moves)
