from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from dependencies import schemas, get_db, token, users, Annotated, OAuth2PasswordRequestForm, timedelta, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["Token"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)

@router.post("/token", response_model=schemas.Token, tags=["Token"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
