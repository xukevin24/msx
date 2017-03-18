'''
'''
import sys

import os
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, os.getcwd())

import strategy.istrategy as istrategy
import data_api 
import operator
class Strategy(istrategy.IStrategy):
    def __init__(self, enterStrategy, exitStrategy):
        self.enter_strategy = enterStrategy #[]与
        self.exit_strategy = exitStrategy   #[]或
        self.min_start_val = -1

    def min_start(self):
        if self.min_start_val < 0:
            self.min_start_val = 0
            for STG in self.enter_strategy:
                self.min_start_val = max(STG.min_start(), self.min_start_val)
            for STG in self.exit_strategy:
                self.min_start_val = max(STG.min_start(), self.min_start_val)
        return self.min_start_val

    def is_entry(self, dataApi, index):
        for STG in self.enter_strategy:
            if STG.is_entry(dataApi, index) == False:
                return False
        return True

    def is_exit(self, dataApi, index, enterInfo):
        for STG in self.exit_strategy:
            if STG.is_exit(dataApi, index, enterInfo):
                return True
        return False


