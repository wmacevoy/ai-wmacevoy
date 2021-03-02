from random import Random

from game import Game
from move import Move
from const import Const
from randomagent import RandomAgent
from agent import Agent


class Matchup:
    '''
    Pit two agents against each other in a game
    '''
    def __init__(self, verbose : bool = False, fast : bool = False):
        self._game = Game()
        self._goatAgent : Agent = RandomAgent(self._game, Const.MARK_GOAT)
        self._tigerAgent : Agent = RandomAgent(self._game,Const.MARK_TIGER)
        self._verbose = verbose
        self._fast = fast
        if not self._fast:
            self._shadowGame = Game()


    def propose(self) -> Move:
        if self._game.state == Const.STATE_TURN_GOAT:
            return self._goatAgent.propose()
        if self._game.state == Const.STATE_TURN_TIGER:
            return self._tigerAgent.propose()
        raise ValueError("game is over")
        
    
    def turn(self)  -> None:
        if self._game.over:
            if self._verbose:
                print("game over - " + Const.stateStr(game.state))
                print(game)
            return
        move = self.propose()
        self._game.play(move)
        if not self._fast:
            self._shadowGame.moveOk(move)
            self._shadowGame.play(move)
            if self._game != self._shadowGame:
                raise ValueError("game and shadow out of sync")
        if self._verbose:
            print("after move " + str(move) + ":")
            print(self._game)

    #@property
    #def game(self) -> Game:
    #    return self._game

    def reset(self) -> None:
        self._game.reset()
        if not self._fast:
            self._shadowGame.reset()

    @property
    def state(self) -> int:
        return self._game.state

    @property
    def over(self) -> bool:
        return self._game.over

    @property
    def tigerAgent(self) -> Agent:
        return self._tigerAgent
    @tigerAgent.setter
    def tigerAgent(self,value : Agent) -> None:
        value.game = self._game
        value.side = Const.MARK_TIGER
        self._tigerAgent = value

    @property
    def goatAgent(self) -> Agent:
        return self._goatAgent
    @goatAgent.setter
    def goatAgent(self,value : Agent) -> None:
        value.game = self._game
        value.side = Const.MARK_GOAT
        self._goatAgent = value

