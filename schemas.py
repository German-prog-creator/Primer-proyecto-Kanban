from pydantic import BaseModel

# Estructura básica que comparten las tareas
class TaskBase(BaseModel):
    title: str
    status: str = "pendiente"

# Lo que necesitamos cuando se crea una tarea nueva
class TaskCreate(TaskBase):
    pass

# Lo que el backend le responde a React (incluyendo el ID que le asignó la base de datos)
class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True