import unittest,random
from typing import List

from const import Const
from game import Game,_goatPlacements
from move import Move


class GameTest(unittest.TestCase):
    def testGoatStaticPlacements(self):
#        game = Game()
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                msg="at ("+str(row) + "," + str(col) + ")"
                moves=Game.GOAT_PLACEMENTS[(row,col)]
                self.assertEqual(len(moves), 1, msg)
                for move in moves:
                    self.assertEqual(move.mark,Const.MARK_GOAT,msg)
                    self.assertTrue(move.placement,msg)
    def testGoatDynamicPlacements(self):
        game = Game()
        moves = game.goatPlacements()
        self.assertEqual(len(moves), Const.ROWS*Const.COLS-4)
        for move in moves:
            self.assertEqual(move.mark,Const.MARK_GOAT)
            self.assertTrue(move.placement)

    def testTigerMove(self):
        game = Game()
        moves = game.tigerMoves()
        self.assertEqual(len(moves),12)

    def testGoatMove(self):
        game = Game()
        moves = game.goatMoves()
        self.assertEqual(len(moves),Const.ROWS*Const.COLS-4)

    def test4Moves(self):
        game = Game()
        self.assertFalse(game.over)
        for turns in range(8):
            moves = game.moves
            firstMove = moves[0]
            game.play(firstMove)
            self.assertFalse(game.over)

    def testCountPlacementMoves(self):
        game = Game()
        placements = 0
        while True:
            moves = game.goatMoves()
            move0=moves[0]
            if not move0.placement:
                break
            placements += 1
            game.play(move0)
            moves = game.tigerMoves()
            move0 = moves[0]
            game.play(move0)
        self.assertEqual(placements,Const.GOAT_PLACEMENTS)
        

if __name__ == '__main__':
    unittest.main()
