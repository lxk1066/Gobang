# -*- coding: UTF-8 -*-

# tic_tac_toe  --->  class
# -*- coding:UTF-8 -*-
# *is_offensive* means Who is the first and who is the second

class Player(object):
    def __init__(self, initiative: bool):
        self.__initiative = initiative
        self.__status = None

    def win_fail(self):
        if self.__status == 1:
            return True
        elif self.__status == -1:
            return False
        else:
            return None

    def set_winner(self):
        self.__status = True

    def set_loser(self):
        self.__status = False

    def update(self):
        self.__initiative = not self.__initiative

    def get_initiative(self):
        return self.__initiative

    def get_status(self):
        return self.__status


