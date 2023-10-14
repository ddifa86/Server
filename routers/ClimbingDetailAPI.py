from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.ClimbingDetailHistory import ClimbingDetailHistory, ClimbingDetailHistoryModel
from models.ClimbingHistory import ClimbingHistory, ClimbingHistoryModel
from database import get_db
from datetime import datetime
from dateutil.parser import parse

router = APIRouter()

# ClimbingDetailHistory 정보를 생성하는 API
@router.post("/climbing_detail_history/", response_model=ClimbingDetailHistoryModel)
def create_climbing_detail_history(history: ClimbingDetailHistoryModel, db: Session = Depends(get_db)):
    #  tag_time 문자열을 datetime으로 변환
    tag_time = datetime.strptime(history.tag_time, '%Y-%m-%dT%H:%M:%SZ')

    db_history = ClimbingDetailHistory(
    climbing_id=history.climbing_id,
    route_id=history.route_id,
    hold_id=history.hold_id,
    tag_time=tag_time,
    hold_seq=history.hold_seq
    )
    
    db.add(db_history)
    db.commit()
    db.refresh(db_history)

    return history

# 특정 ClimbingDetailHistory 정보를 조회하는 API
@router.get("/climbing_detail_history/{climbing_id}", response_model=List[ClimbingDetailHistoryModel])
def read_climbing_detail_history(climbing_id: str, db: Session = Depends(get_db)):
    climbing_history = db.query(ClimbingDetailHistory).filter_by(climbing_id=climbing_id).all()
    if not climbing_history:
        raise HTTPException(status_code=404, detail="등록된 ClimbingDetailHistory를 찾을 수 없습니다.")
    return climbing_history


# ClimbingHistoryModel와 List<ClimbingDetailHistoryModel>을 한 번에 생성하는 API
@router.post("/climbing_history_with_details/", response_model=ClimbingHistoryModel)
def create_climbing_history_with_details(
    climbing_history: ClimbingHistoryModel,
    climbing_details: List[ClimbingDetailHistoryModel],
    db: Session = Depends(get_db)
):
    try:
        # start_time과 end_time을 문자열에서 datetime으로 변환
        start_time = datetime.strptime(climbing_history.start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(climbing_history.end_time, '%Y-%m-%dT%H:%M:%SZ')

        # ClimbingHistory 정보 저장
        db_climbing_history = ClimbingHistory(
            climbing_id=climbing_history.climbing_id,
            route_id=climbing_history.route_id,
            user_id=climbing_history.user_id,
            start_time=start_time,
            end_time=end_time,
            climbing_date=climbing_history.climbing_date,
            climbing_time=climbing_history.climbing_time,
            progress=climbing_history.progress,
            completion_status=climbing_history.completion_status
        )

        db.add(db_climbing_history)
        db.commit()
        db.refresh(db_climbing_history)

         # ClimbingDetailHistory 정보 저장
        db_climbing_details = []
        for detail in climbing_details:
            tag_time = datetime.strptime(detail.tag_time, '%Y-%m-%dT%H:%M:%SZ')
            db_climbing_details.append(
                ClimbingDetailHistory(
                    climbing_id=db_climbing_history.climbing_id,
                    tag_time=tag_time,
                    **detail.dict(exclude={'tag_time','climbing_id'})
                )
            )
        db.add_all(db_climbing_details)
        db.commit()

        return climbing_history
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="저장에 실패했습니다.")
