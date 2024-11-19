import datetime
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
import jwt
from sqlmodel import select
from typing_extensions import Annotated
from model.Token import TokenData
from model.User import User
from security import oauth2_scheme, ALGORITHM, SECRET_KEY, pwd_context
from database import SessionDep


router = APIRouter(prefix="/user")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: SessionDep, username: str):
    statement = select(User).where(User.username == username)
    result = db.execute(statement).one_or_none()

    if result:
        return result
    else:
        return {"message": "User not found"}


def authenticate_user(db: SessionDep, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user[0].hashed_password):
        return False
    return user[0]


def create_access_token(data: dict, expires_delta: Union[datetime.timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/signup")
async def sign_up(user: User, session: SessionDep) -> User :
    user.hashed_password = get_password_hash(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user