from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models.UserClimbDiary import UserClimbDiary, UserClimbDiaryModel
from database import get_db

router = APIRouter()

@router.post("/user_climb_diary/", response_model=UserClimbDiaryModel)
def create_user_climb_diary(diary_entry: UserClimbDiaryModel, db: Session = Depends(get_db)):
    db_diary_entry = UserClimbDiary(**diary_entry.dict())
    db.add(db_diary_entry)
    db.commit()
    db.refresh(db_diary_entry)
    return db_diary_entry


# 사용자 ID에 따른 다이어리 리스트를 반환하는 API
@router.get("/user_climb_diary/{user_id}", response_model=List[UserClimbDiaryModel])
def read_user_climb_diary(user_id: str, db: Session = Depends(get_db)):
    diary_entries = db.query(UserClimbDiary).filter(UserClimbDiary.user_id == user_id).all()
    if not diary_entries:
        raise HTTPException(status_code=404, detail="해당 사용자의 다이어리를 찾을 수 없습니다.")
    return diary_entries


@router.put("/user_climb_diary/{climbing_date}", response_model=UserClimbDiaryModel)
def update_user_climb_diary(climbing_date: str, diary_update: UserClimbDiaryModel, db: Session = Depends(get_db)):
    diary_entry = db.query(UserClimbDiary).filter_by(climbing_date=climbing_date).first()
    if diary_entry is None:
        raise HTTPException(status_code=404, detail="해당 날짜의 다이어리를 찾을 수 없습니다.")
    for key, value in diary_update.dict().items():
        setattr(diary_entry, key, value)
    db.commit()
    db.refresh(diary_entry)
    return diary_entry


