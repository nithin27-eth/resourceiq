from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db_setup import initialize_database

# Import all 5 domain route modules
from api.routes_computational import router as comp_router
from api.routes_energy import router as energy_router
from api.routes_human import router as human_router
from api.routes_academic import router as academic_router
from api.routes_insights import router as insights_router

# Initialize FastAPI app
app = FastAPI(
    title="ResourceIQ API",
    description="AI-Powered Multi-Domain Resource Intelligence Platform",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
# This allows Member 6's HTML/JS frontend to make API calls from any browser/domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routers
app.include_router(comp_router)
app.include_router(energy_router)
app.include_router(human_router)
app.include_router(academic_router)
app.include_router(insights_router)

# Startup event: automatically ensure tables exist when server boots
@app.on_event("startup")
async def startup_event():
    initialize_database()
    print("🚀 ResourceIQ Server started successfully.")

# Health check route
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "ResourceIQ API is active. Go to /docs for interactive Swagger UI."
    }

if __name__ == "__main__":
    import uvicorn
    # Run server on all network interfaces (0.0.0.0) at port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
