from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Optional

from database import create_document, get_documents
from schemas import Submission

app = FastAPI(title="Vibe Code Academy API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend OK", "backend": "fastapi"}

@app.get("/test")
async def test_db():
    try:
        collections = ["user", "progress", "submission"]
        existing = {}
        # trigger a lightweight call for each collection
        for c in collections:
            docs = await get_documents(c, limit=1)
            existing[c] = len(docs)
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "collections": list(existing.keys()),
            "connection_status": "ok",
        }
    except Exception as e:
        return {"backend": "fastapi", "database": "mongodb", "connection_status": f"error: {e}"}

# Simulated run endpoint; stores submissions for history
class RunRequest(BaseModel):
    language: Literal["python", "javascript", "node", "java", "csharp", "c", "cpp", "css"]
    code: str
    user_id: Optional[str] = None

@app.post("/run")
async def run_code(req: RunRequest):
    # No real execution for safety; echo preview
    preview = "\n".join(req.code.splitlines()[:12])
    result = f"Simulated run for {req.language}\n---\n{preview}"
    if req.language == "css":
        result = "CSS applied! (simulation)"

    # Store submission history
    _ = await create_document("submission", Submission(user_id=req.user_id, language=req.language, code=req.code, result=result).model_dump())
    return {"result": result}
