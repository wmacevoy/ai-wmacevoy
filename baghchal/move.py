from typing import Tuple
from const import Const

class Move:
    '''
    Encapulates the idea of a single move for either side.
    There 4 kinds: goat placements, goat movements,
    tiger movements, and tiger captures.

    move.goat vs move.tiger --- which side
    move.placement vs move.movement vs move.capture
     --- what kind
    move.distance -- how far
    move.capRow, move.capCol the (row,col) a capture skips
      (where there should be a goat)
    '''
    @classmethod
    def ok(cls, mark : int, fromRow : int, fromCol : int, toRow : int, toCol : int):
        if mark == Const.MARK_NONE:
            raise ValueError(f"mark must be goat or tiger")
        Const.markOk(mark)
        Const.rowOk(fromRow)
        Const.colOk(fromCol)
        Const.rowOk(toRow)
        Const.colOk(toCol)
        
        dist : int = max(abs(toRow-fromRow),abs(toCol-fromCol))
        diagonal : bool = \
            (fromRow + fromCol) % 2 == 0 and \
            (toRow + toCol) % 2 == 0 and \
            (abs(fromRow-toRow) == abs(fromCol-toCol))
        straight : bool = (fromRow == toRow) or \
                (fromCol == toCol)
        if (not straight) and (not diagonal):
            raise ValueError("impossible move") 
        if mark == Const.MARK_GOAT:
            if dist > 1:
                raise ValueError("goats can only place or move 1")
        elif dist < 1 or dist > 2:
            raise ValueError("tigers can only move 1 or 2 (capture)")


    def __init__(self, mark : int, fromRow : int, fromCol : int, toRow : int, toCol : int):
        self.ok(mark,fromRow,fromCol,toRow,toCol)
        self._mark : int = mark
        self._fromRow : int = fromRow
        self._fromCol : int = fromCol
        self._toRow : int = toRow
        self._toCol : int = toCol

    @property
    def distance(self) -> int:
        return max(abs(self._toRow-self._fromRow),abs(self._toCol-self._fromCol))
    @property
    def placement(self) -> bool:
        return self.distance == 0

    @property
    def capture(self) -> bool:
         return self.distance == 2

    @property
    def goat(self) -> bool:
        return self._mark == Const.MARK_GOAT

    @property
    def tiger(self) -> bool:
        return self._mark == Const.MARK_TIGER

    @property
    def fromRow(self) -> int:
        return self._fromRow
    @property
    def fromCol(self) -> int:
        return self._fromCol
    @property
    def fromRowCol(self) -> Tuple[int,int]:
        return (self._fromRow,self._fromCol)

    @property
    def toRow(self) -> int:
        return self._toRow
    @property
    def toCol(self) -> int:
        return self._toCol
    @property
    def toRowCol(self) -> Tuple[int,int]:
        return (self._toRow,self._toCol)
    @property
    def capRow(self) -> int:
        return (self._fromRow+self._toRow)//2
    @property
    def capCol(self) -> int:
        return (self._fromCol+self._toCol)//2
    @property
    def capRowCol(self) -> Tuple[int,int]:
        return ((self._fromRow+self._toRow)//2,(self._fromCol+self._toCol)//2)

    @property
    def mark(self) -> int:
        return self._mark

    def __str__(self) -> str:
        if self.placement:
            return Const.markStr(self._mark) + chr(ord('a')+self._toRow)+chr(ord('1')+self._toCol)
        else:
            return Const.markStr(self._mark) + chr(ord('a')+self._fromRow)+chr(ord('1')+self._fromCol) + '-' + chr(ord('a')+self._toRow)+chr(ord('1')+self._toCol)

    @classmethod
    def parse(cls,word : str) -> 'Move': # Move is not yet defined
        mark : int = Const.MARK_NONE
        if word[0] == 'g' or word[0] == 'G': mark = Const.MARK_GOAT
        if word[0] == 't' or word[0] == 'T': mark = Const.MARK_TIGER
        if mark == Const.MARK_NONE:
            raise ValueError("word must start with g or t")
        fromRow=ord(word[1])-ord('a')
        fromCol=ord(word[2])-ord('1')
        if len(word) > 3 and word[3] == '-':
            toRow=ord(word[4])-ord('a')
            toCol=ord(word[5])-ord('1')
        else:
            toRow=fromRow
            toCol=fromCol
        move = Move(mark,fromRow,fromCol,toRow,toCol)
        return move
