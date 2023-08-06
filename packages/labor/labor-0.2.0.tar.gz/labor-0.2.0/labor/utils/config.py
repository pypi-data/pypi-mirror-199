#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

from typing import Union
from functools import reduce
from copy import deepcopy


from .file_helper import FileHelper

DEFAULT_CONF_FILE='config.json'

class Configuration:

    __cache = {}

    __instance = None

    def __init__(self,
                 conf_dir='~/.labor',
                 conf_file_name=DEFAULT_CONF_FILE):


        if Configuration.__instance is not None:
            raise Error('this is a singleton, use get_instance function instead!')

        self.file_helper = FileHelper()

        self.conf_dir = conf_dir
        self.conf_file_name = conf_file_name

        self.load()

        Configuration.__instance = self

    @staticmethod
    def get_instance():

        if Configuration.__instance is None:
            Configuration()

        return Configuration.__instance

    def get_full_path(self):
        """
        Returns the full path of the conf file

        Returns
        -------
            str
        """

        return os.path.join(self.conf_dir, self.conf_file_name)

    @property
    def conf_file_name(self):

        return self.__conf_file_name

    @conf_file_name.setter
    def conf_file_name(self, conf_file_name):
        self.__conf_file_name = conf_file_name

    def get(self, key: str):
        """
        Returns a cached conf using a path key

        Parameters
        ----------
            key {str}
        """

        data = deepcopy(self.__cache)

        for k in key.split('.'):

            if data.get(k) is None:
                return None

            data = data.get(k)

        return data


    def put(self, key: str, data: Union[dict, str, bool, int]):
        """
        Insert or update a value using a key address

        Parameters
        ----------
            key: {str} | Ex: 'path.to.your.key'
        """

        if key is None:
            return None

        keys = key.split('.')
        keys.reverse()
        final_key = keys.pop(0)

        final_data = reduce(lambda acc, n_key: {n_key: acc}, keys, {final_key: data})
        
        self.__cache = {**self.__cache, **final_data}

        self.write()

        return self

    def write(self): 
        """
        Save the cached data

        Returns
        -------
            self
        """

        self.file_helper.save_json(
                self.__cache,
                self.conf_dir,
                self.conf_file_name
                )

        return self

    def load(self):

        self.__cache = self.file_helper.load_json(self.get_full_path()) or {}
    
        return self

