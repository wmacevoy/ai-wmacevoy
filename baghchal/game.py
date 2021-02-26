from typing import Dict,Set,List, Tuple, Optional
from const import Const
from move import Move


def _goatPlacements() -> Dict[Tuple[int,int],List[Move]]:
    allMoves : Dict[Tuple[int,int],List[Move]] = {}
    for row in range(Const.ROWS):
        for col in range(Const.COLS):
            atMoves : List[Move] = []
            move = Move(Const.MARK_GOAT,row,col,row,col)
            atMoves.append(move)
            allMoves[(row,col)]=atMoves
    return allMoves

def _goatMovements() -> Dict[Tuple[int,int],List[Move]]:
    allMoves : Dict[Tuple[int,int],List[Move]] = {}
    for row in range(Const.ROWS):
        for col in range(Const.COLS):
            atMoves : List[Move] = []
            for (dRow,dCol) in Const.DIRS[(row,col)]:
                move = Move(Const.MARK_GOAT,row,col,row+dRow,col+dCol)
                atMoves.append(move)
            allMoves[(row,col)]=atMoves
    return allMoves

def _tigerMovements() -> Dict[Tuple[int,int],List[Move]]:
    allMoves : Dict[Tuple[int,int],List[Move]] = {}
    for row in range(Const.ROWS):
        for col in range(Const.COLS):
            atMoves : List[Move] = []
            for (dRow,dCol) in Const.DIRS[(row,col)]:
                move = Move(Const.MARK_TIGER,row,col,row+dRow,col+dCol)
                atMoves.append(move)
            allMoves[(row,col)]=atMoves
    return allMoves

def _tigerCaptures() -> Dict[Tuple[int,int],List[Move]]:
    allMoves : Dict[Tuple[int,int],List[Move]] = {}
    for row in range(Const.ROWS):
        for col in range(Const.COLS):
            atMoves : List[Move] = []
            for (dRow,dCol) in Const.DIRS[(row,col)]:
                toRow = row + 2*dRow
                toCol = col + 2*dCol
                if 0 <= toRow and toRow < Const.ROWS and 0 <= toCol and toCol < Const.COLS:
                    move = Move(Const.MARK_TIGER,row,col,toRow,toCol)
                    atMoves.append(move)
            allMoves[(row,col)]=atMoves
    return allMoves

class Game:
    def __init__(self):
        self.reset()


    GOAT_PLACEMENTS : Dict[Tuple[int,int],List[Move]] = _goatPlacements()
    GOAT_MOVEMENTS : Dict[Tuple[int,int],List[Move]] = _goatMovements()
    TIGER_MOVEMENTS : Dict[Tuple[int,int],List[Move]] = _tigerMovements()
    TIGER_CAPTURES : Dict[Tuple[int,int],List[Move]] = _tigerCaptures()


    def reset(self):
        self._board : List[List[int]] = [[Const.MARK_NONE for col in range(Const.COLS)] for row in range(Const.ROWS)]
        self._board[0][0] = Const.MARK_TIGER
        self._board[Const.ROWS-1][0] = Const.MARK_TIGER
        self._board[0][Const.COLS-1] = Const.MARK_TIGER
        self._board[Const.ROWS-1][Const.COLS-1] = Const.MARK_TIGER
        self._state : int = Const.STATE_TURN_GOAT
        self._turns : int = 0
        self._captureTurns : List[int] = [0]
        self._placed : int = 0 # number of goats placed
        self._captured : int = 0 # number of goats captured    

    @property
    def over(self) -> bool:
        return \
            self._state == Const.STATE_WIN_GOAT or \
            self._state == Const.STATE_WIN_TIGER or \
            self._state == Const.STATE_DRAW

    def moveOk(self,move : Move) -> None:
        if self._board[move.toRow][move.toCol] != Const.MARK_NONE:
            raise ValueError("destination (to) is occupied") 
        if not move.placement and self._board[move.fromRow][move.fromCol] != move.mark:
            raise ValueError("source (from) is not player")
        if move.capture:
            if self._board[move.capRow][move.capCol] != Const.MARK_GOAT:
                raise ValueError("capture move without goat")

    def movements(self, fromRow : int, fromCol : int, dist : int = 1) -> List[Move]:
        mark : int = self._board[fromRow][fromCol]
        moves : List[Move] = []
        for (dRow,dCol) in Const.DIRS[(fromRow,fromCol)]:
            toRow : int = fromRow+dist*dRow
            toCol : int = fromCol+dist*dCol
            try:
                move=Move(mark,fromRow,fromCol,toRow,toCol)
                self.moveOk(move)
                moves.append(move)
            except ValueError:
                pass
        return moves


    def goatPlacements(self) -> List[Move]:
        moves : List[Move] = []
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                if self._board[row][col] == Const.MARK_NONE:
                    placements = self.GOAT_PLACEMENTS[(row,col)]
                    moves.extend(placements)
        return moves

    def goatMovements(self) -> List[Move]:
        moves : List[Move] = []
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                if self._board[row][col] == Const.MARK_GOAT:
                    for movement in self.GOAT_MOVEMENTS[(row,col)]:
                        if self._board[movement.toRow][movement.toCol] == Const.MARK_NONE:
                            moves.append(movement)
        return moves

    def anyGoatMoves(self) -> bool:
        if self._placed < Const.GOAT_PLACEMENTS:
            return True
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                if self._board[row][col] == Const.MARK_GOAT:
                    for movement in self.GOAT_MOVEMENTS[(row,col)]:
                        if self._board[movement.toRow][movement.toCol] == Const.MARK_NONE:
                            return True
        return False
            
    def anyTigerMoves(self) -> bool:
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                if self._board[row][col] == Const.MARK_TIGER:
                    for movement in self.TIGER_MOVEMENTS[(row,col)]:
                        if self._board[movement.toRow][movement.toCol] == Const.MARK_NONE:
                            return True
                    for capture in self.TIGER_CAPTURES[(row,col)]:
                        if self._board[capture.toRow][capture.toCol] == Const.MARK_NONE:
                            if self._board[capture.capRow][capture.capCol] == Const.MARK_GOAT:
                                return True
        return False

    def tigerMoves(self) -> List[Move]:
        moves : List[Move] = []
        for row in range(Const.ROWS):
            for col in range(Const.COLS):
                if self._board[row][col] == Const.MARK_TIGER:
                    for movement in self.TIGER_MOVEMENTS[(row,col)]:
                        if self._board[movement.toRow][movement.toCol] == Const.MARK_NONE:
                            moves.append(movement)
                    for capture in self.TIGER_CAPTURES[(row,col)]:
                        if self._board[capture.toRow][capture.toCol] == Const.MARK_NONE:
                            if self._board[capture.capRow][capture.capCol] == Const.MARK_GOAT:
                                moves.append(capture)
        return moves

    def goatMoves(self) -> List[Move]:
        if self._placed < Const.GOAT_PLACEMENTS:
            return self.goatPlacements()
        else:
            return self.goatMovements()

    @property
    def moves(self) -> List[Move]:
        if self._state == Const.STATE_TURN_GOAT:
            return self.goatMoves()
        if self._state == Const.STATE_TURN_TIGER:
            return self.tigerMoves()
        return []

    def play(self,move : Move):
        if self.over:
            raise RuntimeError("move after game is over")
        if move.goat:
            if self._state != Const.STATE_TURN_GOAT:
                raise ValueError("it is not goat's turn")
        else:
            if self._state != Const.STATE_TURN_TIGER:
                raise ValueError("it is not tiger's turn")
        self.moveOk(move)
        self._turns = self._turns + 1
        self._board[move.fromRow][move.fromCol]=Const.MARK_NONE
        self._board[move.toRow][move.toCol]=move.mark
        if move.placement:
            self._placed += 1
        elif move.capture:
            capRow=(move.fromRow+move.toRow)//2
            capCol=(move.fromCol+move.toCol)//2
            self._board[capRow][capCol]=Const.MARK_NONE
            self._captured += 1
            if self._captured >= Const.GOAT_CAPTURES_FOR_TIGER_WIN:
                self._state = Const.STATE_WIN_TIGER
            self._captureTurns.append(self._turns)
        if self._state == Const.STATE_TURN_GOAT:
            if not self.anyTigerMoves():
                self._state = Const.STATE_WIN_GOAT
            else:
                self._state = Const.STATE_TURN_TIGER
        elif self._state == Const.STATE_TURN_TIGER:
            self._state = Const.STATE_TURN_GOAT
        if self._turns - self._captureTurns[-1] > Const.MAX_MOVES_WITHOUT_CAPTURE:
            self._state = Const.STATE_DRAW
        if self._state == Const.STATE_TURN_GOAT:
            if not self.anyGoatMoves():
                self._state = Const.STATE_DRAW

    def unplay(self, move : Move):
        self._turns = self._turns - 1
        self._state = Const.STATE_TURN_GOAT if (self._turns % 2 == 0) else Const.STATE_TURN_TIGER
        if move.placement:
            self._board[move.toRow][move.toCol] = Const.MARK_NONE
            self._placed -= 1
        else:
            self._board[move.fromRow][move.fromCol] = move.mark
            self._board[move.toRow][move.toCol] = Const.MARK_NONE
        if move.capture:
            capRow=(move.fromRow+move.toRow)//2
            capCol=(move.fromCol+move.toCol)//2
            self._board[capRow][capCol] = Const.MARK_GOAT
            self._captured = self._captured - 1
            self._captureTurns.pop()

    @property
    def board(self) -> List[List[int]]:
        return [[self._board[row][col]  for col in range(Const.COLS)] for row in range(Const.ROWS)]
        
    @property
    def state(self) -> int:
        return self._state
    
    def playCommands(self,commands : str) -> None:
        for command in commands.split():
            self.play(Move.parse(command))

    def __str__(self) -> str:
        ans = "\n"
        ans = ans + "turn " + str(self._turns) + "(" + Const.stateStr(self.state) + "):\n"
        for row in range(Const.ROWS):
            s=""
            for col in range(Const.COLS):
                s=s+Const.markStr(self._board[row][col])
            ans = ans + s + "\n"
        
        return ans

    def copyTo(self,target : 'Game') -> None:
        target._board = [[self._board[row][col] for col in range(Const.COLS)] for row in range(Const.ROWS)]
        target._state = self._state
        target._turns = self._turns
        target._captured = self._captured
        target._captureTurns = self._captureTurns.copy()
        target._placed = self._placed

    def clone(self) -> 'Game':
        ans = Game()
        self.copyTo(ans)
        return ans
