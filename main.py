import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from hf_client import HuggingFaceClient
load_dotenv()

HF_MODEL = os.getenv("HF_MODEL", "facebook/blenderbot-400M-distill")
app = FastAPI(title="Intelligent Customer Support Agent")
app.mount("/static", StaticFiles(directory="static"), name="static")

hf = HuggingFaceClient(token=os.getenv("HF_API_TOKEN"), model=HF_MODEL, timeout=int(os.getenv("HF_TIMEOUT") or 60))

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message", "")
    if not user_message:
        return JSONResponse({"error":"No message provided"}, status_code=400)

    # Basic prompt construction: include system instructions and user's message.
    prompt = f"You are a helpful customer support assistant. Answer concisely and politely.\nUser: {user_message}\nAssistant:"
    try:
        output = hf.generate(prompt=prompt, max_length=512)
        return JSONResponse({"reply": output})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)