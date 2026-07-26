from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import cast

from app.auth import get_current_user
from app.crud import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
)
from app.database import get_db
from app.models import User
from app.schemas import ( Message,TodoCreate, TodoResponse,  TodoUpdate,   ) 

router = APIRouter( prefix="/todos",tags=["Todos"],)


@router.post("/",response_model=TodoResponse,)
def create_new_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user_id = cast(int, current_user.id)
    return create_todo(
        db,
        todo,
        current_user_id,
    )


@router.get("/", response_model=list[TodoResponse],)
def read_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user_id = cast(int, current_user.id)
    return get_all_todos(
        db,
        current_user_id,
    )


@router.get("/{todo_id}",   response_model=TodoResponse, )
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = get_todo_by_id(
        db,
        todo_id,
    )

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    current_user_id = cast(int, current_user.id)
    if cast(int, todo.user_id) != current_user_id:
        raise HTTPException(status_code=403,detail="Access denied",)

    return todo


@router.put("/{todo_id}",response_model=TodoResponse,)
def update_existing_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = get_todo_by_id(db,  todo_id,)

    if db_todo is None:
        raise HTTPException(status_code=404,  detail="Todo not found",)

    current_user_id = cast(int, current_user.id)
    if db_todo.user_id != current_user_id: # pyright: ignore[reportGeneralTypeIssues]
        raise HTTPException(status_code=403,detail="Access denied",)

    return update_todo(db,todo_id,todo,)


@router.delete("/{todo_id}",response_model=Message,)
def remove_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = get_todo_by_id(db,todo_id,)

    if todo is None:
        raise HTTPException(status_code=404,detail="Todo not found",)

    if cast(int, todo.user_id) != cast(int, current_user.id):
        raise HTTPException( status_code=403,detail="Access denied",)

    delete_todo( db,todo_id,)

    return {
        "message": "Todo deleted successfully"
    }