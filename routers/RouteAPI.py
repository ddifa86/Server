from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.Route import Route, RouteModel
from database import get_db


router = APIRouter()

# Route 정보를 생성하는 API
@router.post("/route/", response_model=RouteModel)
def create_route(route: RouteModel, db: Session = Depends(get_db)):
    db_route = Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

# 모든 Route 정보를 조회하는 API
@router.get("/route/", response_model=List[RouteModel])
def read_all_routes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    routes = db.query(Route).offset(skip).limit(limit).all()
    return routes

# 특정 Route 정보를 조회하는 API
@router.get("/route/{crag_id}", response_model=List[RouteModel])
def read_route(crag_id: str, db: Session = Depends(get_db)):
    route = db.query(Route).filter_by(crag_id=crag_id).all()
    if not route:
        raise HTTPException(status_code=404, detail="등록된 Route를 찾을 수 없습니다.")
    return route

# 특정 Route 정보를 업데이트하는 API
@router.put("/route/{route_id}", response_model=RouteModel)
def update_route(route_id: str, updated_route: RouteModel, db: Session = Depends(get_db)):
    route = db.query(Route).filter_by(route_id=route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="등록된 Route를 찾을 수 없습니다.")
    for field, value in updated_route.dict().items():
        setattr(route, field, value)
    db.commit()
    db.refresh(route)
    return route

# 특정 Route 정보를 삭제하는 API
@router.delete("/route/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    route = db.query(Route).filter_by(route_id=route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="등록된 Route를 찾을 수 없습니다.")
    db.delete(route)
    db.commit()
    return {"message": "Route가 삭제되었습니다."}