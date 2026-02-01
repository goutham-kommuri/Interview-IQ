# Setup and Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- API credentials for AI model provider

## Step-by-Step Installation

### 1. Clone or Download Project

```bash
# Navigate to project directory
cd mock_interview_platform
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

**Important**: The `--pre` flag is required for the Agent Framework package as it's in preview.

```bash
# Install all dependencies including pre-release packages
pip install --pre -r requirements.txt
```

If you encounter issues, install packages individually:

```bash
pip install --pre agent-framework-azure-ai
pip install pydantic>=2.0.0
pip install python-dotenv>=1.0.0
pip install pyyaml>=6.0
```

### 4. Configure Environment

#### Option A: Microsoft Foundry (Azure AI)

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```
FOUNDRY_API_KEY=your_foundry_api_key_here
FOUNDRY_ENDPOINT=https://your-instance.inference.ai.azure.com
FOUNDRY_MODEL_ID=gpt-4o-mini
```

3. Get credentials:
   - Visit [Microsoft Foundry](https://foundry.microsoft.com)
   - Create or select a project
   - Deploy a model (gpt-4o-mini recommended)
   - Copy API key and endpoint

#### Option B: GitHub Models (Recommended for Getting Started)

1. Edit `.env`:
```
GITHUB_TOKEN=your_github_token_here
GITHUB_MODEL=openai/gpt-4o-mini
```

2. Generate GitHub token:
   - Go to GitHub.com → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Copy the token to `.env`

3. No additional setup needed - GitHub Models have free tier!

### 5. Verify Installation

```bash
# Test if all imports work
python -c "
from src.agents import AIInterviewer
from src.core import ResumeAnalyzer, QuestionGenerator
from src.utils import Config
print('✓ All imports successful!')
print('✓ Installation complete!')
"
```

## Running the Platform

### Option 1: Run Demo Interview

```bash
python src/main.py
```

This will:
- Use sample resume and job description
- Run 5 interview questions
- Generate comprehensive report
- Show all evaluation metrics

### Option 2: Interactive Interview

Edit `src/main.py` and change:
```python
interactive=False  # Change to True
```

Then run:
```bash
python src/main.py
```

### Option 3: Programmatic Usage

Create a new Python script:

```python
from src.agents import AIInterviewer
from src.utils import Config

# Initialize
config = Config()
interviewer = AIInterviewer(config)

# Your resume and JD
resume = """Your resume text here"""
jd = """Your job description here"""

# Start interview
init = interviewer.initialize_interview(
    resume, jd,
    candidate_name="John Doe",
    job_title="Senior Engineer"
)

print(f"Interview initialized: {init['message']}")
print(f"Questions: {init['total_questions']}")

# Run interview
# ... implement interview loop ...
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'agent_framework'"

**Solution**: Make sure you installed with `--pre` flag:
```bash
pip install --pre -r requirements.txt
```

### Issue: API Key not found

**Solution**: 
1. Verify `.env` file exists in project root
2. Check credentials are correct
3. Ensure no extra spaces around values:
```
# ✓ Correct
FOUNDRY_API_KEY=abc123

# ✗ Incorrect (spaces matter!)
FOUNDRY_API_KEY = abc123
```

### Issue: "FOUNDRY_API_KEY environment variable not set"

**Solution**: 
1. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```
2. Edit `.env` with your credentials
3. Make sure virtual environment is activated

### Issue: Low evaluation scores in demo

**Solution**: This is normal for auto-generated answers. To test properly:
1. Set `interactive=True` in `src/main.py`
2. Provide detailed, thoughtful answers
3. Take reasonable time for answers (not too quick)

### Issue: Questions not adapting in difficulty

**Solution**: Ensure you're providing varied answer quality:
- First few answers: Provide detailed responses (score >80%)
- Later answers: Provide basic responses (score <50%)
- Observe difficulty changes

## Configuration Options

Edit `.env` to customize:

```bash
# Interview settings
MAX_QUESTIONS=5                        # Number of questions (default: 5)
TIME_PER_QUESTION=120                 # Seconds per question (default: 120)
PASSING_THRESHOLD=60                  # Minimum passing score % (default: 60)
EARLY_TERMINATION_THRESHOLD=40        # Early exit trigger % (default: 40)
```

## Project Structure

```
mock_interview_platform/
├── src/
│   ├── agents/                    # AI agent implementation
│   │   └── ai_interviewer.py
│   ├── core/                      # Core business logic
│   │   ├── resume_analyzer.py
│   │   ├── job_description_analyzer.py
│   │   ├── question_generator.py
│   │   ├── answer_evaluator.py
│   │   └── interview_scorer.py
│   ├── utils/                     # Utilities and helpers
│   │   ├── models.py              # Data structures
│   │   ├── config.py              # Configuration
│   │   └── logger.py              # Logging
│   ├── __init__.py
│   └── main.py                    # Main orchestrator
├── data/
│   └── samples/
│       └── sample_data.py         # Sample resume and JD
├── .env.example                   # Environment template
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

## Next Steps

1. **Explore the code**: Start with `src/main.py` to understand the flow
2. **Customize questions**: Edit `QUESTION_TEMPLATES` in `question_generator.py`
3. **Adjust evaluation**: Modify weights in `interview_scorer.py`
4. **Add your data**: Use your own resume and job description
5. **Integrate with systems**: Extend `AIInterviewer` for your needs

## Advanced Configuration

### Custom Question Templates

Edit `src/core/question_generator.py`:

```python
QUESTION_TEMPLATES = {
    SkillArea.TECHNICAL: {
        "easy": [
            "Your custom question template with {concept}?",
        ],
        ...
    }
}
```

### Modify Evaluation Weights

Edit `src/core/answer_evaluator.py`:

```python
SCORE_WEIGHTS = {
    "accuracy": 0.25,      # Increase importance of accuracy
    "clarity": 0.20,
    "depth": 0.25,
    "relevance": 0.20,
    "time_efficiency": 0.10,
}
```

### Custom Skill Areas

Edit `src/utils/models.py` and add new `SkillArea` enum values

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Check GitHub Issues (if applicable)
4. Verify credentials and installation

## Performance Tips

- Use `gpt-4o-mini` for cost efficiency
- Batch process multiple interviews
- Cache question generation results
- Enable logging for debugging

---

**Setup Complete!** 🎉

You're ready to run mock interviews. Start with:
```bash
python src/main.py
```
