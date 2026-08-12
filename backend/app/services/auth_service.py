from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def register_user(db: Session, user_create: UserCreate):
    hashed_pwd = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        password_hash=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
