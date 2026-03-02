from pydantic import BaseModel, Field


class OwnerProfile(BaseModel):
    age: int = Field(ge=0, le=120)
    industry: str
    income_range: str


class Preferences(BaseModel):
    response_style: str | None = None
    strategy_style: str | None = None
    locale_bias: str | None = None


class FamilyMember(BaseModel):
    id: str
    relation: str
    age_band: str | None = None
    occupation_or_school: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    shared_financial_responsibilities: list[str] = Field(default_factory=list)
