from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import crud
from src.db import schemas
from src.db.database import get_db

router = APIRouter(
    prefix="/specific-stock",
    tags=["Posts"]
)
# Get the existing sentiment
@router.get("/{stock_id}", response_model=schemas.PostResponse)
def get_sentiment(post_id: int, db: Session = Depends(get_db)):

    post = crud.get_post_by_id(db, post_id)

    if not post:
        print("got something")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post