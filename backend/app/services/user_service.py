from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

class UserService:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Fetch a user by database integer ID.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """
        Fetch a user by unique username.
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """
        Fetch a user by unique email.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user, automatically secure hashing the password.
        """
        hashed_password = get_password_hash(obj_in.password)
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, *, username_or_email: str, password: str) -> Optional[User]:
        """
        Verify login credentials. Checks matches against username or email.
        Returns the User object if verification is successful, otherwise None.
        """
        # Allow sign in with email or username
        if "@" in username_or_email:
            user = UserService.get_by_email(db, username_or_email)
        else:
            user = UserService.get_by_username(db, username_or_email)
            
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
