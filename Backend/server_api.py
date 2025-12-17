from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_brain import solve

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: str

@app.post("/api/solve")
async def run_agent(req: TaskRequest):
    result = solve(req.task)
    return {
        "code": result["code"],
        "logs": result["logs"],
        "attempts": result["attempts"]
    }
import os
from typing import TypedDict, List