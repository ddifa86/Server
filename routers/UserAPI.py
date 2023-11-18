from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models.User import UserModel, User
from database import get_db


router = APIRouter()

@router.get("/users", response_model=List[UserModel])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 클라이언트가 보낸 비밀번호와 실제 사용자의 비밀번호를 비교하여 일치하지 않으면 에러를 반환
    if user.password != password:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    return UserModel.from_orm(user)

@router.post("/users", response_model=UserModel)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    db_user = User(
        user_id=user.user_id,
        password=user.password,
        name=user.name,
        role=user.role,
        crew=user.crew,
        leadlevel=user.leadlevel
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=UserModel)
def update_user(user_id: str, updated_user: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    for field, value in updated_user.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    db.delete(user)
    db.commit()
    return {"message": "사용자가 삭제되었습니다."}