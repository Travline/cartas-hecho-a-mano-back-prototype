import os
import re
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from collections.abc import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

raw_url = os.getenv("DATABASE_URL")

if not raw_url:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno de Vercel")

# 1. Asegurar el protocolo correcto de forma limpia
# Primero normalizamos a postgresql:// y luego a postgresql+asyncpg://
DATABASE_URL = raw_url.replace("postgres://", "postgresql://", 1)
if "postgresql+asyncpg://" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Limpieza de parámetros conflictivos de Supabase/Prisma
DATABASE_URL = re.sub(r'(\?|&)?prepared_statements=[^&]*', '', DATABASE_URL)
DATABASE_URL = re.sub(r'(\?|&)?pgbouncer=[^&]*', '', DATABASE_URL)

# 3. Configuración del Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0
    },
    pool_pre_ping=True,
    pool_size=2,
    max_overflow=0
)

async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session