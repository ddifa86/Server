from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models.Hold import Hold, HoldModel
from database import get_db

router = APIRouter()

# Hold 정보를 생성하는 API
@router.post("/hold/", response_model=HoldModel)
def create_hold(hold: HoldModel, db: Session = Depends(get_db)):
    db_hold = Hold(**hold.dict())
    db.add(db_hold)
    db.commit()
    db.refresh(db_hold)
    return db_hold


# 모든 Hold 정보를 조회하는 API
@router.get("/hold/", response_model=List[HoldModel])
def read_all_holds(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    holds = db.query(Hold).offset(skip).limit(limit).all()
    return holds

# 특정 Hold 정보를 조회하는 API
@router.get("/hold/{hold_id}", response_model=HoldModel)
def read_hold(hold_id: str, db: Session = Depends(get_db)):
    hold = db.query(Hold).filter_by(hold_id=hold_id).first()
    if not hold:
        raise HTTPException(status_code=404, detail="등록된 Hold를 찾을 수 없습니다.")
    return hold

# 특정 Hold 정보를 업데이트하는 API
@router.put("/hold/{hold_id}", response_model=HoldModel)
def update_hold(hold_id: str, updated_hold: HoldModel, db: Session = Depends(get_db)):
    hold = db.query(Hold).filter_by(hold_id=hold_id).first()
    if not hold:
        raise HTTPException(status_code=404, detail="등록된 Hold를 찾을 수 없습니다.")
    for field, value in updated_hold.dict().items():
        setattr(hold, field, value)
    db.commit()
    db.refresh(hold)
    return hold

# 특정 Hold 정보를 삭제하는 API
@router.delete("/hold/{hold_id}")
def delete_hold(hold_id: str, db: Session = Depends(get_db)):
    hold = db.query(Hold).filter_by(hold_id=hold_id).first()
    if not hold:
        raise HTTPException(status_code=404, detail="등록된 Hold를 찾을 수 없습니다.")
    db.delete(hold)
    db.commit()
    return {"message": "Hold가 삭제되었습니다."}