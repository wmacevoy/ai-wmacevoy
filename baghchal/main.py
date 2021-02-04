from const import Const
from game import Game
import random
from matchup import Matchup
from randomagent import RandomAgent
from playoff import Playoff

game = Game()
playoff = Playoff(trials = 1)


playoff.addGoatAgent("random goat",RandomAgent(game,Const.MARK_GOAT))
playoff.addTigerAgent("random tiger",RandomAgent(game,Const.MARK_TIGER))

playoff.play()
