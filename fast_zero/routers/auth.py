from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.security import create_token,  verify_password


router = APIRouter(prefix='/auth',tags=["auth"])
Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/login", response_model=Token)
def login( form_data: OAuth2Form, session: Session):

    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    acess_token = create_token(
        {'sub': user.email}
    )
    return {'access_token': acess_token, 'token_type': 'bearer'}