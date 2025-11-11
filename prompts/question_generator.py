"""Technical question generation prompts."""

def generate_technical_questions_prompt(tech_stack: list, years_experience: int) -> str:
    """
    Generate prompt for creating technical questions.
    
    Args:
        tech_stack: List of technologies
        years_experience: Candidate's years of experience
        
    Returns:
        Formatted prompt for question generation
    """
    experience_level = "beginner" if years_experience < 2 else "intermediate" if years_experience < 5 else "advanced"
    
    # Limit to first 3-4 technologies to avoid token limits
    limited_stack = tech_stack[:4] if len(tech_stack) > 4 else tech_stack
    tech_list = ", ".join(limited_stack)
    
    prompt = f"""You are conducting a technical interview for a candidate with {years_experience} years of experience ({experience_level} level).

Their tech stack includes: {tech_list}

Generate a conversational interview response that:
1. Starts with: "Great! Let's dive into some technical questions."
2. Asks ONE specific question about the FIRST technology ({limited_stack[0]})
3. The question should be appropriate for {experience_level} level
4. Keep it conversational and friendly
5. Maximum 3-4 sentences total

Example format:
"Great! Let's dive into some technical questions. Let's start with [technology]. [Your specific question here]"

Generate the response now:"""
    
    return prompt


def generate_followup_question_prompt(tech: str, previous_answer: str, years_experience: int) -> str:
    """
    Generate a follow-up question based on candidate's answer.
    
    Args:
        tech: The technology being discussed
        previous_answer: Candidate's previous answer
        years_experience: Years of experience
        
    Returns:
        Prompt for generating follow-up question
    """
    prompt = f"""The candidate just answered a question about {tech}:
"{previous_answer}"

Based on their answer, generate ONE relevant follow-up question that:
1. Builds upon what they just said
2. Probes deeper into their understanding
3. Is appropriate for someone with {years_experience} years of experience
4. Is conversational and encouraging

Present the question naturally, and briefly acknowledge their previous answer before asking the new question.

Generate the follow-up question:"""
    
    return prompt


def validate_technical_answer_prompt(question: str, answer: str) -> str:
    """
    Generate prompt to validate and provide feedback on technical answer.
    
    Args:
        question: The question asked
        answer: Candidate's answer
        
    Returns:
        Prompt for answer validation
    """
    prompt = f"""Question asked: "{question}"
Candidate's answer: "{answer}"

Provide brief, encouraging feedback that:
1. Acknowledges their answer
2. If correct, praises them
3. If partially correct, gently highlights what's good
4. If unclear, asks for clarification
5. Keeps it to 1-2 sentences
6. Maintains a positive, supportive tone

DO NOT provide the correct answer or lecture them. Just acknowledge and move forward.

Generate the feedback:"""
    
    return prompt
