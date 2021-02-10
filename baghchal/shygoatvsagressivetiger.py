from const import Const
from game import Game
import random
from matchup import Matchup
from randomagent import RandomAgent
from shygoatagent import ShyGoatAgent
from agressivetigeragent import AggressiveTigerAgent
from playoff import Playoff

game = Game()
playoff = Playoff(trials = 1000)


playoff.addGoatAgent("shy goat",ShyGoatAgent(game,Const.MARK_GOAT))
playoff.addTigerAgent("agressive tiger",AggressiveTigerAgent(game,Const.MARK_TIGER))

playoff.play()
