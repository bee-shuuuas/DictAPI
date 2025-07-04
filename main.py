from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_word_data

app = FastAPI()

# Allow access from any domain (for mobile app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/word/{word}")
def fetch_word(word: str):
    return get_word_data(word)
