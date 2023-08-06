#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 09 10:39:16 2022
@author ccavalcante
"""

import os
import json

class FileHelper:
    """
    Used to manage files in general
    """

    def exists(self, path: str):
        """
        Checks if a file exists

        Parameters
        ----------
            path: {str}

        Returns
        -------
            bool
        """

        return os.path.exists(path)

    def mkdir(self, path: str):
        """
        Creates a directory if it does not exists

        Parameters
        ----------            
            path {str}

        Returns
        -------
            {bool}
        """

        if self.exists(path):
            return True

        return os.mkdir(path)

    def load_json(self, path: str):
        """
        Load a json file and returns as dictionary

        Parameters
        ----------
            path {str}

        Returns
        -------
            {dict}
        """

        if not self.exists(path):

            return None

        file = open(path, 'r')

        return json.load(file)


    def save_json(self, data: dict, path: str, file_name: str, indent=2):
        """
        Save a dictionary into a json file

        Parameters
        ----------
            data {dict}
            path {str}
            indent {int} | default: 2

        Returns
        -------
            bool
        """

        path = os.path.expanduser(path)

        if not self.exists(path):
            self.mkdir(path)

        try: 
            file = open(os.path.join(path, file_name), 'w')
            json.dump(data, file, indent=indent)
        except Exception as e:

            print(e)
            return False

        return True
