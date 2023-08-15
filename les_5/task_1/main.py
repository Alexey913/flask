# Задание №1
# 📌 Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс Task с полями id, title, description и status.
# 📌 Создайте список tasks для хранения задач.
# 📌 Создайте маршрут для получения списка задач (метод GET).
# 📌 Создайте маршрут для создания новой задачи (метод POST).
# 📌 Создайте маршрут для обновления задачи (метод PUT).
# 📌 Создайте маршрут для удаления задачи (метод DELETE).
# 📌 Реализуйте валидацию данных запроса и ответа.


from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import uvicorn
from random import randint as rnd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = "Свободное поле"
    status: bool


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = "Свободное поле"
    status: bool


tasks = []


@app.get('/', response_model=list[Task])
async def root():
    logger.info('Отработал GET-запрос')
    return tasks


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskIn):
    id = len(tasks) + 1
    new_task = Task
    new_task.id = id
    new_task.title = task.title
    new_task.description = task.description
    new_task.status = task.status
    tasks.append(new_task)
    logger.info('Отработал POST-запрос')
    return new_task


@app.get("/{id}", response_model=Task)
async def find_task(id: int):
    for task in tasks:
        if task.id == id:
            logger.info('Отработал find-запрос')
            return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    logger.info(f'Отработал PUT-запрос для задачи task_id = {task_id}')
    return {"task_id": task_id, "task": task}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    logger.info(f'Отработал DELETE-запрос для задачи task_id = {task_id}')
    return {"task_id": task_id}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    print(tasks)
