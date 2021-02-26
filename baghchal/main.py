from metaagent import MetaAgent
import sys,re,importlib
from typing import List
from const import Const
from game import Game
from agent import Agent
from matchup import Matchup
from randomagent import RandomAgent
from shygoatagent import ShyGoatAgent
from playoff import Playoff

# https://thomassileo.name/blog/2012/12/21/dynamically-load-python-modules-or-classes/
def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

def metaagent(game : Game, side : int, parms : string) -> Agent:
    args=parms.split(',')
    metaAgent = MetaAgent(game,side)
    for arg in args:
        matched=re.match(r'maxDepth=(.*)',arg)
        if matched:
            metaAgent.maxDepth=int(matched.group(1))
        matched=re.match(r'goat=(.*)',arg)
        if matched:
            name=matched.group(1)
            clazz=load_class(name)
            metaAgent.goat=clazz(game,Const.MARK_GOAT)
        matched=re.match(r'tiger=(.*)',arg)
        if matched:
            name=matched.group(1)
            clazz=load_class(name)
            metaAgent.tiger=clazz(game,Const.MARK_TIGER)
       
def setup(args) -> Playoff:
    game=Game()
    verbose=False
    trials=1
    goats : List[Agent] = []
    tigers : List[Agent] = []
    for i in range(len(args)):
        if args[i] == "--verbose":
            verbose = True
            continue
        matched=re.match(r'--trials=([0-9]+)',args[i])
        if matched:
            trials = int(matched.group(1))
            continue
        matched=re.match(r'--goat=(.*)',args[i])
        if matched:
            name=matched.group(1)
            clazz=load_class(name)
            agent=clazz(game,Const.MARK_GOAT)
            goats.append((name + " goat",agent))
            continue
        matched=re.match(r'--metagoat=(.*)',args[i])
        if matched:
            parms=matched.group(1)
            agent=metaagent(game,Const.MARK_GOAT,parms)
            continue
        matched=re.match(r'--tiger=(.*)',args[i])
        if matched:
            name=matched.group(1)
            clazz=load_class(name)
            agent=clazz(game,Const.MARK_TIGER)
            tigers.append((name + " tiger",agent))
            continue
        matched=re.match(r'--metatiger=(.*)',args[i])
        if matched:
            parms=matched.group(1)
            agent=metaagent(game,Const.MARK_TIGER,parms)
            continue
    
    if len(goats) == 0:
        goats.append(('default random goat',RandomAgent(game,Const.MARK_GOAT)))
    if len(tigers) == 0:
        tigers.append(('default random tiger',RandomAgent(game,Const.MARK_TIGER)))
    playoff=Playoff(trials,verbose)
    for (name,agent) in goats:
        playoff.addGoatAgent(name,agent)
    for (name,agent) in tigers:
        playoff.addTigerAgent(name,agent)
    return playoff

def main(args) -> None:
    playoff = setup(args)
    playoff.play()

if __name__ == '__main__':
    main(sys.argv)
