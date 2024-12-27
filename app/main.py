from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import auth, exams, categories, profile, test_results
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(exams.router, prefix="/exams", tags=["Exams"])
app.include_router(test_results.router, prefix="/results", tags=["Test Results"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Exam System API"}
