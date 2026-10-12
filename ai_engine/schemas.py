from pydantic import BaseModel,Field


class InterviewQuestion(BaseModel):
    question: str
    topic: str
    difficulty: str

class InterviewRequest(BaseModel):    
    technology: str    
    difficulty: str    
    count: int = Field(ge=1, le=20)

class InterviewResponse(BaseModel):
    technology: str
    difficulty: str
    questions: list[InterviewQuestion]