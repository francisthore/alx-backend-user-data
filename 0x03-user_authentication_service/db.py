#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given attributes."""
        if not kwargs:
            raise InvalidRequestError("No search parameters provided.")
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid attribute: {key}")
        session = self._session
        query = session.query(User)
        filter_condition = tuple_(*(getattr(User, key) for key in kwargs)).in_(
            [tuple(kwargs.values())]
        )
        user = query.filter(filter_condition).first()
        if not user:
            raise NoResultFound("User not found")
        return user
