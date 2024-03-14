from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing_extensions import Annotated
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from crud import users, token, organisations, tables, lists, tasks, subtasks
import models, schemas
from database import SessionLocal, engine
from crud.token import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from fastapi.middleware.cors import CORSMiddleware

from fastapi import APIRouter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    print(token_data.username)
    user = users.get_user(db, email=token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

