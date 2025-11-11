"""Conversation manager for handling chat flow and state."""
from typing import List, Dict, Optional
import re
from models import CandidateInfo
from config.settings import ConversationState, EXIT_KEYWORDS, MAX_CONTEXT_MESSAGES
from utils.gemini_client import GeminiClient
from prompts import (
    SYSTEM_PROMPT, 
    GREETING_PROMPT, 
    FALLBACK_PROMPT, 
    EXIT_CONFIRMATION_PROMPT,
    TECH_STACK_ACKNOWLEDGMENT
)
from prompts.question_generator import (
    generate_technical_questions_prompt,
    generate_followup_question_prompt
)


class ConversationManager:
    """Manages conversation flow and state transitions."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize conversation manager.
        
        Args:
            gemini_client: Instance of GeminiClient
        """
        self.client = gemini_client
        self.state = ConversationState.GREETING
        self.candidate = CandidateInfo()
        self.conversation_history: List[Dict[str, str]] = []
        self.current_tech_index = 0
        self.questions_asked = 0
        self.max_questions_per_tech = 3
        
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only last N messages for context
        if len(self.conversation_history) > MAX_CONTEXT_MESSAGES * 2:
            self.conversation_history = self.conversation_history[-MAX_CONTEXT_MESSAGES * 2:]
    
    def check_exit_intent(self, user_input: str) -> bool:
        """Check if user wants to exit."""
        user_lower = user_input.lower().strip()
        return any(keyword in user_lower for keyword in EXIT_KEYWORDS)
    
    def process_message(self, user_input: str) -> str:
        """
        Process user message and generate response.
        
        Args:
            user_input: User's message
            
        Returns:
            Bot's response
        """
        user_input = user_input.strip()
        
        # Check for exit intent
        if self.check_exit_intent(user_input) and self.state != ConversationState.GREETING:
            self.state = ConversationState.ENDED
            prompt = EXIT_CONFIRMATION_PROMPT.format(user_input=user_input)
            response = self.client.generate_content(prompt)
            self.add_to_history("user", user_input)
            self.add_to_history("assistant", response)
            return response
        
        # Handle based on current state
        if self.state == ConversationState.GREETING:
            return self._handle_greeting()
        
        elif self.state == ConversationState.COLLECT_NAME:
            return self._handle_name_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_EMAIL:
            return self._handle_email_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_PHONE:
            return self._handle_phone_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_EXPERIENCE:
            return self._handle_experience_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_POSITION:
            return self._handle_position_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_LOCATION:
            return self._handle_location_collection(user_input)
        
        elif self.state == ConversationState.COLLECT_TECH_STACK:
            return self._handle_tech_stack_collection(user_input)
        
        elif self.state == ConversationState.TECHNICAL_QA:
            return self._handle_technical_qa(user_input)
        
        elif self.state == ConversationState.WRAP_UP:
            return self._handle_wrap_up(user_input)
        
        return "I'm not sure how to respond to that. Could you please clarify?"
    
    def _handle_greeting(self) -> str:
        """Handle initial greeting."""
        response = self.client.generate_content(GREETING_PROMPT)
        self.add_to_history("assistant", response)
        self.state = ConversationState.COLLECT_NAME
        return response
    
    def _handle_name_collection(self, user_input: str) -> str:
        """Handle name collection."""
        try:
            self.candidate.full_name = user_input
            self.add_to_history("user", user_input)
            response = f"Nice to meet you, {self.candidate.full_name}!\n\nCould you please provide your email address?"
            self.add_to_history("assistant", response)
            self.state = ConversationState.COLLECT_EMAIL
            return response
        except ValueError as e:
            self.add_to_history("user", user_input)
            response = f"I noticed an issue with the name format: {str(e)}\n\nCould you please provide your full name again?"
            self.add_to_history("assistant", response)
            return response
    
    def _handle_email_collection(self, user_input: str) -> str:
        """Handle email collection."""
        try:
            self.candidate.email = user_input
            self.add_to_history("user", user_input)
            response = f"Thank you! I've noted your email as {self.candidate.email}.\n\nWhat's your phone number?"
            self.add_to_history("assistant", response)
            self.state = ConversationState.COLLECT_PHONE
            return response
        except ValueError as e:
            self.add_to_history("user", user_input)
            response = f"That doesn't appear to be a valid email address. Please provide a valid email (e.g., name@example.com)."
            self.add_to_history("assistant", response)
            return response
    
    def _handle_phone_collection(self, user_input: str) -> str:
        """Handle phone collection."""
        try:
            self.candidate.phone = user_input
            self.add_to_history("user", user_input)
            response = f"Perfect! I've saved your phone number.\n\nHow many years of professional experience do you have? (Please provide a number)"
            self.add_to_history("assistant", response)
            self.state = ConversationState.COLLECT_EXPERIENCE
            return response
        except ValueError as e:
            self.add_to_history("user", user_input)
            response = "Please provide a valid phone number (e.g., +1234567890 or 123-456-7890)."
            self.add_to_history("assistant", response)
            return response
    
    def _handle_experience_collection(self, user_input: str) -> str:
        """Handle years of experience collection."""
        try:
            # Extract number from input
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                years = int(numbers[0])
                self.candidate.years_experience = years
                self.add_to_history("user", user_input)
                
                exp_level = "beginner" if years < 2 else "intermediate" if years < 5 else "senior"
                response = f"Great! {years} years of experience - that's {exp_level} level.\n\nWhat position(s) are you interested in? (You can list multiple positions separated by commas)"
                self.add_to_history("assistant", response)
                self.state = ConversationState.COLLECT_POSITION
                return response
            else:
                raise ValueError("No number found")
        except (ValueError, IndexError):
            self.add_to_history("user", user_input)
            response = "Please provide your years of experience as a number (e.g., 3 or 5 years)."
            self.add_to_history("assistant", response)
            return response
    
    def _handle_position_collection(self, user_input: str) -> str:
        """Handle desired position collection."""
        positions = [p.strip() for p in user_input.split(',')]
        self.candidate.desired_positions = positions
        self.add_to_history("user", user_input)
        
        if len(positions) == 1:
            response = f"Excellent! You're looking for a {positions[0]} role.\n\nWhere are you currently located?"
        else:
            response = f"Excellent! You're interested in: {', '.join(positions)}.\n\nWhere are you currently located?"
        
        self.add_to_history("assistant", response)
        self.state = ConversationState.COLLECT_LOCATION
        return response
    
    def _handle_location_collection(self, user_input: str) -> str:
        """Handle location collection."""
        try:
            self.candidate.current_location = user_input
            self.add_to_history("user", user_input)
            response = (f"Perfect! I've noted that you're in {self.candidate.current_location}.\n\n"
                       f"Now, let's talk about your technical skills.\n\n"
                       f"Please list the programming languages, frameworks, databases, and tools you're proficient in. "
                       f"(e.g., Python, React, PostgreSQL, Docker)")
            self.add_to_history("assistant", response)
            self.state = ConversationState.COLLECT_TECH_STACK
            return response
        except ValueError as e:
            self.add_to_history("user", user_input)
            response = "Please provide your current location (city or city, country)."
            self.add_to_history("assistant", response)
            return response
    
    def _handle_tech_stack_collection(self, user_input: str) -> str:
        """Handle tech stack collection."""
        # Parse tech stack from input
        tech_stack = [tech.strip() for tech in re.split(r'[,;\n]', user_input) if tech.strip()]
        self.candidate.tech_stack = tech_stack
        self.add_to_history("user", user_input)
        
        # Generate acknowledgment
        tech_list = ", ".join(tech_stack)
        acknowledgment = f"Impressive tech stack! I see you work with: {tech_list}.\n\n"
        
        # Generate technical questions
        prompt = generate_technical_questions_prompt(tech_stack, self.candidate.years_experience or 0)
        questions_response = self.client.generate_content(prompt)
        
        # Fallback if AI fails
        if not questions_response or "couldn't generate" in questions_response.lower() or "error" in questions_response.lower():
            questions_response = self._generate_fallback_questions(tech_stack)
        
        response = acknowledgment + questions_response
        self.add_to_history("assistant", response)
        self.state = ConversationState.TECHNICAL_QA
        self.current_tech_index = 0
        self.questions_asked = 1
        
        return response
    
    def _generate_fallback_questions(self, tech_stack: list) -> str:
        """Generate simple fallback questions if AI fails."""
        if not tech_stack:
            return "Let's talk about your experience. What projects have you worked on?"
        
        first_tech = tech_stack[0]
        return (f"Great! Let's dive into some technical questions.\n\n"
                f"Let's start with {first_tech}. Can you tell me about a recent project "
                f"where you used {first_tech}? What was your role and what challenges did you face?")
    
    def _handle_technical_qa(self, user_input: str) -> str:
        """Handle technical Q&A."""
        self.add_to_history("user", user_input)
        
        # Store the answer
        if self.candidate.tech_stack:
            tech = self.candidate.tech_stack[min(self.current_tech_index, len(self.candidate.tech_stack) - 1)]
            if tech not in self.candidate.technical_responses:
                self.candidate.technical_responses[tech] = []
            self.candidate.technical_responses[tech].append(user_input)
        
        # Check if we should continue with questions
        self.questions_asked += 1
        total_questions_needed = min(len(self.candidate.tech_stack or []) * self.max_questions_per_tech, 15)
        
        if self.questions_asked >= total_questions_needed:
            # Move to wrap up
            self.state = ConversationState.WRAP_UP
            response = (f"Thank you for your detailed answers! 🎉\n\n"
                       f"You've done great in this initial screening. "
                       f"Our team will review your responses and get back to you within 2-3 business days.\n\n"
                       f"Is there anything you'd like to ask about the position or our process?")
            self.add_to_history("assistant", response)
            return response
        
        # Generate next question
        if self.candidate.tech_stack:
            tech = self.candidate.tech_stack[self.current_tech_index % len(self.candidate.tech_stack)]
            prompt = generate_followup_question_prompt(tech, user_input, self.candidate.years_experience or 0)
            response = self.client.generate_content(prompt)
            
            self.current_tech_index += 1
            self.add_to_history("assistant", response)
            return response
        
        return "Thank you for your answer. Let's continue."
    
    def _handle_wrap_up(self, user_input: str) -> str:
        """Handle wrap-up phase."""
        self.add_to_history("user", user_input)
        
        # Check if they have a question
        if "?" in user_input or any(word in user_input.lower() for word in ["what", "when", "where", "how", "why", "who"]):
            # Generate answer to their question
            context = f"The candidate asked: {user_input}\n\nProvide a brief, helpful answer about the hiring process, timeline, or next steps. Keep it professional and encouraging."
            response = self.client.generate_content(context)
            response += "\n\nIs there anything else you'd like to know?"
        else:
            # Final goodbye
            response = (f"Thank you so much for your time today, {self.candidate.full_name}!\n\n"
                       f"We're excited about your candidacy and will be in touch soon. "
                       f"Have a wonderful day!\n\n"
                       f"Best regards,\nTalentScout Team")
            self.state = ConversationState.ENDED
        
        self.add_to_history("assistant", response)
        return response
    
    def get_state_description(self) -> str:
        """Get human-readable state description."""
        state_descriptions = {
            ConversationState.GREETING: "Initial Greeting",
            ConversationState.COLLECT_NAME: "Collecting Name",
            ConversationState.COLLECT_EMAIL: "Collecting Email",
            ConversationState.COLLECT_PHONE: "Collecting Phone",
            ConversationState.COLLECT_EXPERIENCE: "Collecting Experience",
            ConversationState.COLLECT_POSITION: "Collecting Position",
            ConversationState.COLLECT_LOCATION: "Collecting Location",
            ConversationState.COLLECT_TECH_STACK: "Collecting Tech Stack",
            ConversationState.TECHNICAL_QA: "Technical Assessment",
            ConversationState.WRAP_UP: "Wrapping Up",
            ConversationState.ENDED: "Conversation Ended"
        }
        return state_descriptions.get(self.state, "Unknown")
