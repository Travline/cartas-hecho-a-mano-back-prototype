from fastapi import APIRouter, Depends, HTTPException, Request, Response
from models.users import UserCreate, UserRead, User, UserLogin
from database.db_connection import AsyncSession, get_session
from auth.hash import hash_secret, verify_secret
from auth.jwt import get_current_user, send_refresh_token, send_token, create_token
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=201)
async def register(
  user: UserCreate,
  session: AsyncSession = Depends(get_session)
):
  hashed_password = await hash_secret(user.pwd)
  if not hashed_password:
    raise HTTPException(status_code=400, detail="Hashing error or password too short")

  user_dict = user.model_dump()
  user_dict["pwd"] = hashed_password
    
  db_user = User(**user_dict)
  
  session.add(db_user)
  
  try:
    await session.commit()
    await session.refresh(db_user)
  except IntegrityError as e:
    await session.rollback()
    if "mail" in str(e.orig):
      raise HTTPException(status_code=400, detail="Email already used")
    raise HTTPException(status_code=500, detail="Integrity error")

  return db_user

@router.post("/login")
async def login(
  response: Response,
  user: UserLogin,
  session: AsyncSession = Depends(get_session)
):
  if len(user.pwd.strip()) < 8:
    raise HTTPException(status_code=400, detail="Unexpected data")
  
  statement = select(User).where(User.mail == user.mail.strip(), User.is_active == True)
  result = await session.exec(statement)
  db_user = result.one_or_none()

  if not db_user:
    raise HTTPException(status_code=401, detail="Invalid credentials")

  is_correct_pwd = await verify_secret(secret=user.pwd, storaged_secret=db_user.pwd)

  if not is_correct_pwd:
    raise HTTPException(status_code=401, detail="Invalid credentials")

  token = await create_token(str(db_user.user_id))
  await send_token(response, token)

  return {"message":"Login succesful"}

@router.get("/me")
async def get_admin_profile(
    request: Request,
    response: Response,
    user_id: str = Depends(get_current_user)  
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Sesión expirada")

    await send_refresh_token(user_id, request, response)

    return {"id": user_id}
