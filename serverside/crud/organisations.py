import uuid
from sqlalchemy.orm import Session
import models, schemas

def get_organisation(db: Session, uuid: str):
    return db.query(models.Organisation).filter(models.Organisation.uuid == uuid).first()

def get_organisations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organisation).offset(skip).limit(limit).all()

def create_organisation(db: Session, organisation: schemas.OrganisationCreate):
    organisation_uuid = str(uuid.uuid4())
    db_organisation = models.Organisation(uuid=organisation_uuid, **organisation.dict())
    db.add(db_organisation)
    db.commit()
    db.refresh(db_organisation)
    return db_organisation

def delete_organisation(db: Session, uuid: str):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.uuid == uuid).first()
    if db_organisation:
        db.delete(db_organisation)
        db.commit()
        return True
    return False
