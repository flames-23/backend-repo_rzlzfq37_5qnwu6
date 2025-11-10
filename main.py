import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Faculty, Program, News, Inquiry

app = FastAPI(title="University Website Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "University API is running"}

# Public content endpoints
@app.get("/api/faculties")
def list_faculties(limit: int = 20):
    try:
        items = get_documents("faculty", {}, limit)
        # Convert ObjectId to string if present
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/programs")
def list_programs(limit: int = 50, faculty_id: Optional[str] = None):
    try:
        filter_dict = {"faculty_id": faculty_id} if faculty_id else {}
        items = get_documents("program", filter_dict, limit)
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news")
def list_news(limit: int = 10):
    try:
        items = get_documents("news", {}, limit)
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact / inquiry
@app.post("/api/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        inserted_id = create_document("inquiry", payload)
        return {"id": inserted_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoint to seed minimal demo content if database is empty
class SeedRequest(BaseModel):
    include_samples: bool = True

@app.post("/api/seed")
def seed_content(body: SeedRequest):
    try:
        # Check if collections have data
        has_faculty = len(get_documents("faculty", {}, 1)) > 0
        if not has_faculty and body.include_samples:
            create_document("faculty", Faculty(name="Faculty of Engineering", description="Leading innovation and technology.", dean="Dr. Andi", website="#", featured_image="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200"))
            create_document("faculty", Faculty(name="Faculty of Business", description="Entrepreneurship and leadership.", dean="Dr. Sari", website="#", featured_image="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200"))
        has_program = len(get_documents("program", {}, 1)) > 0
        if not has_program and body.include_samples:
            create_document("program", Program(title="Computer Science (BSc)", level="Undergraduate", faculty_id=None, duration_years=4, overview="Learn algorithms, AI, and software engineering."))
            create_document("program", Program(title="Business Administration (BBA)", level="Undergraduate", faculty_id=None, duration_years=4, overview="Management, finance, and marketing foundations."))
        has_news = len(get_documents("news", {}, 1)) > 0
        if not has_news and body.include_samples:
            create_document("news", News(title="Campus Innovation Week 2025", content="Join workshops, talks, and hackathons across campus.", author="PR Team", cover_image="https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?w=1200", published_at=datetime.utcnow()))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
