#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 09 14:18:23 2022
@author ccavalcante
"""

from colorama import init
from termcolor import colored

init(autoreset=True)

class AlertUtil:
    """
    Class used to print colored allerts
    """

    @classmethod
    def simple_print(cls, message):
        print(message)

    @classmethod
    def __print(cls, message, color):

        print(cls.paint(message, color))

    @classmethod
    def paint(cls, message, color):
        return colored(message, color)

    @classmethod
    def error(cls, message):

        cls.__print(message, 'red')

    @classmethod
    def success(cls, message):

        cls.__print(message, 'green')

    @classmethod
    def info(cls, message):
        cls.__print(message, 'cyan')

    @classmethod
    def warn(cls, message):
        
        cls.__print(message, 'yellow')
