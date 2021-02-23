from typing import List, Tuple, Optional
from agent import Agent
from game import Game
from const import Const
from move import Move
import random

class EdgeCenterGoatAgent(Agent):
    def __init__(self,game : Game, side : int):
        super(EdgeCenterGoatAgent, self).__init__(game,side)
        if side != Const.MARK_GOAT:
            raise ValueError("side must be goat")
    
    def isEdgeCenterOpen(self, row, col):
        game = self.game
        board = game.board
        move = [row,col]

        if move == [0,2] or move == [2,0] or move == [2,4] or move == [4,2]:
            if board[row][col] == Const.MARK_NONE:
                return True
        elif move == [0,0] or move == [0,4] or move == [4,0] or move == [4,4] or move == [2,2]:
            if board[row][col] == Const.MARK_NONE:
                return True
        else:        
            return False
    
    def isCloseToTiger(self,row : int, col : int):
        game : Game = self.game
        board : List[List[int]] = game.board
        for (dRow,dCol) in Const.DIRS[(row,col)]:
            if board[row+dRow][col+dCol] == Const.MARK_TIGER:
                return True
        return False

    def propose(self) -> Move:
        notCloseToTigerMoves : List[Move] =  []
        edgeMoves : List[Move] = []
        moves = self.game.goatMoves()
        for move in moves:
            if self.isEdgeCenterOpen(move.toRow,move.toCol):
                edgeMoves.append(move)
            if not self.isCloseToTiger(move.toRow,move.toCol):
                notCloseToTigerMoves.append(move)
        if len(edgeMoves) > 0:
            return edgeMoves[0]
        if len(notCloseToTigerMoves) > 0:
            return random.choice(notCloseToTigerMoves)
        if (len(moves) == 0):
            print(self.game)
        return random.choice(moves)
