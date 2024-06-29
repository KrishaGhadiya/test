from typing import Union

from fastapi import APIRouter, Depends, Request, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import schemas, crud, database
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.get("/profile", response_class=HTMLResponse)
def read_user_profile(request: Request, user_id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})