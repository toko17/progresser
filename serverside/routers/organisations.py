from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
import schemas, dependencies
from crud import organisations

router = APIRouter(tags=["Organisation"])

@router.get("/organisations/", response_model=List[schemas.OrganisationRead])
def read_organisations(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_organisations = organisations.get_organisations(db, skip=skip, limit=limit)
    return db_organisations

@router.get("/organisations/{uuid}", response_model=schemas.OrganisationRead)
def read_organisation(uuid: str, db: Session = Depends(dependencies.get_db)):
    db_organisation = organisations.get_organisation(db, uuid=uuid)
    if db_organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return db_organisation

@router.post("/organisations/", response_model=schemas.OrganisationRead)
def create_organisation(organisation: schemas.OrganisationCreate, db: Session = Depends(dependencies.get_db)):
    return organisations.create_organisation(db=db, organisation=organisation)

@router.delete("/organisations/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organisation(uuid: str, db: Session = Depends(dependencies.get_db)):
    success = organisations.delete_organisation(db, uuid=uuid)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
