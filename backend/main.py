from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import tempfile, os, shutil

# Import funciones fachada 

from business_agents.webScrappers.instagramScrapper import scrape_instagram_profile

app = FastAPI(title="Risk Evaluation API")


# Allow requests from your frontend URL
origins = [
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_cache = {}

class UsernameRequest(BaseModel):
    username: str

class ScrapeResponse(BaseModel):
    followers: int
    followees: int

class ScrapeResponse_Instagram(ScrapeResponse):
    pass

class ScrapeResponse_Twitter(ScrapeResponse):
    pass



class Response_PDF(BaseModel):
    balance_sheet: Optional[str] = None
    general_info: Optional[str] = None
    result: Dict[str, Any]

@app.get("/social-media", response_model=ScrapeResponse)
def get_social_media_instagram():
    return ScrapeResponse(followers=0, followees=0) 

@app.post("/social-media", response_model=ScrapeResponse_Instagram)
def scrape_social_media_instagram(data: UsernameRequest):
    try:
        followers, followees = scrape_instagram_profile(data.username)
        memory_cache["instagram"] = ScrapeResponse_Instagram(followers=followers, followees=followees)
        return memory_cache["instagram"]
    except Exception as e:
        # Return error 400 if something goes wrong (e.g. user not found)
        raise HTTPException(status_code=400, detail=str(e))
    
def evaluate_from_pdfs(paths: List[str]) -> Dict[str, Any]:
    """Placeholder PDF evaluation returning dummy metrics.
    Replace this with actual evaluation logic."""
    metrics = {"files_processed": len(paths), "score": 0.0}
    return metrics

@app.post("/pdf-media", response_model=Response_PDF)
def extract_pdfs(balance_sheet: Optional[UploadFile] = File(None), general_info: Optional[UploadFile] = File(None)):
    try:
        if not (balance_sheet or general_info):
            raise HTTPException(status_code=400, detail="At least one PDF must be provided")

        saved_paths = []
        balance_name = balance_sheet.filename if balance_sheet else None
        general_name = general_info.filename if general_info else None

        with tempfile.TemporaryDirectory() as temp_dir:
            if balance_sheet:
                bs_path = os.path.join(temp_dir, balance_sheet.filename)
                with open(bs_path, "wb") as f:
                    shutil.copyfileobj(balance_sheet.file, f)
                saved_paths.append(bs_path)
            if general_info:
                gi_path = os.path.join(temp_dir, general_info.filename)
                with open(gi_path, "wb") as f:
                    shutil.copyfileobj(general_info.file, f)
                saved_paths.append(gi_path)

            result = evaluate_from_pdfs(saved_paths)

        return Response_PDF(balance_sheet=balance_name, general_info=general_name, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


