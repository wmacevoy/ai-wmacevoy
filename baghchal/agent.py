from game import Game
from move import Move

class Agent:
    '''
    Agents are the 'AI' part, they propose
    a Move object as the best next move in the
    game for their side.
    '''
    def __init__(self, game : Game, side : int):
        self._game = game
        self._side = side

    @property
    def state(self) -> int:
        return self._game.state

    @property
    def game(self) -> Game:
        return self._game

    @game.setter
    def game(self,value) -> None:
        self._game = value

    @property
    def side(self) -> int:
        return self._side

    @side.setter
    def side(self,value) -> None:
        self._side = value

    def propose(self) -> Move:
        '''
        propose must be defined in a subclass for the specific logic
        of choosing a 'good' move.  See RandomAgent as an
        example that chooses random one of the available
        moves to the side in question.
        '''
        raise ValueError("nope.")
