from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import FastAPI, HTTPException
import httpx
from sqlalchemy.orm import Session
from .models import Question
from .db import get_db

app = FastAPI()


@app.get("/get_questions/")
async def get_questions(db: AsyncSession = Depends(get_db)):
    async with db() as session:
        query = select(Question)
        result = await session.execute(query)
        questions = result.scalars().all()
        return questions


@app.post("/get_questions/")
async def get_questions(questions_num: int):
    if questions_num <= 0:
        raise HTTPException(status_code=400, detail="Количество вопросов должно быть положительным целым числом")

    api_url = f"https://jservice.io/api/random?count={questions_num}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 200:
                questions = response.json()
                return questions
            else:
                raise HTTPException(status_code=response.status_code, detail="Не удалось получить вопросы")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при выполнении запроса к API: {str(e)}")


@app.post("/question/")
async def quest_post(question: Question, db: AsyncSession = Depends(get_db)):
    question_num = question.question_num
    questions = await get_questions(question_num)
    for x in range(1, question_num + 1):
        gen_quest = x
        return {"question": gen_quest}


def is_unique(db: Session, text: str):
    exist_question = db.query(Question).filter(Question.text == text).first()
    if exist_question:
        raise HTTPException(status_code=400, detail="Вопрос уже существует")


def save_question(db: Session, text: str, answer: str):
    new_question = Question(text=text, answer=answer)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@app.post("/fetch-questions/")
async def fetch_questions(question: Question, db: AsyncSession = Depends(get_db)):
    question_num = question.question_num
    questions = []

    async with httpx.AsyncClient() as client:
        for _ in range(question_num):
            response = await client.get("https://jservice.io/api/random?count=1")
            data = response.json()

            if not is_unique(db, data):
                while not is_unique(db, data):
                    response = await client.get("https://jservice.io/api/random?count=1")
                    data = response.json()

            save_question(db, data)
            questions.append(data)

    return questions


@app.get("/previous_question/")
async def get_previous(db: Session):
    previous_question = db.query(Question).order_by(Question.id.desc()).first()
    if previous_question is not None:
        return previous_question
    else:
        raise HTTPException(status_code=404, detail="No previous question found")
