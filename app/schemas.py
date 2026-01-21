from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FacultyBase(BaseModel):
    name: str
    image_url: Optional[str] = None
    education: Optional[str] = None
    contact_no: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    biography: Optional[str] = None
    specialization: Optional[str] = None
    teaching: Optional[str] = None
    publications: Optional[str] = None
    university: str = "DA-IICT"

class FacultyResponse(FacultyBase):
    id: int
    raw_source_file: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedFacultyResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[FacultyResponse]
