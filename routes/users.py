from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal

from models.user import User

from schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserProfileResponse
)
from security import (
    verify_password,
    create_access_token,
    get_current_user,
    hash_password
)

from fastapi import APIRouter, status

router = APIRouter(
    prefix="/users",
    tags=["/Users"]
)

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




@router.post("/",response_model=UserResponse, tags=["Users"])
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

@router.get('/',response_model=UserResponse)
def get_user(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
       db.close()
       return {'error': 'User not found'}, 404

    db.close()

    return user


@router.delete('/{user_id}')
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


@router.put('/{user_id}', response_model=UserResponse)
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


@router.get('/users/',response_model=list[UserResponse])
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users






