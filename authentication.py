from ..import schemas,   database,models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter,Depends,status,Response,HTTPException

router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login", response_model=schemas.Token)
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email ==request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    

   
    access_token = token.create_access_token(
        data={"sub": user.email}  # Use email as the subject
    )
    return {"access_token": access_token, "token_type": "bearer"}