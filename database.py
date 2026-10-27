from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Aquí definimos el nombre del archivo de nuestra base de datos local
SQLALCHEMY_DATABASE_URL = "sqlite:///./kanban.db"

# Creamos el motor que conectará Python con SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos una "sesión" (una conexión activa para hacer operaciones)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Esta función abre una conexión a la base de datos cuando se necesita y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()