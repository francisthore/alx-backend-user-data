#!/usr/bin/env python3
"""
    Module that implements session authentication mechanism
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Class that implements session authentication system
    """

    def __init__(self) -> None:
        """Initialises the class objects"""
        super().__init__()
