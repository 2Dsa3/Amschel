from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

import uvicorn

from business_agents.webScrapper_agent import scrape_instagram_profile

app = FastAPI()


# Allow requests from your Next.js frontend URL
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow your Next.js app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}

memory_cache = {}


class UsernameRequest(BaseModel):
    username: str

class ScrapeResponse(BaseModel):
    followers: int
    followees: int

class ScrapeResponse_Instagram(ScrapeResponse):
    pass

@app.get("/social-media", response_model=ScrapeResponse)
def get_social_media_instagram():
    return ScrapeResponse(followers=0, followees=0) 

@app.post("/social-media", response_model=ScrapeResponse_Instagram)
def scrape_social_media_instagram(data: UsernameRequest):
    try:
        followers, followees = scrape_instagram_profile(data.username)
        return ScrapeResponse(followers=followers, followees=followees)
    except Exception as e:
        # Return error 400 if something goes wrong (e.g. user not found)
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)