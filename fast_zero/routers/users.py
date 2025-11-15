from fastapi import APIRouter
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserResponseSchema, UserSchema
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fast_zero.security import get_current_user, get_password_hash
from typing import Annotated

router = APIRouter(prefix='/users',tags=["users"])
Session = Annotated[Session, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]

@router.post("/",status_code=HTTPStatus.CREATED,response_model=UserResponseSchema)
def create_user(user: UserSchema, session: Session ):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:  
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already registered"
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already registered"
            )
    db_user = User(user.username, get_password_hash(user.password), user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get("/", status_code=HTTPStatus.OK, response_model=list[UserResponseSchema]) 
def get_users(session=Depends(get_session), limit: int = 1, offset: int = 0, current_user = Depends(get_current_user)):
    users_list = session.scalars(select(User).limit(limit).offset(offset)).all()
    return users_list

@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserResponseSchema)
def put_user(user_id: int, user: UserSchema, session: Session, current_user : Current_user):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You can only update your own user"
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError: 
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail='Username or Email already exists'
        )

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT, response_model=None)
def delete_user(user_id: int, session: Session, current_user : Current_user):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You can only delete your own user"
        )
    session.delete(current_user)
    session.commit()