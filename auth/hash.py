from os import getenv
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from dotenv import load_dotenv
from typing import Optional

ph = PasswordHasher(
  time_cost=2,
  memory_cost=32768,
  parallelism=1,
  hash_len=64,
  salt_len=16,
)
load_dotenv()
PEPPER = getenv("PEPPER")

async def hash_secret(secret:str) -> Optional[str]:
  try:
    if len((str(secret)).strip()) >= 8:
      return ph.hash(secret+PEPPER)
    else:
      return None
  except Exception as e:
    print(str(e))
    return None

async def verify_secret(storaged_secret:str, secret:str) -> bool:
  try:
    if len((str(secret)).strip()) >= 8:
      return ph.verify(storaged_secret, secret+PEPPER)   
    else:
      return False
  except Exception:
    return False
