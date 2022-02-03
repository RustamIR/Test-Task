import uvicorn

from http import HTTPStatus

from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse

from models import Post
from post import PostService
from elastic import EsService


app = FastAPI(
        title='Test Task',
        version='1.0.0',
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=JSONResponse,
)


@app.get('/posts/search', response_model_exclude_unset=True)
async def posts_search(text: str,
                       sort: str = "created_date",
                       page_number: int = 0,
                       page_size: int = 20,
                       post_service: PostService=PostService()):
    post_list = EsService().search_text(
        text=text,
        sort = sort,
        size = page_size,
    )
    if not post_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [PostService(id=Post.id,
                        rubrics=Post.rubrics,
                        text=Post.text,
                        created_date=Post.created_date) for post in post_list]



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, use_colors=True)