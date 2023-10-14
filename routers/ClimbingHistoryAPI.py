from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.ClimbingHistory import ClimbingHistory, ClimbingHistoryModel
from database import get_db

router = APIRouter()

# ClimbingHistory 정보를 생성하는 API
@router.post("/climbing_history/", response_model=ClimbingHistoryModel)
def create_climbing_history(history: ClimbingHistoryModel, db: Session = Depends(get_db)):
    db_history = ClimbingHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# 모든 ClimbingHistory 정보를 조회하는 API
@router.get("/climbing_history/", response_model=List[ClimbingHistoryModel])
def read_all_climbing_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    histories = db.query(ClimbingHistory).offset(skip).limit(limit).all()
    return histories

# 특정 ClimbingHistory 정보를 조회하는 API
@router.get("/climbing_history/{climbing_id}", response_model=List[ClimbingHistoryModel])
def read_climbing_history(climbing_id: str, db: Session = Depends(get_db)):
    history = db.query(ClimbingHistory).filter_by(climbing_id=climbing_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    return history

# 특정 ClimbingHistory 정보를 업데이트하는 API
@router.put("/climbing_history/{climbing_id}", response_model=ClimbingHistoryModel)
def update_climbing_history(climbing_id: str, updated_history: ClimbingHistoryModel, db: Session = Depends(get_db)):
    history = db.query(ClimbingHistory).filter_by(climbing_id=climbing_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    for field, value in updated_history.dict().items():
        setattr(history, field, value)
    db.commit()
    db.refresh(history)
    return history

# 특정 ClimbingHistory 정보를 삭제하는 API
@router.delete("/climbing_history/{climbing_id}")
def delete_climbing_history(climbing_id: str, db: Session = Depends(get_db)):
    history = db.query(ClimbingHistory).filter_by(climbing_id=climbing_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    db.delete(history)
    db.commit()
    return {"message": "ClimbingHistory가 삭제되었습니다."}
