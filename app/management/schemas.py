from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: str
    is_admin: bool


class UserCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    phone_no: str | None = None
    password: str


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    img: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: int
    is_admin: bool

