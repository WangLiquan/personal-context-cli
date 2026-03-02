from pydantic import BaseModel, Field


class OwnerProfile(BaseModel):
    age: int = Field(ge=0, le=120)
    industry: str
    income_range: str
