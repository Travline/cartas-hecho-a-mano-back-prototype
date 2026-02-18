import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel # Importante para la metadata
from collections.abc import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

raw_url = os.getenv("DATABASE_URL")

if raw_url:
    # Cambiamos el protocolo a asyncpg
    DATABASE_URL = raw_url.replace("postgres://", "postgresql+asyncpg://", 1).replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # IMPORTANTE: Si la URL trae 'prepared_statements=false' del .env de Supabase, quítalo
    if "prepared_statements=" in DATABASE_URL:
        import re
        DATABASE_URL = re.sub(r'(\?|&)?prepared_statements=[^&]*', '', DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    # Esta es la traducción de "prepared_statements=false" para asyncpg:
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
        yield session # El bloque 'async with' cierra la sesión automáticamente al terminar