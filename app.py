"""
TalentScout Hiring Assistant - Main Application
"""

import streamlit as st
from utils.gemini_client import GeminiClient
from utils.conversation_manager import ConversationManager
from config.settings import APP_TITLE, COMPANY_NAME, ConversationState, GEMINI_API_KEY
from utils.ui_components import (
    render_feature_cards, 
    render_progress_ring, 
    render_typing_indicator,
    render_success_animation
)
import time

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling with animated background */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .main {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            padding: 2rem;
        }
        
        /* Card-like containers */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Chat input styling */
        .stChatInputContainer {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 0.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
            color: white;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Title styling */
        h1 {
            color: white;
            text-align: center;
            font-weight: 700;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 0.5rem;
        }
        
        /* Caption styling */
        .stCaption {
            text-align: center;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Progress bar container */
        .progress-container {
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Welcome card */
        .welcome-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
            max-width: 600px;
            margin: 3rem auto;
        }
        
        .welcome-card h2 {
            color: #667eea;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .welcome-card p {
            color: #4a5568;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
        }
        
        /* Info cards */
        .info-card {
            background: rgba(255, 255, 255, 0.1);
            border-left: 4px solid #667eea;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(5px);
        }
        
        /* Success message */
        .success-card {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
            margin: 2rem 0;
        }
        
        /* Spinner customization */
        .stSpinner > div {
            border-color: #667eea !important;
        }
        
        /* Remove streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Chat message role indicators */
        [data-testid="stChatMessageContent"] {
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Smooth fade-in animation for messages */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stChatMessage {
            animation: fadeInUp 0.5s ease-out;
        }
        
        /* Metric card styling */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        [data-testid="stMetricLabel"] {
            color: white !important;
            font-weight: 600;
        }
        
        [data-testid="stMetricValue"] {
            color: white !important;
            font-size: 2rem !important;
            font-weight: 700;
        }
        
        /* Pulse animation for avatar */
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .stChatMessage img {
            animation: pulse 2s ease-in-out infinite;
        }
        
        /* Hover effect for info cards */
        .info-card:hover {
            background: rgba(255, 255, 255, 0.15);
            transition: background 0.3s ease;
        }
        
        /* Loading animation enhancement */
        .stSpinner > div > div {
            border-top-color: #667eea !important;
            border-right-color: #764ba2 !important;
        }
        
        /* Input focus effect */
        .stChatInputContainer:focus-within {
            box-shadow: 0 0 0 2px #667eea;
            transition: box-shadow 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.gemini_client = None
        st.session_state.conversation_manager = None
        st.session_state.conversation_started = False
        st.session_state.user_input_key = 0

def check_api_key():
    return bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")

def start_conversation():
    try:
        st.session_state.gemini_client = GeminiClient()
        st.session_state.conversation_manager = ConversationManager(st.session_state.gemini_client)
        st.session_state.conversation_started = True
        greeting = st.session_state.conversation_manager.process_message("")
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    except Exception as e:
        st.error(f"Error: {e}")

def reset_conversation():
    st.session_state.messages = []
    st.session_state.conversation_manager = None
    st.session_state.conversation_started = False
    st.session_state.user_input_key += 1
    st.rerun()

def main():
    initialize_session_state()
    load_custom_css()
    
    # Header
    st.title("TalentScout Hiring Assistant")
    st.markdown('<p class="stCaption">AI-Powered Candidate Screening Platform</p>', unsafe_allow_html=True)
    
    if not check_api_key():
        st.error("API key not configured. Please check your .env file.")
        return
    
    # Sidebar with enhanced UI
    with st.sidebar:
        st.markdown("### Interview Dashboard")
        st.markdown("---")
        
        if st.session_state.conversation_started and st.session_state.conversation_manager:
            mgr = st.session_state.conversation_manager
            
            # Current stage
            st.markdown(f"""
                <div class="info-card">
                    <h4>Current Stage</h4>
                    <p style="font-size: 1.1rem; font-weight: 600;">{mgr.get_state_description()}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Progress indicator with circular ring
            progress = mgr.candidate.get_completion_percentage()
            st.markdown("#### Completion Progress")
            render_progress_ring(progress, "Complete")
            
            # Candidate info (if available)
            if mgr.candidate.full_name:
                st.markdown("---")
                st.markdown("#### Candidate Information")
                if mgr.candidate.full_name:
                    st.markdown(f"**Name:** {mgr.candidate.full_name}")
                if mgr.candidate.email:
                    st.markdown(f"**Email:** {mgr.candidate.email}")
                if mgr.candidate.years_experience is not None:
                    st.markdown(f"**Experience:** {mgr.candidate.years_experience} years")
                if mgr.candidate.desired_positions:
                    st.markdown(f"**Position:** {', '.join(mgr.candidate.desired_positions)}")
            
            st.markdown("---")
            
            # Actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Reset", use_container_width=True):
                    reset_conversation()
            with col2:
                if st.button("Export", use_container_width=True):
                    st.info("Export feature coming soon!")
        else:
            st.markdown("""
                <div class="info-card">
                    <h4>Welcome!</h4>
                    <p>Start the interview to begin the candidate screening process.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### Interview Process")
            st.markdown("""
                1. **Basic Information** - Name, email, phone
                2. **Experience Details** - Years & position
                3. **Technical Skills** - Tech stack
                4. **Technical Assessment** - Q&A
                5. **Wrap Up** - Final questions
            """)
        
        # Footer info
        st.markdown("---")
        st.markdown("#### About")
        st.markdown(f"""
            <small>
            <b>{COMPANY_NAME}</b><br>
            Powered by Google Gemini AI<br>
            Version 1.0
            </small>
        """, unsafe_allow_html=True)
    
    # Main content area
    if not st.session_state.conversation_started:
        # Welcome screen with enhanced UI
        st.markdown("""
            <div class="welcome-card">
                <h2>Welcome to TalentScout</h2>
                <p>
                    Our AI-powered hiring assistant will guide you through a comprehensive 
                    screening interview. The process typically takes 10-15 minutes.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        render_feature_cards()
        
        # Center the start button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start Interview", use_container_width=True, type="primary"):
                start_conversation()
                st.rerun()
    else:
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            for msg in st.session_state.messages:
                if msg["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("user"):
                        st.markdown(msg["content"])
        
        # Input area
        if st.session_state.conversation_manager.state != ConversationState.ENDED:
            user_input = st.chat_input("Type your response here...", key=f"chat_input_{st.session_state.user_input_key}")
            
            if user_input:
                # Display user message immediately
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Show typing indicator
                with st.chat_message("assistant"):
                    render_typing_indicator()
                
                with st.spinner("Processing your response..."):
                    response = st.session_state.conversation_manager.process_message(user_input)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        else:
            # Interview completed with animation
            st.markdown("""
                <div class="success-card">
                    <h2>Interview Completed!</h2>
                    <p style="font-size: 1.2rem; margin-top: 1rem;">
                        Thank you for completing the screening interview. 
                        Our team will review your responses and get back to you soon.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Show success animation
            render_success_animation()
            
            # Show summary
            if st.session_state.conversation_manager:
                mgr = st.session_state.conversation_manager
                st.markdown("---")
                st.markdown("### Interview Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Questions Answered", mgr.questions_asked)
                with col2:
                    st.metric("Tech Skills", len(mgr.candidate.tech_stack) if mgr.candidate.tech_stack else 0)
                with col3:
                    st.metric("Completion", f"{mgr.candidate.get_completion_percentage()}%")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Start New Interview", use_container_width=True, type="primary"):
                    reset_conversation()

if __name__ == "__main__":
    main()
