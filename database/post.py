import crud 

from schemas import PostService
from db_settings import SessionLocal

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/posts/search")
def search_post(text: str, db: Session = Depends(get_db)):
    results_list = crud.get_posts(db=db, search_text=text)
    return {"result": results_list}


@router.delete("/posts/delete")
def remove_post(remove_item: PostService, db: Session = Depends(get_db),):
    result = crud.delete_by_id(db=db, id=remove_item.id)
    return {"result": result}
