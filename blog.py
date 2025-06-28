from fastapi import APIRouter, Depends,status, Response, HTTPException
from .. import schemas, models,database,oauth2
from typing import List
from sqlalchemy.orm import Session,joinedload

get_db =database.get_db

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"])



@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).options(joinedload(models.Blog.creator)).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, response: Response, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with this id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with this id {id} is not available")
    blog.update(request.dict())
    db.commit()
    return 'updated successfully'

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog) 
def show(id: int, response: Response, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
       # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"blog wiith the id {id} is not availabel"}
    return blog