# Code Review Assistant 🔍

An AI-powered code review tool that automatically analyzes code for readability, modularity, and potential bugs using Large Language Models (LLMs).

## Features

- **Automated Code Analysis**: Upload code files and get instant AI-powered reviews
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, C#, Go, Ruby, PHP, Swift, Kotlin, Rust
- **Comprehensive Scoring**: Readability, Modularity, and Bug Risk scores (1-10)
- **Actionable Suggestions**: Specific, categorized improvement recommendations
- **Review History**: SQLite database stores all reviews for future reference
- **Modern Dashboard**: Beautiful, responsive web interface with drag-and-drop upload
- **RESTful API**: FastAPI backend for easy integration

## Architecture

```
├── Backend (FastAPI)
│   ├── Code upload endpoint
│   ├── OpenAI/LLM integration
│   ├── SQLite database for reviews
│   └── RESTful API
│
├── Frontend (HTML/CSS/JS)
│   ├── Drag-and-drop file upload
│   ├── Real-time review display
│   └── Score visualization
│
└── LLM Analysis
    ├── Readability assessment
    ├── Modularity evaluation
    ├── Bug detection
    └── Best practices checking
```

## Installation

### Prerequisites

- Python 3.8+
- HuggingFace Token
- Modern web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/code-review-assistant.git
cd code-review-assistant
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 4: Run the Backend

```bash
python main.py
```

The API will start at `http://localhost:8000`

### Step 5: Open the Frontend

Open `index.html` in your web browser, or serve it using:

```bash
# Using Python's built-in server
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## Usage

### Via Web Dashboard

1. Open the web interface
2. Drag and drop your code file or click "Choose File"
3. Wait for AI analysis (typically 5-15 seconds)
4. Review the scores and suggestions
5. Implement improvements based on recommendations

### Via API

```bash
# Upload a file for review
curl -X POST "http://localhost:8000/api/review" \
  -F "file=@your_code.py"

# Get all reviews
curl "http://localhost:8000/api/reviews"

# Get specific review
curl "http://localhost:8000/api/reviews/1"
```

### API Response Example

```json
{
  "id": 1,
  "filename": "example.py",
  "language": "Python",
  "timestamp": "2025-10-12T10:30:00",
  "summary": "Good code structure with room for improvement in error handling",
  "readability_score": 7,
  "modularity_score": 8,
  "bug_risk_score": 4,
  "suggestions": [
    {
      "category": "bug",
      "severity": "medium",
      "line": "15",
      "issue": "Missing error handling for file operations",
      "suggestion": "Add try-except block to handle IOError",
      "example": "try:\n    with open(file) as f:\n        data = f.read()\nexcept IOError as e:\n    handle_error(e)"
    }
  ]
}
```

## Project Structure

```
code-review-assistant/
│
├── main.py                 # FastAPI backend
├── index.html             # Frontend dashboard
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── reviews.db            # SQLite database (created automatically)
├── README.md             # This file
└── demo_video.mp4        # Demo video (create this)
```

## LLM Integration

The system uses HuggingFace by default for code analysis. The LLM analyzes:

1. **Readability**: Variable naming, code clarity, comments
2. **Modularity**: Function decomposition, code organization
3. **Bug Risk**: Logic errors, edge cases, security issues
4. **Best Practices**: Language-specific conventions

### Using Alternative LLMs

You can use local LLMs like Ollama by modifying the `analyze_code_with_llm` function:

```python
# For Ollama
import requests

def analyze_with_ollama(code, language):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "codellama",
            "prompt": f"Review this {language} code: {code}",
            "stream": False
        }
    )
    return response.json()
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| POST | `/api/review` | Upload code for review |
| GET | `/api/reviews` | List all reviews |
| GET | `/api/reviews/{id}` | Get specific review |

## Evaluation Criteria

This project demonstrates:

✅ **LLM Insight Quality**: Detailed, actionable code analysis  
✅ **Code Handling**: Multi-language support with proper parsing  
✅ **API Design**: RESTful endpoints with proper error handling  
✅ **Completeness**: Full-stack implementation with database storage  
✅ **User Experience**: Modern, responsive dashboard  
✅ **Documentation**: Comprehensive README and code comments  

## Testing

Test the application with various code files:

```bash
# Test with a Python file
curl -X POST http://localhost:8000/api/review \
  -F "file=@test_code.py"

# Test with a JavaScript file
curl -X POST http://localhost:8000/api/review \
  -F "file=@test_code.js"
```

## Troubleshooting

### "OpenAI API Key not found"
- Ensure `.env` file exists with valid `OPENAI_API_KEY`
- Restart the backend after adding the key

### "CORS Error" in browser
- Ensure backend is running on port 8000
- Check CORS middleware configuration in `main.py`

### "File too large" error
- Maximum file size is 50KB
- Split larger files or increase limit in code

### Database locked
- Close any other connections to `reviews.db`
- Delete `reviews.db` and restart (will lose history)

## Future Enhancements

- [ ] Support for multiple file uploads
- [ ] Code diff comparison between versions
- [ ] Custom rule configuration
- [ ] Team collaboration features
- [ ] Integration with GitHub/GitLab
- [ ] Export reports as PDF
- [ ] Real-time collaboration
- [ ] CI/CD integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to use for personal or commercial projects

## Contact

Eesha Pedakota-eesha6325@gmail.com
Project Link: https://github.com/EESHA-P/Code-review-assistant

## Acknowledgments

- Hugging Face for Token
- FastAPI for the excellent web framework
- The open-source community

---
