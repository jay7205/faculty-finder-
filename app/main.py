from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Optional
import io
import pandas as pd
from .schemas import FacultyResponse, PaginatedFacultyResponse
from .api import FacultyAPI

app = FastAPI(
    title="Faculty Finder API",
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
            "details": "/api/faculty/{id}",
            "export_csv": "/api/faculty/export/csv",
            "export_json": "/api/faculty/export/json"
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

@app.get("/api/faculty/export/csv")
async def export_csv():
    _, data = api.get_all(page=1, limit=1000)
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=faculty_data.csv"
    return response

@app.get("/api/faculty/export/json")
async def export_json():
    _, data = api.get_all(page=1, limit=1000)
    return JSONResponse(content=data, headers={"Content-Disposition": "attachment; filename=faculty_data.json"})

@app.get("/api/faculty/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(faculty_id: int):
    faculty = api.get_by_id(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty
