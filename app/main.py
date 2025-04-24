from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.openai_utils import get_embedding
from app.db import get_best_answer

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/qa")
def qa_route(payload: QuestionRequest):
    embedding = get_embedding(payload.question)
    result = get_best_answer(embedding)
    
    if result is None:
        raise HTTPException(status_code=200, detail="No relevant answer found")

    return result