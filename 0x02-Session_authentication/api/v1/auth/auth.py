#!/usr/bin/env python3
"""
Module that handles and defines authentication class
for the API
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Class that defines and handles auth methods
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if paths requires authentication"""
        if not path:
            return True
        if not excluded_paths:
            return True
        if path[-1] != '/':
            path = '{}/'.format(path)

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
            elif path == excluded:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets auth header from request"""
        if not request:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if not request:
            return None
        session_cookie = request.cookies.get(os.getenv('SESSION_NAME'))
        return session_cookie
