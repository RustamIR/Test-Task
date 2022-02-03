from sqlalchemy.orm import Session

import elastic
from models import Post


def delete_by_id(db: Session, id: int):
    deleted_post = elastic.search_id(id)
    if deleted_post is not None:
        elastic_result = elastic.delete_id(deleted_post[0]['_id'])
        db_result = db.query(Post).filter(Post.id == id).delete()
        db.commit()
        return all(elastic_result, db_result)
    return False


def get_posts(db: Session, text: str):
    id_list = [item["id"] for item in elastic.search_text(text)]

    result = db.query(Post) \
        .filter(Post.id.in_(id_list)) \
        .order_by(Post.created_date.desc()) \
        .all()
    return result
