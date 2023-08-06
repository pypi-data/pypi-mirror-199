#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 09 13:36:02 2022
@author ccavalcante
"""
import os

import click

from labor.services.login import LoginService 
from labor.utils.alert import AlertUtil

class Screen:

    @classmethod
    def clean(cls):

        os.system('clear')

    @classmethod
    def show_banner(cls):
        cls.clean()

        f = open('./labor/banner.txt')

        print('\n\n', f.read(), '\n\n')


class LoginController:

    def __init__(self):

        self.__service = LoginService()

    def sign_in(self):

        Screen.show_banner()

        email = click.prompt(AlertUtil.paint('Enter your email', 'blue'), type=str)
        password = click.prompt(
                AlertUtil.paint('Enter your password', 'blue'), 
                type=str,
                hide_input=True)

        body, status_code = self.__service.do_login(email, password)

        if status_code != 200:

            errors = " ".join(body['errors'])

            AlertUtil.error(errors)

            return

        user_name = AlertUtil.paint(body['data']['name'], 'green')

        message = f'Seja bem-vindo {user_name}'

        AlertUtil.simple_print("\n\n" + message)
