from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from dependencies import schemas, get_db, users, Annotated, get_current_active_user, List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)


# Get a list of all users.
# @router.get("/", response_model=List[schemas.User], tags=["Users"])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = users.get_users(db, skip=skip, limit=limit)
#     return users

# Get current user.
@router.get("/me", response_model=schemas.User, tags=["Users"])
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user


# Get user by id.
# @router.get("/{user_id}", response_model=schemas.User, tags=["Users"])
# def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = users.get_user_by_id(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# Create a user.
@router.post("/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db, user=user)


# Update the user.
@router.put("/", response_model=schemas.User, tags=["Users"])
def update_user(user: schemas.UserUpdate, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    db_user = users.get_user(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    
    return users.update_user(db, user=user)


# Delete the user.
@router.delete("/", response_model=schemas.User, tags=["Users"])
def delete_user(user: schemas.UserDelete, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    db_user = users.get_user(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    
    return users.delete_user(db, user=user)

