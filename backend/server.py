from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_research_pipeline_stream
import json

app = FastAPI()

# ✅ CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

def event_stream(topic: str):
    for step in run_research_pipeline_stream(topic):
        yield f"data: {json.dumps(step)}\n\n"

@app.get("/research")
def research(topic: str):
    return StreamingResponse(event_stream(topic), media_type="text/event-stream")