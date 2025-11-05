# Therapy AI Chat Backend

FastAPI backend for the Therapy AI Chat application.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn app:app --reload
   ```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /`: Health check
- `POST /chat`: Send a message and get AI response

### POST /chat

Request body:
```json
{
  "message": "Hello, how are you?",
  "history": [["Hi", "I'm doing well, thank you!"]]
}
```

Response:
```json
{
  "response": "I'm doing well, thank you! How can I help you today?"
}
```

## Deployment on Railway

1. Push this code to a GitHub repository.
2. Connect the repository to a new Railway project.
3. Railway will automatically detect the Python app and use uvicorn to run it.
4. The app will be deployed and accessible via the Railway URL.

### Notes for Railway Deployment
- The app is configured to use CPU only for compatibility with Railway's free tier.
- Models are loaded lazily on first request to avoid timeout during deployment.
- Hugging Face cache is set to `/tmp/hf_cache` which is ephemeral but allows downloads during runtime.
- The PEFT adapter files (adapter_model.safetensors, adapter_config.json, etc.) must be included in the deployment.
