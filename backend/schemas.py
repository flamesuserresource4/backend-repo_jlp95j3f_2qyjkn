from pydantic import BaseModel, Field
from typing import Optional, Literal

# One class = one collection (lowercased name)

class User(BaseModel):
    username: str
    email: str
    password_hash: str
    role: Literal["student", "instructor"] = "student"

class Progress(BaseModel):
    user_id: str
    track: Literal["python", "javascript", "node", "java", "csharp", "c", "cpp", "css"]
    lessons_completed: int = 0
    xp: int = 0

class Submission(BaseModel):
    user_id: Optional[str] = None
    language: Literal["python", "javascript", "node", "java", "csharp", "c", "cpp", "css"]
    code: str
    result: Optional[str] = None
