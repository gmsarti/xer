from pydantic import BaseModel, Field
from typing import List, Optional

class Classification(BaseModel):
    framework: str
    name: str

class TaleSummary(BaseModel):
    id: int
    title: str = Field(..., validation_alias="titulo")
    author: Optional[str] = Field(None, validation_alias="origem") # Mapping 'origem' to 'author' as per plan/schema match
    url: str
    classifications: List[Classification] = []

    class Config:
        populate_by_name = True

class TaleDetail(TaleSummary):
    text: Optional[str] = Field(None, validation_alias="texto_completo")

class TaleListResponse(BaseModel):
    tales: List[TaleSummary]
    total: int
    page: int
    page_size: int
