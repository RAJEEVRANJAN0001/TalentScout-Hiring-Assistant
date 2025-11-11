"""Application settings and configuration."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "TalentScout Hiring Assistant")
COMPANY_NAME = os.getenv("COMPANY_NAME", "TalentScout")
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"  # Fast, stable, and efficient for conversations
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 8192  # Increased to handle multiple technology questions

# Conversation States
class ConversationState:
    """Enum for conversation states."""
    GREETING = "greeting"
    COLLECT_NAME = "collect_name"
    COLLECT_EMAIL = "collect_email"
    COLLECT_PHONE = "collect_phone"
    COLLECT_EXPERIENCE = "collect_experience"
    COLLECT_POSITION = "collect_position"
    COLLECT_LOCATION = "collect_location"
    COLLECT_TECH_STACK = "collect_tech_stack"
    TECHNICAL_QA = "technical_qa"
    WRAP_UP = "wrap_up"
    ENDED = "ended"

# Exit keywords
EXIT_KEYWORDS = ["bye", "exit", "quit", "stop", "end", "goodbye", "no thanks"]

# Tech stacks for validation (common technologies)
COMMON_TECH_STACKS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
    "React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Spring Boot",
    "Node.js", "Express", "Next.js", "SQL", "PostgreSQL", "MySQL", "MongoDB",
    "Redis", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux"
]
