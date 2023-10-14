from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.Crag import Crag, CragModel
from database import get_db

router = APIRouter()


# Crag 정보를 생성하는 API
@router.post("/crag/", response_model=CragModel)
def create_crag(crag: CragModel, db: Session = Depends(get_db)):
    db_crag = Crag(**crag.dict())
    db.add(db_crag)
    db.commit()
    db.refresh(db_crag)
    return db_crag

# 모든 Crag 정보를 조회하는 API
@router.get("/crag/", response_model=List[CragModel])
def read_crag(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crags = db.query(Crag).offset(skip).limit(limit).all()
    return crags

# 특정 Crag 정보를 조회하는 API
@router.get("/crag/{crag_id}", response_model=CragModel)
def read_crag(crag_id: str, db: Session = Depends(get_db)):
    crag = db.query(Crag).filter_by(crag_id=crag_id).first()
    if not crag:
        raise HTTPException(status_code=404, detail="등록된 Crag를 찾을 수 없습니다.")
    return crag

# 특정 Crag 정보를 업데이트하는 API
@router.put("/crag/{crag_id}", response_model=CragModel)
def update_crag(crag_id: str, updated_crag: CragModel, db: Session = Depends(get_db)):
    crag = db.query(Crag).filter_by(crag_id=crag_id).first()
    if not crag:
        raise HTTPException(status_code=404, detail="등록된 Crag를 찾을 수 없습니다.")
    for field, value in updated_crag.dict().items():
        setattr(crag, field, value)
    db.commit()
    db.refresh(crag)
    return crag

# 특정 Crag 정보를 삭제하는 API
@router.delete("/crag/{crag_id}")
def delete_crag(crag_id: str, db: Session = Depends(get_db)):
    crag = db.query(Crag).filter_by(crag_id=crag_id).first()
    if not crag:
        raise HTTPException(status_code=404, detail="등록된 Crag를 찾을 수 없습니다.")
    db.delete(crag)
    db.commit()
    return {"message": "Crag가 삭제되었습니다."}