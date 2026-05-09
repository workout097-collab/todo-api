from fastapi import APIRouter, Depends
from database import SessionLocal
from models.user import User
from models.task import Task,TaskCreate, TaskResponse, TaskUpdate
from security import get_current_user
from fastapi import HTTPException


router = APIRouter(
    prefix="/tasks",
    tags=["/Tasks"]
)


@router.get('/', response_model=list[TaskResponse])
def get_tasks(
    current_user_email: str = Depends(get_current_user)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    tasks = db.query(Task).filter(
        Task.user_id == user.id
    ).all()

    return tasks

@router.get('/{task_id}', response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user_email: str = Depends(get_current_user)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.post('/')
def add_task(
    task: TaskCreate,
    current_user_email: str = Depends(get_current_user)
):

    db = SessionLocal()
    if len(task.title) < 3:
        return {'error': 'Title too short'}, 400

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        'message': 'Task added',
        'task': {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description
        }
    }



@router.put('/{task_id}')
def update_task(task_id: int, updated_task: TaskCreate, current_user_email: str = Depends(get_current_user)):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description

    db.commit()
    db.refresh(task)

    return {
        'message': 'Task updated',
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description
        }
    }

@router.delete('/{task_id}')
def delete_task(
    task_id: int,
    current_user_email: str = Depends(get_current_user)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {'message': 'Task deleted'}





