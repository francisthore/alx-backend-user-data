#!/usr/bin/env python3
"""Authentication module."""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Authentication manager."""

    def __init__(self):
        self._database = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            user = self._database.find_user_by(email=email)
        except NoResultFound:
            return self._database.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials."""
        try:
            user = self._database.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session for a user."""
        try:
            user = self._database.find_user_by(email=email)
        except NoResultFound:
            return None
        session = _generate_uuid()
        self._database.update_user(user.id, session_id=session)
        return session

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a user by session ID."""
        if not session_id:
            return None
        try:
            return self._database.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Invalidate a user session."""
        self._database.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token."""
        try:
            user = self._database.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")
        token = _generate_uuid()
        self._database.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password."""
        try:
            user = self._database.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")
        self._database.update_user(
            user.id, hashed_password=_hash_password(password), reset_token=None
        )


def _hash_password(password: str) -> bytes:
    """Hash a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique ID."""
    return str(uuid4())
