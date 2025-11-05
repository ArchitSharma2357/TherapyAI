# Therapy AI Chat Frontend

Static HTML/JS frontend for the Therapy AI Chat application.

## Setup

1. Serve the files using a static server. For example:
   ```
   cd frontend
   python -m http.server 8000
   ```

2. Open http://localhost:8000 in your browser.

## Configuration

Update the `BACKEND_URL` in `script.js` to point to your deployed backend API.

For local testing:
```javascript
const BACKEND_URL = 'http://localhost:8000';
```

For production (Railway):
```javascript
const BACKEND_URL = 'https://your-backend-project.railway.app';
```

## Deployment on Railway

1. Push this code to a GitHub repository.
2. Connect the repository to a new Railway project.
3. Railway will automatically detect it as a static site and deploy it.
4. Set environment variables if needed (e.g., for backend URL).
5. The frontend will be accessible via the Railway URL.
