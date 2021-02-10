from const import Const
from game import Game
import random
from matchup import Matchup
from randomagent import RandomAgent
from shygoatagent import ShyGoatAgent
from playoff import Playoff

game = Game()
playoff = Playoff(trials = 10, verbose = False)


playoff.addGoatAgent("shy goat",ShyGoatAgent(game))
playoff.addTigerAgent("random tiger",RandomAgent(game,Const.MARK_TIGER))

playoff.play()
