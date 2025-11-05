from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os
from pydantic import BaseModel
from typing import List, Tuple

# Set Hugging Face cache directory to /tmp for Railway (ephemeral, but models download each deploy)
os.environ['HF_HOME'] = '/tmp/hf_cache'

app = FastAPI(title="Therapy AI Chat Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for lazy loading
tokenizer = None
model = None
device = "cpu"  # Force CPU for Railway

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        try:
            # Load base model and tokenizer
            base_model_name = "gpt2-medium"
            tokenizer = AutoTokenizer.from_pretrained(base_model_name)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            # Load base model
            base_model = AutoModelForCausalLM.from_pretrained(base_model_name).to(device)

            # Load PEFT adapter from current directory
            adapter_path = "./"
            model = PeftModel.from_pretrained(base_model, adapter_path).to(device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

class ChatRequest(BaseModel):
    message: str
    history: List[Tuple[str, str]] = []

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Load model if not already loaded
        load_model()

        # Build conversation history
        conversation = ""
        for user_msg, assistant_msg in request.history:
            conversation += f"User: {user_msg}\nAssistant: {assistant_msg}\n"
        conversation += f"User: {request.message}\nAssistant:"

        # Tokenize input
        inputs = tokenizer(conversation, return_tensors="pt", truncation=True, max_length=512).to(device)

        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=100,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the new assistant response
        assistant_response = full_response.split("Assistant:")[-1].strip()

        return {"response": assistant_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Therapy AI Chat Backend API"}
