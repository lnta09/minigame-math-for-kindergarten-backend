from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Field, select, Session
from typing import List
from db import get_session

# 🧱 Model
class levels(SQLModel, table=True):
    level_id: int | None = Field(default=None, primary_key=True)
    level_name: str
    description: str | None = None
    order_index: int | None = None


# ⚙️ Router
router = APIRouter(prefix="/levels", tags=["levels"])

@router.get("/", response_model=List[levels])
def get_levels(session: Session = Depends(get_session)):
    """Lấy danh sách tất cả các level"""
    levels_list = session.exec(select(levels)).all()
    return levels_list

@router.get("/{level_id}", response_model=levels)
def get_level(level_id: int, session: Session = Depends(get_session)):
    """Lấy thông tin level theo ID"""
    level = session.exec(select(levels).where(levels.level_id == level_id)).first()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level

@router.post("/", response_model=levels)
def create_level(level: levels, session: Session = Depends(get_session)):
    """Thêm mới một level"""
    session.add(level)
    session.commit()
    session.refresh(level)
    return level

@router.put("/{level_id}", response_model=levels)
def update_level(level_id: int, updated: levels, session: Session = Depends(get_session)):
    """Cập nhật level"""
    level = session.exec(select(levels).where(levels.level_id == level_id)).first()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    level.level_name = updated.level_name
    level.description = updated.description
    session.add(level)
    session.commit()
    session.refresh(level)
    return level

@router.delete("/{level_id}")
def delete_level(level_id: int, session: Session = Depends(get_session)):
    """Xóa level"""
    level = session.exec(select(levels).where(levels.level_id == level_id)).first()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    session.delete(level)
    session.commit()
    message = "Level " + str(level_id) + " deleted successfully"
    return {"message": message}
