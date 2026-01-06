from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.post("/chat")
async def chat(user_msg: UserMessage):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_msg.message}
            ]
        )

        reply = response.choices[0].message.content
        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
