from fastapi import FastAPI, Query
from queue_module import queue  # Redis Queue instance
from queue_module.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is up and running"}

@app.post("/chat")
def send_chat(query: str = Query(..., description="Chat message")):
    # Redis Queue me task enqueue karo
    job = queue.enqueue(process_query, query)
    return {
        "status": "Your message has been queued successfully.",
        "job_id": job.id
    }
