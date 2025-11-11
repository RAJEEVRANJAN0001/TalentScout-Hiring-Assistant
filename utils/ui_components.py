"""
Custom UI components for TalentScout Hiring Assistant
"""

import streamlit as st


def render_animated_header():
    """Render an animated header with gradient background"""
    st.markdown("""
        <style>
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .animated-header {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .animated-header h1 {
            color: white;
            margin: 0;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .animated-header p {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.3rem;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)


def render_feature_cards():
    """Render feature cards showing benefits using Streamlit columns"""
    
    # Add CSS for individual cards
    st.markdown("""
        <style>
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            margin: 0.5rem 0;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .feature-title {
            color: #667eea;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .feature-desc {
            color: #4a5568;
            font-size: 1rem;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Use Streamlit columns for better compatibility
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Fast Screening</div>
                <div class="feature-desc">Complete the interview in just 10-15 minutes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">Smart Questions</div>
                <div class="feature-desc">AI-powered technical assessment tailored to your skills</div>
            </div>
        """, unsafe_allow_html=True)


def render_progress_ring(percentage, label):
    """Render a circular progress indicator"""
    st.markdown(f"""
        <style>
        .progress-ring-container {{
            text-align: center;
            margin: 1rem 0;
        }}
        
        .progress-ring {{
            position: relative;
            width: 120px;
            height: 120px;
            margin: 0 auto;
        }}
        
        .progress-ring-circle {{
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
        }}
        
        .progress-ring-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.8rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .progress-label {{
            margin-top: 1rem;
            font-size: 1rem;
            color: white;
            font-weight: 600;
        }}
        </style>
        
        <div class="progress-ring-container">
            <svg class="progress-ring" width="120" height="120">
                <circle
                    class="progress-ring-circle"
                    stroke="#e2e8f0"
                    stroke-width="10"
                    fill="transparent"
                    r="50"
                    cx="60"
                    cy="60"
                />
                <circle
                    class="progress-ring-circle"
                    stroke="#667eea"
                    stroke-width="10"
                    fill="transparent"
                    r="50"
                    cx="60"
                    cy="60"
                    stroke-dasharray="{314 * percentage / 100} 314"
                    stroke-linecap="round"
                />
            </svg>
            <div class="progress-ring-text">{percentage}%</div>
            <div class="progress-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_stage_timeline(current_stage, all_stages):
    """Render a visual timeline of interview stages"""
    stage_emojis = {
        "Initial Greeting": "👋",
        "Collecting Name": "✍️",
        "Collecting Email": "📧",
        "Collecting Phone": "📱",
        "Collecting Experience": "💼",
        "Collecting Position": "🎯",
        "Collecting Location": "📍",
        "Collecting Tech Stack": "🛠️",
        "Technical Assessment": "💻",
        "Wrapping Up": "🎉",
        "Conversation Ended": "✅"
    }
    
    current_idx = all_stages.index(current_stage) if current_stage in all_stages else 0
    
    timeline_html = '<div class="timeline">'
    for idx, stage in enumerate(all_stages):
        status = "completed" if idx < current_idx else "current" if idx == current_idx else "pending"
        emoji = stage_emojis.get(stage, "📌")
        
        timeline_html += f"""
            <div class="timeline-item {status}">
                <div class="timeline-marker">{emoji}</div>
                <div class="timeline-content">{stage}</div>
            </div>
        """
    
    timeline_html += '</div>'
    
    st.markdown("""
        <style>
        .timeline {
            position: relative;
            padding: 1rem 0;
        }
        
        .timeline-item {
            display: flex;
            align-items: center;
            margin: 1rem 0;
            opacity: 0.5;
            transition: opacity 0.3s ease;
        }
        
        .timeline-item.completed,
        .timeline-item.current {
            opacity: 1;
        }
        
        .timeline-marker {
            font-size: 1.5rem;
            margin-right: 1rem;
            min-width: 40px;
        }
        
        .timeline-content {
            font-size: 0.95rem;
            font-weight: 500;
        }
        
        .timeline-item.current .timeline-content {
            color: #667eea;
            font-weight: 700;
        }
        
        .timeline-item.completed .timeline-content {
            color: #10b981;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(timeline_html, unsafe_allow_html=True)


def render_typing_indicator():
    """Render animated typing indicator"""
    st.markdown("""
        <style>
        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 1rem;
        }
        
        .typing-indicator span {
            height: 10px;
            width: 10px;
            background-color: #667eea;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.7;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }
        </style>
        
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    """, unsafe_allow_html=True)


def render_success_animation():
    """Render success animation"""
    st.markdown("""
        <style>
        @keyframes checkmark {
            0% {
                stroke-dashoffset: 50;
            }
            100% {
                stroke-dashoffset: 0;
            }
        }
        
        .success-checkmark {
            width: 80px;
            height: 80px;
            margin: 0 auto;
        }
        
        .success-checkmark circle {
            stroke: #10b981;
            stroke-width: 3;
            fill: none;
            animation: checkmark 0.6s ease-in-out;
        }
        
        .success-checkmark path {
            stroke: #10b981;
            stroke-width: 3;
            fill: none;
            stroke-dasharray: 50;
            stroke-dashoffset: 50;
            animation: checkmark 0.6s 0.3s ease-in-out forwards;
        }
        </style>
        
        <svg class="success-checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
            <circle cx="26" cy="26" r="25"/>
            <path fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
        </svg>
    """, unsafe_allow_html=True)


def render_info_tooltip(text, tooltip_text):
    """Render text with info tooltip"""
    st.markdown(f"""
        <style>
        .tooltip-container {{
            position: relative;
            display: inline-block;
        }}
        
        .tooltip-icon {{
            display: inline-block;
            width: 18px;
            height: 18px;
            background-color: #667eea;
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 18px;
            font-size: 12px;
            font-weight: bold;
            cursor: help;
            margin-left: 5px;
        }}
        
        .tooltip-text {{
            visibility: hidden;
            width: 200px;
            background-color: #2d3748;
            color: white;
            text-align: center;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .tooltip-container:hover .tooltip-text {{
            visibility: visible;
            opacity: 1;
        }}
        </style>
        
        <div class="tooltip-container">
            {text}
            <span class="tooltip-icon">i</span>
            <span class="tooltip-text">{tooltip_text}</span>
        </div>
    """, unsafe_allow_html=True)
