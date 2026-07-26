from sqlalchemy.orm import Session

from app import models, schemas


# User CRUD

#Get a user by email.
def get_user_by_email(db: Session, email: str):
   
    return db.query(models.User).filter(models.User.email == email).first()

#Get a user by ID.
def get_user_by_id(db: Session, user_id: int):
    
    return db.query(models.User).filter(models.User.id == user_id).first()

  #Get all users
def get_all_users(db: Session):
    
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    #Create a new user
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



# Todo CRUD

#Create a todo for a user
def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        user_id=user_id,
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo



 #Get all todos for a specific user

def get_all_todos(db: Session, user_id: int):
    
    return (
        db.query(models.Todo)
        .filter(models.Todo.user_id == user_id)
        .all()
    )


 #Get a todo by ID
def get_todo_by_id(db: Session, todo_id: int):
   
    return (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .first()
    )


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):       #Update a todo
   
    db_todo = get_todo_by_id(db, todo_id)

    if not db_todo:
        return None

    update_data = todo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo(db: Session, todo_id: int):         #Delete a todo
    
    db_todo = get_todo_by_id(db, todo_id)

    if not db_todo:
        return None

    db.delete(db_todo)
    db.commit()

    return db_todo