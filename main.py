from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models 
import schemas
from database import engine, get_db

# Esto crea las tablas en SQLite automáticamente al arrancar por primera vez
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kanban API", version="1.0")

# ¡MUY IMPORTANTE! CORS permite que tu React (que corre en otro puerto, como el 5173) 
# pueda hablar con este servidor de Python sin que el navegador bloquee la comunicación por seguridad.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. RUTA GET: El frontend pide todas las tareas guardadas
@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.TaskModel).all()
    return tasks

# 2. RUTA POST: El frontend manda una nueva tarea para que la guardemos
@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.TaskModel(title=task.title, status=task.status)
    db.add(new_task)      # La agregamos a la sesión
    db.commit()     # Guardamos los cambios permanentemente en SQLite
    db.refresh(new_task)  # Actualizamos el objeto con el ID que le dio la base de datos
    return new_task

# 3. RUTA PUT: El frontend avisa que una tarea cambió (de columna o de texto)
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskBase, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    task.title = task_update.title
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task

# 4. RUTA DELETE: El frontend pide borrar una tarea por su ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(task)
    db.commit()
    return {"message": "Tarea eliminada exitosamente"}

    if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)