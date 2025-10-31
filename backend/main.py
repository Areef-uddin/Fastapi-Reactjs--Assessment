from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import store, schemas

app = FastAPI(title="Tasks + Comments (No DB)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Reset endpoint for tests/dev only
@app.post("/__reset__")
def reset_store():
    store.store.reset()
    return {"reset": True}


# Tasks
@app.post("/tasks/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate):
    t = store.store.create_task(title=task.title, description=task.description)
    return t


@app.get("/tasks/", response_model=list[schemas.TaskRead])
def list_tasks():
    return store.store.list_tasks()


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int):
    t = store.store.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task: schemas.TaskCreate):
    t = store.store.update_task(task_id, title=task.title, description=task.description)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    ok = store.store.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}


# Comments
@app.post("/tasks/{task_id}/comments/", response_model=schemas.CommentRead)
def add_comment(task_id: int, comment: schemas.CommentCreate):
    c = store.store.create_comment(task_id, comment.content)
    if not c:
        raise HTTPException(status_code=404, detail="Task not found")
    return c


@app.get("/tasks/{task_id}/comments/", response_model=list[schemas.CommentRead])
def list_comments(task_id: int):
    # ensure task exists
    if not store.store.get_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return store.store.list_comments(task_id)


@app.put("/comments/{comment_id}", response_model=schemas.CommentRead)
def update_comment(comment_id: int, comment: schemas.CommentCreate):
    c = store.store.update_comment(comment_id, comment.content)
    if not c:
        raise HTTPException(status_code=404, detail="Comment not found")
    return c


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    ok = store.store.delete_comment(comment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"deleted": True}
