from sqlalchemy.orm import Session
import models, schemas

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email.lower())

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email.lower())
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = get_user(db, user.email)  # Now directly using get_user
    if db_user:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value) if key != 'email' else None  # Skip updating email
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_email: str):
    db_user = get_user(db, user_email)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user(db, email).first()
    if db_user and db_user.check_password(password):
        return db_user
    return False
