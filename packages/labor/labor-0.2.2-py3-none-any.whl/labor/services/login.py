#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 09 13:43:12 2022
@author ccavalcante
"""

import httpx

from utils.config import Configuration

from labor.enums.api import LaborApiEnum


class LoginService:

    def __init__(self):

        self.__config = Configuration.get_instance()

        self.__logged_user_key = 'user.auth' 

    def __update_header_interceptor(self, headers):

        headers = {
            'access-token': headers['access-token'],
            'client': headers['client'],
            'expiry': headers['expiry'],
            'uid': headers['uid'],
            'token-type': headers['token-type']
        }

        self.logged_user = headers

        return self

    @property
    def logged_user(self) -> dict:

        return self.__config.get(self.__logged_user_key)

    @logged_user.setter
    def logged_user(self, logged_user: dict):

        self.__config.put(
                self.__logged_user_key,
                logged_user
                )

        self.__config.write()

    def __do_request(self,
                     url_path, 
                     body={},
                     method='get', 
                     intercept=True):

        headers = self.logged_user

        url = LaborApiEnum.BASE_URL + url_path 
        response = getattr(httpx, method)(
                url,
                json=body,
                headers=headers
                )

        if intercept and response.status_code == 200:
            self.__update_header_interceptor(response.headers)

        return response


    def do_login(self, email, password):

        body = {
                'email': email,
                'password': password
                }

        res = self.__do_request(
                LaborApiEnum.SIGN_IN,
                body=body,
                method='post'
                )

        return res.json(), res.status_code 

