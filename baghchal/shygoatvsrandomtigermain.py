from const import Const
from game import Game
import random
from matchup import Matchup
from randomagent import RandomAgent
from shygoatagent import ShyGoatAgent
from playoff import Playoff

game = Game()
playoff = Playoff(trials = 1000)


playoff.addGoatAgent("shy goat",ShyGoatAgent(game,Const.MARK_GOAT))
playoff.addTigerAgent("random tiger",RandomAgent(game,Const.MARK_TIGER))

playoff.play()
