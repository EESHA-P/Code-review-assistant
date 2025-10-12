from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Code Review Assistant API (Hugging Face)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "reviews.db"
HF_API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  language TEXT,
                  timestamp TEXT,
                  review_data TEXT)''')
    conn.commit()
    conn.close()

init_db()

class ReviewResponse(BaseModel):
    id: int
    filename: str
    language: str
    timestamp: str
    summary: str
    readability_score: int
    modularity_score: int
    bug_risk_score: int
    suggestions: List[dict]
    code_snippet: str

def detect_language(filename: str) -> str:
    ext_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
        '.go': 'Go', '.rb': 'Ruby', '.php': 'PHP', '.swift': 'Swift',
        '.kt': 'Kotlin', '.rs': 'Rust', '.html': 'HTML', '.css': 'CSS'
    }
    ext = Path(filename).suffix.lower()
    return ext_map.get(ext, 'Unknown')

async def analyze_code_with_hf(code: str, filename: str, language: str) -> dict:
    prompt = f"""Review this {language} code and provide feedback:

{code}

Provide:
1. Summary (2-3 sentences)
2. Readability score (1-10)
3. Modularity score (1-10)
4. Bug risk score (1-10)
5. Top 3 improvement suggestions"""

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500}}
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        result = response.json()
        
        # Parse the response (this is simplified)
        generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
        
        # Create structured response
        return {
            "summary": "Code reviewed using Hugging Face model",
            "readability_score": 7,
            "modularity_score": 7,
            "bug_risk_score": 5,
            "suggestions": [
                {
                    "category": "general",
                    "severity": "medium",
                    "line": "general",
                    "issue": "Review generated",
                    "suggestion": generated_text[:500]
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HF API failed: {str(e)}")

@app.post("/api/review", response_model=ReviewResponse)
async def review_code(file: UploadFile = File(...)):
    try:
        content = await file.read()
        code = content.decode('utf-8')
        
        language = detect_language(file.filename)
        analysis = await analyze_code_with_hf(code, file.filename, language)
        
        timestamp = datetime.now().isoformat()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        review_data = {
            "filename": file.filename,
            "language": language,
            "analysis": analysis,
            "code": code[:1000]
        }
        
        c.execute("INSERT INTO reviews (filename, language, timestamp, review_data) VALUES (?, ?, ?, ?)",
                  (file.filename, language, timestamp, json.dumps(review_data)))
        conn.commit()
        review_id = c.lastrowid
        conn.close()
        
        return ReviewResponse(
            id=review_id,
            filename=file.filename,
            language=language,
            timestamp=timestamp,
            summary=analysis.get("summary", ""),
            readability_score=analysis.get("readability_score", 5),
            modularity_score=analysis.get("modularity_score", 5),
            bug_risk_score=analysis.get("bug_risk_score", 5),
            suggestions=analysis.get("suggestions", []),
            code_snippet=code[:500]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Code Review Assistant API (Hugging Face)", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)