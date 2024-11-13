#!/usr/bin/env python3
"""
    Module that implements session authentication mechanism
"""
from api.v1.auth.auth import Auth
from flask import request
import uuid
import os


class SessionAuth(Auth):
    """Class that implements session authentication system
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user with user_id"""
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns use id based on a session id"""
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
        
        
