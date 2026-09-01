import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase from Environment Variable (Render Secure Config)
if not firebase_admin._apps:
    firebase_json = os.environ.get("FIREBASE_JSON_CONTENT")
    if firebase_json:
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

# Configure Google Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(
    title="NexusOps AI Backend",
    description="Production-ready backend powered by Gemini AI and Firebase Firestore.",
    version="1.0"
)

class TaskRequest(BaseModel):
    task: str

@app.get("/")
def home():
    return {"status": "NexusOps AI Backend is online and running successfully!"}

@app.post("/run-task")
def run_task(payload: TaskRequest):
    try:
        # Generate AI response using Gemini
        model = genai.GenerativeModel("gemini-3.5-flash")
        prompt = f"You are NexusOps AI, an expert operations assistant. Handle this task professionally:\n\nTask: {payload.task}"
        ai_response = model.generate_content(prompt)
        result_text = ai_response.text

        # Save task and history securely to Firebase Firestore
        try:
            db = firestore.client()
            db.collection("nexus_tasks_history").add({
                "task": payload.task,
                "response": result_text,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as db_error:
            print(f"Firestore save error: {db_error}")

        return {
            "status": "success",
            "task": payload.task,
            "response": result_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))