from pydantic import BaseModel, EmailStr, validator


class UserInput(BaseModel):
    full_name: str
    email: EmailStr
    linkedin_profile: str
    salary_range: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v

    @validator('linkedin')
    def linkedin_must_be_url(cls, v):
        if not v.startswith('https://www.linkedin.com/'):
            raise ValueError('Invalid LinkedIn URL')
        return v
