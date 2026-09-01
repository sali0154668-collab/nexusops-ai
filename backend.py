import os
import json

firebase_key_content = os.environ.get("FIREBASE_JSON_CONTENT")
if firebase_key_content and not os.path.exists("nexusops-ai-1c0fe-firebase-adminsdk-fbsvc-70cd876441.json"):
    with open("nexusops-ai-1c0fe-firebase-adminsdk-fbsvc-70cd876441.json", "w") as f:
        f.write(firebase_key_content)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase connection initialize karo
cred = credentials.Certificate(
    "nexusops-ai-1c0fe-firebase-adminsdk-fbsvc-70cd876441.json"
)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Apni Gemini API key
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class TaskRequest(BaseModel):
  task: str


@app.post("/run-task")
def run_agent(request: TaskRequest):
  try:
    model = genai.GenerativeModel("gemini-3.5-flash")
    prompt_text = f"Current Year is 2026. Task: {request.task}"
    response = model.generate_content(prompt_text)

    # Yeh Firestore database mein chat save kar dega
    db.collection("tasks").add({
        "task": request.task,
        "result": response.text,
        "timestamp": firestore.SERVER_TIMESTAMP,
    })

    return {"result": response.text}
  except Exception as e:
    return {"result": f"Gemini Error: {str(e)}"}