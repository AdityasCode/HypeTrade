from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import src.processing.scraping as scraping
import src.db.models
import datetime
import src.db.schemas
from src.db import crud
from src.db.database import get_db

router = APIRouter(prefix="/scraping", tags=["Scraping"])

SUBREDDITS = ["stocks", "investing", "wallstreetbets", "stockmarket"]

@router.get("/", tags=["scraping"])
def update_sentiments(db: Session = Depends(get_db)):
    """
    Updates the database with new Reddit posts.
    """
    stocks = crud.get_top_stocks(db)
    for stock in stocks:
        stock_id = stock.stock_id
        keyword = stock.ticker
        for SUBREDDIT in SUBREDDITS:
            scraping.scrape_subreddit_posts(db, SUBREDDIT, keyword, stock_id, limit=50)
        scraping.process_unprocessed_entries(db, stock_id)

def requested_update(db: Session, keyword: str, stock_id: int):
    for SUBREDDIT in SUBREDDITS:
        # Scrape the subreddit for posts containing the keyword
        scraping.scrape_subreddit_posts(db, SUBREDDIT, keyword, stock_id, limit=50)
    scraping.process_unprocessed_entries(db, stock_id)
    return {"message": "Scraping and sentiment update completed for top stocks."}

# periodical_update(db=db)