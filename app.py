import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Amazon Review Framework API",
    description="API for accessing Amazon Review Framework components",
    version="2.0.0",
)

# Enable CORS for API access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory containing framework files
FRAMEWORK_DIR = "NEW-SYSTEM"

# Serve static files directly
app.mount("/files", StaticFiles(directory=FRAMEWORK_DIR), name="files")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Amazon Review Framework API",
        "endpoints": [
            "/api/files",
            "/api/files/{filename}",
            "/api/framework"
        ],
        "static_files": "/files/{filename}"
    }

# List all framework files
@app.get("/api/files")
def list_files():
    if os.path.exists(FRAMEWORK_DIR):
        files = [f for f in os.listdir(FRAMEWORK_DIR) if f.endswith('.json')]
        return {"files": files}
    raise HTTPException(status_code=404, detail=f"Directory {FRAMEWORK_DIR} not found")

# Get a specific file
@app.get("/api/files/{filename}")
def get_file(filename: str):
    if not filename.endswith(".json"):
        filename += ".json"
    
    file_path = os.path.join(FRAMEWORK_DIR, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading {filename}: {str(e)}")
    raise HTTPException(status_code=404, detail=f"File {filename} not found")

# Get the complete framework
@app.get("/api/framework")
def get_framework():
    framework = {}
    if os.path.exists(FRAMEWORK_DIR):
        for filename in os.listdir(FRAMEWORK_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(FRAMEWORK_DIR, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        framework[filename] = json.load(f)
                except Exception as e:
                    framework[filename] = {"error": f"Error loading {filename}: {str(e)}"}
        return framework
    raise HTTPException(status_code=404, detail=f"Directory {FRAMEWORK_DIR} not found")

# Define request model for review generation
class ReviewRequest(BaseModel):
    product_name: str
    category: str
    experience: str

# Define response model
class ReviewResponse(BaseModel):
    review: str

# This endpoint would integrate with Claude API (not implemented here)
@app.post("/api/generate-review")
def generate_review(request: ReviewRequest):
    # Note: This is a placeholder. In a real implementation, you would:
    # 1. Load your framework files
    # 2. Create a prompt for Claude API
    # 3. Call Claude API with the appropriate context
    # 4. Return the generated review
    
    return ReviewResponse(
        review=f"This is a placeholder for a generated review for {request.product_name}. " +
               "In a real implementation, this would call Claude API with your framework files."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)