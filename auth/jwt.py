from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta, UTC
from typing import Optional
from dotenv import load_dotenv
from os import getenv
from fastapi import Request, Response, Depends, HTTPException
from database.db_connection import AsyncSession, get_session
from sqlmodel import select
from models.users import User

load_dotenv()

async def create_token(user_id: str) -> Optional[str]:
  exp = datetime.now(timezone.utc) + timedelta(minutes=20)
  payload = {
    "user_id": str(user_id),
    "exp": exp
  }
  try:
    return jwt.encode(payload, getenv("JWT_KEY"), algorithm=getenv("JWT_ALGORITHM"))
  except JWTError:
    return None

async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> Optional[str]:
  token = request.cookies.get(getenv("COOKIE_NAME"))
  if not token:
    raise HTTPException(status_code=401, detail="Unexpected token")
  
  try:
    payload = jwt.decode(
      token, 
      getenv("JWT_KEY"), 
      algorithms=[getenv("JWT_ALGORITHM")]
    )
    user_id = payload.get("user_id")
  except JWTError:
    raise HTTPException(status_code=401, detail="No valid token")
  
  statement = select(User).where(User.user_id == user_id, User.is_active == True)
  result = await session.exec(statement)
  db_user = result.one_or_none()

  if not db_user:
      raise HTTPException(status_code=401, detail="Usuario no encontrado")
  
  return db_user.user_id
  
async def send_token(response: Response, token: Optional[str]):
  if not token:
    return

  response.set_cookie(  
    key=getenv("COOKIE_NAME"),
    value=token,
    httponly=True,
    samesite="none",
    secure=True
  )

async def send_refresh_token(user_id: str, request: Request, response: Response):
  token = request.cookies.get(getenv("COOKIE_NAME"))
  if not token:
    return 

  try:
    payload = jwt.decode(
      token, 
      getenv("JWT_KEY"), 
      algorithms=[getenv("JWT_ALGORITHM")],
      options={"verify_exp": False}
    )
  except JWTError:
    return

  exp_timestamp = int(payload.get("exp"))
  current_timestamp = int(datetime.now(timezone.utc).timestamp())

  if exp_timestamp - current_timestamp > 300:
    return 

  if current_timestamp - exp_timestamp > 600: 
    return

  new_token = await create_token(user_id)
  await send_token(response, new_token)