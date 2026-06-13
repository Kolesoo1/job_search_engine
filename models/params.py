from typing import Optional, Literal, Annotated

from pydantic import BaseModel, Field


class SearchParams(BaseModel):
    text: str
    area: Optional[int] = 113
    speciality: Optional[int] = None
    experience: Literal["noExperience", "between1And3", "between3And6", "moreThan6"] = (
        Field("noExperience", description="Valid values for the experience field"))
    per_page: int = Field(20, ge=1, le=100, description="Count of vacancies on page")
    page: int = Field(0, ge=0)
