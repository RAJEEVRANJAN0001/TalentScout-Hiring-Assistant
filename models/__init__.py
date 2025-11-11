"""Data models for the hiring assistant."""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator, Field
import re
import phonenumbers


class CandidateInfo(BaseModel):
    """Model for candidate information with validation."""
    
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    years_experience: Optional[int] = None
    desired_positions: Optional[List[str]] = None
    current_location: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    technical_responses: Optional[dict] = Field(default_factory=dict)
    
    @field_validator('full_name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate that name contains only letters and spaces."""
        if v is None:
            return v
        if not re.match(r'^[a-zA-Z\s\-\.]+$', v.strip()):
            raise ValueError('Name must contain only letters, spaces, hyphens, and periods')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if v is None:
            return v
        try:
            # Try to parse the phone number
            parsed = phonenumbers.parse(v, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError('Invalid phone number')
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            # If parsing fails, check if it's a basic format
            cleaned = re.sub(r'[^\d+]', '', v)
            if len(cleaned) >= 10:
                return v.strip()
            raise ValueError('Invalid phone number format')
    
    @field_validator('years_experience')
    @classmethod
    def validate_experience(cls, v: Optional[int]) -> Optional[int]:
        """Validate years of experience."""
        if v is None:
            return v
        if not isinstance(v, int):
            raise ValueError('Years of experience must be a number')
        if v < 0 or v > 50:
            raise ValueError('Years of experience must be between 0 and 50')
        return v
    
    @field_validator('current_location')
    @classmethod
    def validate_location(cls, v: Optional[str]) -> Optional[str]:
        """Validate location."""
        if v is None:
            return v
        if len(v.strip()) < 2:
            raise ValueError('Location must be at least 2 characters long')
        return v.strip()
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "years_experience": self.years_experience,
            "desired_positions": self.desired_positions,
            "current_location": self.current_location,
            "tech_stack": self.tech_stack,
            "technical_responses": self.technical_responses
        }
    
    def is_complete(self) -> bool:
        """Check if all required information is collected."""
        return all([
            self.full_name,
            self.email,
            self.phone,
            self.years_experience is not None,
            self.desired_positions,
            self.current_location,
            self.tech_stack
        ])
    
    def get_completion_percentage(self) -> int:
        """Calculate completion percentage."""
        fields = [
            self.full_name,
            self.email,
            self.phone,
            self.years_experience,
            self.desired_positions,
            self.current_location,
            self.tech_stack
        ]
        completed = sum(1 for field in fields if field is not None)
        return int((completed / len(fields)) * 100)
