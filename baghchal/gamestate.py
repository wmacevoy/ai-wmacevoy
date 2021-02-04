from typing import Tuple
from const import Const
from game import Game

class GameState:
    def __init__(self,game : Game):
        board : int = 0
        if Const.ROWS != Const.COLS:
            board0 : int = 0
            board1 : int = 0
            board2 : int = 0
            board3 : int = 0

            for row in range(Const.ROWS):
                for col in range(Const.COLS):
                    board0 = 3*board0 + game.board[row][col]
                    board1 = 3*board1 + game.board[Const.ROWS-1-row][col]
                    board2 = 3*board2 + game.board[row][Const.COLS-1-col]
                    board3 = 3*board3 + game.board[Const.ROWS-1-row][Const.COLS-1-col]
            board = min(board0,board1,board2,board3)
        else:
            board0 : int = 0
            board1 : int = 0
            board2 : int = 0
            board3 : int = 0
            board0d : int = 0
            board1d : int = 0
            board2d : int = 0
            board3d : int = 0

            # there's an off-diagonal symmetry I did not implement,
            # which would have made 16 equivalent boards...
            for row in range(Const.ROWS):
                for col in range(Const.COLS):
                    board0 = 3*board0 + game.board[row][col]
                    board1 = 3*board1 + game.board[Const.ROWS-1-row][col]
                    board2 = 3*board2 + game.board[row][Const.COLS-1-col]
                    board3 = 3*board3 + game.board[Const.ROWS-1-row][Const.COLS-1-col]
                    board0d = 3*board0 + game.board[col][row]
                    board1d = 3*board1 + game.board[col][Const.ROWS-1-row]
                    board2d = 3*board2 + game.board[Const.COLS-1-col][row]
                    board3d = 3*board3 + game.board[Const.COLS-1-col][Const.ROWS-1-row]
            board = min(board0,board1,board2,board3,board0d,board1d,board2d,board3d)

        self._tuple : Tuple[int,int,int,int] = (board,game._placed, game._captured, game._state)
        self._hash = hash(self._tuple)

    def __eq__(self,to : 'GameState') -> bool:
        return self._tuple == to._tuple
    def __ne__(self,to : 'GameState') -> bool:
        return self._tuple != to._tuple
    def __lt__(self,to : 'GameState') -> bool:
        return self._tuple < to._tuple
    def __le__(self,to : 'GameState') -> bool:
        return self._tuple <= to._tuple
    def __gt__(self,to : 'GameState') -> bool:
        return self._tuple > to._tuple
    def __ge__(self,to : 'GameState') -> bool:
        return self._tuple >= to._tuple
    def __hash__(self) -> int:
        return self._hash
