# TalentScout Hiring Assistant

An AI-powered candidate screening platform built with Streamlit and Google Gemini AI. 


## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Data Validation**: Pydantic v2
- **Backend**: Python 3.10+
- **Environment**: python-dotenv

## Project Structure

```
HRINING/
├── app.py                      # Main Streamlit application
├── config/
│   └── settings.py            # Configuration and constants
├── models/
│   └── __init__.py           # Pydantic data models
├── prompts/
│   ├── __init__.py           # Prompt templates
│   └── question_generator.py # AI question generation prompts
├── utils/
│   ├── conversation_manager.py # Interview flow state machine
│   ├── gemini_client.py       # Google Gemini API wrapper
│   └── ui_components.py       # Reusable UI components
├── .env                        # Environment variables (API keys)
├── .env.example               # Example environment configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

4. **Open Browser**
   Navigate to `http://localhost:8501`

## Configuration

### Environment Variables

Edit `.env` file:

```env
GEMINI_API_KEY=your_actual_api_key_here
APP_TITLE=TalentScout Hiring Assistant
COMPANY_NAME=TalentScout
MAX_CONTEXT_MESSAGES=10
```

### Model Settings

Edit `config/settings.py`:

```python
GEMINI_MODEL = "gemini-2.5-flash"  # Recommended for speed
MAX_OUTPUT_TOKENS = 2048           # Response length limit
TEMPERATURE = 0.7                  # Response creativity
```

## Usage

### Interview Flow

The assistant guides candidates through:

1. **Greeting** - Welcome and introduction
2. **Basic Information** - Name, email, phone
3. **Professional Experience** - Years, positions, location
4. **Technical Skills** - Tech stack evaluation
5. **Technical Assessment** - AI-generated questions
6. **Wrap Up** - Final questions and next steps

### Data Collection

The system collects and validates:
- Full Name
- Email Address  
- Phone Number
- Years of Experience
- Desired Positions
- Current Location
- Technical Skills
- Interview Responses

## Troubleshooting

### Common Issues

**API Key Error**
```bash
# Ensure .env file exists with valid GEMINI_API_KEY
cp .env.example .env
# Edit .env and add your key
```

**Model Not Found (404)**
```python
# Change model in config/settings.py
GEMINI_MODEL = "gemini-2.5-flash"
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

## Performance

### Recommended Settings

**For Speed:**
- Model: `gemini-2.5-flash`
- Tokens: `2048`
- Temperature: `0.7`

**For Quality:**
- Model: `gemini-2.5-pro`
- Tokens: `4096`
- Temperature: `0.8`

## Security

- API keys stored in `.env` (never commit to git)
- Input validation via Pydantic
- Session-only data storage (not persisted)
- Add `.env` to `.gitignore`

## Production Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect Streamlit Cloud
3. Add secrets in dashboard
4. Deploy

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## API Reference

### GeminiClient

```python
from utils.gemini_client import GeminiClient

client = GeminiClient()
response = client.generate_content("Your prompt")
```

### ConversationManager

```python
from utils.conversation_manager import ConversationManager

manager = ConversationManager(gemini_client)
response = manager.process_message(user_input)
progress = manager.candidate.get_completion_percentage()
```

## Customization

### Modify Interview Questions

Edit `prompts/question_generator.py`:

```python
def generate_technical_questions_prompt(tech_stack, experience_years):
    # Customize your questions here
    pass
```

### Update UI Styling

Edit CSS in `app.py`:

```python
def load_custom_css():
    st.markdown("""
        <style>
        /* Your custom CSS */
        </style>
    """, unsafe_allow_html=True)
```

## Project Status

- **Version**: 1.0.0
- **Status**: Production Ready
- **Python**: 3.10+
- **Last Updated**: November 2025

## License

Proprietary software. All rights reserved.

## Support

For issues:
1. Check troubleshooting section
2. Verify API key is valid
3. Ensure Python 3.10+
4. Review configuration settings

## Changelog

### v1.0.0 - November 2025
- Initial release
- AI-powered interview system
- 11-stage conversation flow
- Professional UI
- Progress tracking
- Data validation
- Export-ready structure



---

Built with Streamlit + Google Gemini AI
