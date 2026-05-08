from fastapi.security import OAuth2PasswordRequestForm

from models.user import User, UserCreate, UserLogin
from database import SessionLocal
from fastapi import APIRouter, status
from security import (verify_password,create_access_token)
from fastapi import Depends
from models.user import UserProfileResponse


from security import get_current_user

from security import hash_password

router = APIRouter()

@router.get(
    '/profile',
    response_model=UserProfileResponse
)
def profile(
    current_user_email: str = Depends(get_current_user)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    return user

@router.post('/login')
def login(user_data: OAuth2PasswordRequestForm = Depends()):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == user_data.username
    ).first()

    if not user:
        db.close()
        return {'error': 'User not found'}

    if not verify_password(user_data.password, user.password):
        db.close()
        return {'error': 'Invalid email or password'}

    access_token = create_access_token(
        data={"sub": user.email}
    )

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




@router.post('/users')
def add_users(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        first_name = user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()
    return new_user

@router.get('/users/{user_id}')
def get_user(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
       db.close()
       return {'error': 'User not found'}, 404

    db.close()

    return user


@router.delete('/users/{user_id}')
def deleted_user(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        return {'error': 'User not found'}, 404

    db.delete(user)

    db.commit()

    db.close()

    return  {'message': 'User deleted'}, status.HTTP_200_OK


@router.put('/users/{user_id}')
def update_user(user_id: int, user_data: UserCreate):

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        return {'error': 'User not found'}, 404

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email

    db.commit()

    db.close()


    return user


@router.get('/users/')
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users






