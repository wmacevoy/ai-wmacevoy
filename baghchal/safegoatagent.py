from agent import Agent
from game import Game
from const import Const
from move import Move
from typing import List
import random

# note: moves which limit tiger moves are better; figure out how to implement

class SafeGoatAgent(Agent):
    def __init__(self,game : Game, side : int, goatval : int = 1, offboardval : int = 4, tigerval : int = -5):
        super(SafeGoatAgent, self).__init__(game, side)
        if side != Const.MARK_GOAT:
            raise ValueError("goats only")
        self.OFFBOARD_VALUE = offboardval
        self.TIGER_VALUE = tigerval
        self.GOAT_VALUE = goatval

    def isWin(self, move : Move) -> bool:
        game : Game = self.game
        game.play(move)
        rval : bool = game.state == Const.STATE_WIN_GOAT or game.state == Const.STATE_DRAW
        game.unplay(move)
        return rval

    def score(self, row : int, col : int):
        game : Game = self.game
        board : List[List[Int]] = game.board
        score : int = 0

        if (row + col) % 2 == 0:
            movesAvailable : int = 8
        else:
            movesAvailable : int = 4
        # simply counts the moves which were offboard and multiples by offboard value
        score += (movesAvailable - len(Const.DIRS[(row,col)])) * self.OFFBOARD_VALUE

        for deltas in Const.DIRS[(row,col)]:
            (dRow, dCol) = deltas
            (propRow, propCol) = (row + dRow, col + dCol)
            mark = board[propRow][propCol]
            if mark == Const.MARK_GOAT:
                score += self.GOAT_VALUE
            elif mark == Const.MARK_TIGER:
                (oppDRow, oppDCol) = (dRow * -1, dCol * -1)
                (oppRow, oppCol) = (row + oppDRow, col + oppDCol)
                # checking that it's inbounds
                if oppRow > 0 and oppRow < 4 and oppCol > 0 and oppCol < 4:
                    # checking the opposite space to see if the tiger can make the jump
                    mark = board[oppRow][oppCol]
                    if mark == Const.MARK_NONE:
                        score += self.TIGER_VALUE
        return score

    def propose(self) -> Move:
        notCloseToTigerMoves : List[Move] = []
        moves = self.game.goatMoves()
        bestMoves : List[Move] = []
        bestScore : int = -50
        for move in moves:
            if self.isWin(move):
                return move
            score : int = self.score(move.toRow, move.toCol)
            if score > bestScore:
                bestScore = score
                bestMoves = [move]
            elif score == bestScore:
                bestMoves.append(move)
        if len(bestMoves) > 0:
            return random.choice(bestMoves)
        return random.choice(moves)
