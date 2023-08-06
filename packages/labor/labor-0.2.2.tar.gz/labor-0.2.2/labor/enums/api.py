#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 09 13:47:11 2022
@author ccavalcante
"""

from enum import Enum

class LaborApiEnum(str, Enum):
    """
    Variables to connect to labor api
    """

    BASE_URL = "https://api.getlabor.com.br/"
    SIGN_IN = "auth/sign_in" 
    SIGN_OUT = "auth/sign_out" 
    TASKS = "tasks"
    USERS = "users"
    REPORTS = "reports"
