from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .schemas import FacultyResponse, PaginatedFacultyResponse
from .api import FacultyAPI

app = FastAPI(
    title="Faculty Finder API",
    description="REST API for accessing cleaned faculty data from DA-IICT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FacultyAPI()

@app.get("/")
async def root():
    return {
        "status": "online",
        "api": "Faculty Finder",
        "endpoints": {
            "list": "/api/faculty",
            "search": "/api/faculty/search?q={query}",
            "details": "/api/faculty/{id}"
        }
    }

@app.get("/api/faculty", response_model=PaginatedFacultyResponse)
async def list_faculty(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    total, data = api.get_all(page, limit)
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }

@app.get("/api/faculty/search", response_model=List[FacultyResponse])
async def search_faculty(q: str = Query(..., min_length=2)):
    return api.search(q)

@app.get("/api/faculty/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(faculty_id: int):
    faculty = api.get_by_id(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty
