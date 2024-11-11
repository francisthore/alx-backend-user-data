#!/usr/bin/env python3
"""
    Module that handles basic auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode as b_dec
from base64 import b64encode as b_enc
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
        Setups and handles basic auth operations in API
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
            returns the Base64 part of the Authorization
            header for a Basic Authentication
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
            Decodes a base64 string
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            b64_header = base64_authorization_header
            if b_enc(b_dec(b64_header)).decode('utf-8') == b64_header:
                return b_dec(b64_header).decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
            Extracts user credentials from a string
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(val for val
                     in decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
            Returns user instance for the provided credentials
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        User.load_from_file()
        users = User.search({'email': user_email})

        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Overloads Auth class and retrieved current user from request
        """
        if not request:
            return None
        if not self.authorization_header(request):
            return None
        header = self.authorization_header(request)
        if not self.extract_base64_authorization_header(header):
            return None
        extracted = self.extract_base64_authorization_header(header)
        if not extracted:
            return None
        decoded = self.decode_base64_authorization_header(extracted)
        if not decoded:
            return None
        credentials = self.extract_user_credentials(decoded)
        if credentials == (None, None):
            return None
        user = self.user_object_from_credentials(credentials[0],
                                                 credentials[1])
        if not user:
            return None
        return user
