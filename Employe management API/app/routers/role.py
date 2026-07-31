from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/",response_model=list[schemas.RoleResponse])
def get_roles( db: Session = Depends(get_db)):
    return db.query(models.Role).all()

@router.post("/",response_model=schemas.RoleResponse)
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_role = db.query(models.Role).filter(models.Role.name == role.name).first()

    if existing_role:
        raise HTTPException(status_code=400,detail="Role already exists")

    new_role = models.Role(name=role.name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role

