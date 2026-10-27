from sqlalchemy import Column, Integer, String
from database import Base

# Definimos la tabla llamada "tasks" en la base de datos
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="pendiente")