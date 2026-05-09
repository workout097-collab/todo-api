from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)


class UserTaskResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    email: str
    tasks: list[UserTaskResponse]

    class Config:
        from_attributes = True