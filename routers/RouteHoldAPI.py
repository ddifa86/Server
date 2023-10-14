from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.RouteHold import RouteHold, RouteHoldModel
from database import get_db


router = APIRouter()


# RouteHold 정보를 생성하는 API
@router.post("/route_hold/", response_model=RouteHoldModel)
def create_route_hold(route_hold: RouteHoldModel, db: Session = Depends(get_db)):
    db_route_hold = RouteHold(**route_hold.dict())
    db.add(db_route_hold)
    db.commit()
    db.refresh(db_route_hold)
    return db_route_hold

# 모든 RouteHold 정보를 조회하는 API
@router.get("/route_hold/", response_model=List[RouteHoldModel])
def read_all_route_holds(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    route_holds = db.query(RouteHold).offset(skip).limit(limit).all()
    return route_holds

# 특정 RouteHold 정보를 조회하는 API
# hold_id로 시작하는 route_hold 정보 반환
@router.get("/route_hold/{hold_id}", response_model=List[RouteHoldModel])
def read_route_hold(hold_id: str, db: Session = Depends(get_db)):
    route_hold= db.query(RouteHold).filter_by(hold_id=hold_id , hold_seq = 1 ).all()    
    if not route_hold:
        raise HTTPException(status_code=404, detail="등록된 RouteHold를 찾을 수 없습니다.")        
    # 가져온 route_hold 중 첫 번째 데이터의 route_id를 가져옴
    route_id = route_hold[0].route_id
    # route_id로 시작하는 
    route_hold= db.query(RouteHold).filter_by(route_id=route_id).order_by(RouteHold.hold_seq).all()   
    return route_hold 


# 특정 RouteHold 정보를 조회하는 API
# hold_id로 시작하는 route_hold 정보 반환
@router.get("/find_route/{route_id}", response_model=List[RouteHoldModel])
def read_route_hold(route_id: str, db: Session = Depends(get_db)):
    route_hold = db.query(RouteHold).filter_by(hold_route_idid=route_id).first()
    if not route_hold:
        raise HTTPException(status_code=404, detail="등록된 RouteHold를 찾을 수 없습니다.")
    return route_hold



# 특정 RouteHold 정보를 삭제하는 API
@router.delete("/route_hold/{route_id}")
def delete_route_hold(route_id: str, db: Session = Depends(get_db)):
    route_hold = db.query(RouteHold).filter_by(route_id=route_id).first()
    if not route_hold:
        raise HTTPException(status_code=404, detail="등록된 RouteHold를 찾을 수 없습니다.")
    db.delete(route_hold)
    db.commit()
    return {"message": "RouteHold가 삭제되었습니다."}