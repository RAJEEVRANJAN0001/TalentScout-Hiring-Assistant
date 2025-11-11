"""Gemini API client wrapper."""
import google.generativeai as genai
from typing import List, Dict, Optional
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS
import time


class GeminiClient:
    """Wrapper for Google Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
            }
        )
        self.chat = None
    
    def start_chat(self, history: Optional[List[Dict]] = None):
        """Start a new chat session."""
        if history:
            # Convert history to Gemini format
            gemini_history = []
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            self.chat = self.model.start_chat(history=gemini_history)
        else:
            self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message: str, retry_count: int = 3) -> str:
        """
        Send a message and get response with retry logic.
        
        Args:
            message: The message to send
            retry_count: Number of retries on failure
            
        Returns:
            The response text
        """
        for attempt in range(retry_count):
            try:
                if self.chat is None:
                    self.start_chat()
                
                response = self.chat.send_message(message)
                
                # Extract text from response - handle both simple and multi-part responses
                result_text = self._extract_text_from_response(response)
                if result_text:
                    return result_text
                
                # If we still can't get text, return fallback
                return "I apologize, but I couldn't generate a proper response. Please try again."
            
            except Exception as e:
                if attempt < retry_count - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                else:
                    return f"I apologize, but I'm having trouble processing your request. Please try again. Error: {str(e)}"
    
    def generate_content(self, prompt: str, retry_count: int = 3) -> str:
        """
        Generate content from a prompt without chat context.
        
        Args:
            prompt: The prompt to generate from
            retry_count: Number of retries on failure
            
        Returns:
            The generated text
        """
        for attempt in range(retry_count):
            try:
                response = self.model.generate_content(prompt)
                
                # Check for blocked content or safety issues
                if hasattr(response, 'prompt_feedback'):
                    print(f"Prompt feedback: {response.prompt_feedback}")
                
                # Extract text from response - handle both simple and multi-part responses
                result_text = self._extract_text_from_response(response)
                if result_text:
                    return result_text
                
                # Check finish reason
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'finish_reason'):
                        print(f"Finish reason: {candidate.finish_reason}")
                        if candidate.finish_reason == 3:  # SAFETY
                            return "I apologize, but I need to rephrase that question. Let me ask you something else about your technical experience."
                        elif candidate.finish_reason == 2:  # MAX_TOKENS
                            return "Let me ask you a more focused question about your experience."
                
                # If we still can't get text, return fallback
                return "I apologize, but I couldn't generate a proper response. Please try again."
                
            except Exception as e:
                print(f"Error in generate_content (attempt {attempt + 1}): {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(1)
                    continue
                else:
                    return f"Error generating content: {str(e)}"
    
    def _extract_text_from_response(self, response) -> Optional[str]:
        """
        Extract text from a Gemini API response, handling both simple and multi-part responses.
        
        Args:
            response: The response object from Gemini API
            
        Returns:
            Extracted text or None if extraction failed
        """
        # Try to get text directly first (works for simple responses)
        try:
            text_value = response.text
            if text_value:
                return text_value
        except ValueError:
            # response.text raised ValueError for multi-part response
            # Continue to manual extraction below
            pass
        except AttributeError:
            # No text attribute
            pass
        except Exception:
            # Any other error with response.text
            pass
        
        # Handle multi-part responses by extracting from candidates
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        text_parts = []
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        if text_parts:
                            return ''.join(text_parts)
        except Exception:
            pass
        
        return None
    
    def reset_chat(self):
        """Reset the chat session."""
        self.chat = None
