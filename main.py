from datetime import timedelta
import ssl
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.concurrency import asynccontextmanager
import uvicorn
from controller.ItemController import router as items_router
from controller.UserController import authenticate_user, create_access_token, router as users_router
from credentials import CREDENTIALS
from database import create_db_and_tables
from model.Token import Token
from security import ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionDep

app = FastAPI(title="Micro-Serviço CRM")


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


app.include_router(items_router)
app.include_router(users_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=CREDENTIALS['SSL_CERT'], keyfile=CREDENTIALS['SSL_KEY'])

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=9000, ssl_keyfile=CREDENTIALS['SSL_KEY'], ssl_certfile=CREDENTIALS['SSL_CERT'])
