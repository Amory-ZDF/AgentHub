# app/api/conversations.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.schemas import ConversationCreate, Conversation
from backend.app.dependencies import get_db
from backend.models.conversation import Conversation as ConversationModel
from backend.app.api.auth import get_current_user, SECRET_KEY, ALGORITHM
from backend.models.user import User as UserModel
from backend.utils.logger import logger
from jose import JWTError, jwt
from typing import Optional
import uuid

router = APIRouter()


async def try_get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)), db: Session = Depends(get_db)):
    """尝试获取当前用户，未登录返回None"""
    if not credentials:
        return None
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            return None
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        return user
    except:
        return None


def _make_mission_dict(conv, squad_override=None):
    """将 Conversation 模型转换为前端期望的 mission 格式"""
    # 从数据库恢复 squad 配置，若无则用默认值（不再自动塞 orchestrator，由用户自行添加 Agent）
    squad = squad_override or conv.squad_config or {
        "agents": [],
        "coordinator": {"name": "Coordinator", "role": "分派子 Agent + 解析自然语言编辑"},
        "enabledMcpTools": [],
        "enabledSkills": []
    }
    return {
        "id": f"mis_{conv.id}",
        "name": conv.title or f"新对话 {conv.id}",
        "icon": "assignment",
        "description": "新的对话任务，开始你的AI之旅吧",
        "runs": [{
            "id": "run_current",
            "title": "当前运行",
            "status": "idle",
            "startedAt": None,
            "lastActiveAt": None,
            "conversation": [],
            "artifact": None
        }],
        "squad": squad
    }


@router.post("")
async def create_mission(
    mission_in: dict,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """创建新的mission - 绑定到当前用户"""
    
    squad = mission_in.get("squad", {})
    agents = squad.get("agents", [])
    
    conv = ConversationModel(
        title=mission_in.get("name", "新任务"),
        user_id=current_user.id,
        squad_config=squad
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    
    new_mission = _make_mission_dict(conv)
    
    logger.info(f"✅ 用户{current_user.id} 新建mission: {new_mission['id']} - {new_mission['name']}")
    return {"ok": True, "mission": new_mission}

@router.delete("/{mission_id}")
async def delete_mission(
    mission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """删除指定mission，仅限创建者"""
    
    try:
        conv_id = int(mission_id.replace("mis_", ""))
    except:
        raise HTTPException(status_code=400, detail="无效的mission ID")
    
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conv_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="mission不存在")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除其他用户的mission")
    
    db.delete(conversation)
    db.commit()
    logger.info(f"🗑️ 用户{current_user.id} 删除mission {mission_id}")
    return {"ok": True, "message": "mission已成功删除"}

@router.get("/{mission_id}")
async def get_mission(
    mission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """获取单个mission的详情，仅限创建者"""
    
    try:
        conv_id = int(mission_id.replace("mis_", ""))
    except:
        raise HTTPException(status_code=400, detail="无效的mission ID")
    
    conv = db.query(ConversationModel).filter(
        ConversationModel.id == conv_id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="mission不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他用户的mission")
    
    mission = _make_mission_dict(conv)
    
    return {"ok": True, "mission": mission}

@router.put("/{mission_id}")
async def update_mission(
    mission_id: str,
    mission_update: dict,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """更新mission信息，仅限创建者"""
    
    try:
        conv_id = int(mission_id.replace("mis_", ""))
    except:
        raise HTTPException(status_code=400, detail="无效的mission ID")
    
    conv = db.query(ConversationModel).filter(
        ConversationModel.id == conv_id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="mission不存在")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改其他用户的mission")
    
    if "name" in mission_update:
        conv.title = mission_update["name"]
    if "squad" in mission_update:
        conv.squad_config = mission_update["squad"]
    
    db.commit()
    logger.info(f"✏️ 用户{current_user.id} 更新mission {mission_id}")
    return {"ok": True, "message": "更新成功"}

@router.get("")
async def list_missions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """获取当前用户的所有missions"""
    
    convs = db.query(ConversationModel).filter(
        ConversationModel.is_archived == False,
        ConversationModel.user_id == current_user.id
    ).order_by(
        ConversationModel.last_active_at.desc()
    ).all()
    
    missions = []
    for conv in convs:
        mission_data = _make_mission_dict(conv)
        missions.append(mission_data)
    
    logger.info(f"📋 用户{current_user.id} 已返回 {len(missions)} 个missions")
    return {"ok": True, "missions": missions}