from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.ClimbingHistory import ClimbingHistory, ClimbingHistoryModel
from models.Route import Route, RouteModel
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
   # ClimbingHistory와 Route 테이블을 조인하여 데이터를 가져옵니다.
    histories = (
        db.query(ClimbingHistory, Route)
        .join(Route, ClimbingHistory.route_id == Route.route_id)
        ##.filter(ClimbingHistory.user_id == user_id)
        .all()
    )
    
    if not histories:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    
    histories_with_route_info = []
    for history, route in histories:
        history_dict = history.__dict__
        history_dict['start_time'] = history.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        history_dict['end_time'] = history.end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Route 정보를 추가합니다.
        history_dict['crag_id'] = route.crag_id
        history_dict['difficulty_level'] = route.difficulty_level
        history_dict['route_name'] = route.route_name
        histories_with_route_info.append(ClimbingHistoryModel(**history_dict))
    
    return histories_with_route_info
    #return histories

# 특정 ClimbingHistory 정보를 조회하는 API
@router.get("/climbing_history/{user_id}", response_model=List[ClimbingHistoryModel])
def read_climbing_history(user_id: str, db: Session = Depends(get_db)):
   # ClimbingHistory와 Route 테이블을 조인하여 데이터를 가져옵니다.
    histories = (
        db.query(ClimbingHistory, Route)
        .join(Route, ClimbingHistory.route_id == Route.route_id)
        .filter(ClimbingHistory.user_id == user_id)
        .all()
    )
    
    if not histories:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    
    histories_with_route_info = []
    for history, route in histories:
        history_dict = history.__dict__
        history_dict['start_time'] = history.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        history_dict['end_time'] = history.end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Route 정보를 추가합니다.
        history_dict['crag_id'] = route.crag_id
        history_dict['difficulty_level'] = route.difficulty_level
        history_dict['route_name'] = route.route_name
        histories_with_route_info.append(ClimbingHistoryModel(**history_dict))
    
    return histories_with_route_info
 

 

# 특정 ClimbingHistory 정보를 삭제하는 API
@router.delete("/climbing_history/{climbing_id}")
def delete_climbing_history(climbing_id: str, db: Session = Depends(get_db)):
    history = db.query(ClimbingHistory).filter_by(climbing_id=climbing_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="등록된 ClimbingHistory를 찾을 수 없습니다.")
    db.delete(history)
    db.commit()
    return {"message": "ClimbingHistory가 삭제되었습니다."}


