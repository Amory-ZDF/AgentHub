from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.dependencies import get_db
from backend.models.custom_agent import CustomAgent as CustomAgentModel
from backend.app.schemas import CustomAgent, CustomAgentCreate
from backend.app.api.auth import get_current_user, try_get_current_user
from backend.models.user import User as UserModel
from backend.core.orchestrator import Orchestrator
from backend.utils.logger import logger
from backend.utils.agent_config import (
    normalize_memory_config,
    normalize_planning_config,
    normalize_validation_config,
)
import uuid
from typing import Optional

# 全局初始化Orchestrator实例，和你的main.py里的初始化保持一致
orchestrator = Orchestrator()

router = APIRouter()


@router.get("", response_model=list[CustomAgent])
async def list_agents(db: Session = Depends(get_db), current_user: Optional[UserModel] = Depends(try_get_current_user)):
    """获取当前用户的自定义Agent + 系统内置Agent"""
    # 只查询当前用户的自定义Agent
    query = db.query(CustomAgentModel).filter(CustomAgentModel.is_active == True)
    if current_user:
        query = query.filter(CustomAgentModel.user_id == current_user.id)
    else:
        query = query.filter(CustomAgentModel.user_id == None)  # 未登录时只查无主的
    db_agents = query.all()
    # 给系统Agent补全所有字段
    # ✨ 过滤掉 custom_ 开头的自定义Agent（它们已经作为 db_agents 返回，避免双显）
    from datetime import datetime
    system_agents = [
        {
            "id": 0,
            "agent_id": aid,
            "name": aid,
            "is_system": True,
            "system_prompt": "系统内置Agent",
            "llm_adapter": "system",
            "tools": [],
            "created_at": datetime.now(),
            "is_active": True
        } for aid in orchestrator.agents.keys() if not aid.startswith("custom_")
    ]
    return [*db_agents, *system_agents]


@router.post("", response_model=CustomAgent)
async def create_agent(req: CustomAgentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """创建新的自定义Agent，绑定到当前用户"""
    # 检查当前用户是否已有同名Agent
    existing = db.query(CustomAgentModel).filter(
        CustomAgentModel.name == req.name,
        CustomAgentModel.user_id == current_user.id
    ).first()
    if existing:
        from datetime import datetime
        timestamp = datetime.now().strftime("%m%d%H%M")
        final_name = f"{req.name}_{timestamp}"
    else:
        final_name = req.name
    
    agent_id = f"custom_{final_name.replace(' ', '_').lower()}_{uuid.uuid4().hex[:6]}"
    # A 档：归一化 3 类配置字段，非法值返回 422
    try:
        memory_cfg = normalize_memory_config(req.memory_config)
        planning_cfg = normalize_planning_config(req.planning_config)
        validation_cfg = normalize_validation_config(req.validation_config)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    db_agent = CustomAgentModel(
        name=final_name,
        agent_id=agent_id,
        user_id=current_user.id,
        icon=req.icon or "smart_toy",
        description=req.description or "",
        system_prompt=req.system_prompt,
        llm_adapter=req.llm_adapter,
        tools=req.tools,
        memory_config=memory_cfg,
        planning_config=planning_cfg,
        validation_config=validation_cfg,
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    orchestrator.register_custom_agent(db_agent)
    logger.info(f"✅ 用户{current_user.id} 创建Agent {db_agent.name}")
    return db_agent


@router.put("/{agent_id}", response_model=CustomAgent)
async def update_agent(agent_id: str, req: CustomAgentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """更新自定义Agent，仅限创建者"""
    db_agent = db.query(CustomAgentModel).filter(CustomAgentModel.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent未找到")
    if db_agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改其他用户的Agent")
    db_agent.name = req.name
    db_agent.icon = req.icon or "smart_toy"
    db_agent.description = req.description or ""
    db_agent.system_prompt = req.system_prompt
    db_agent.llm_adapter = req.llm_adapter
    db_agent.tools = req.tools
    # A 档：归一化并持久化 3 类配置字段
    try:
        db_agent.memory_config = normalize_memory_config(req.memory_config)
        db_agent.planning_config = normalize_planning_config(req.planning_config)
        db_agent.validation_config = normalize_validation_config(req.validation_config)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    db.commit()
    db.refresh(db_agent)
    orchestrator.register_custom_agent(db_agent)
    logger.info(f"🔄 用户{current_user.id} 更新Agent {db_agent.name}")
    return db_agent


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """删除自定义Agent，仅限创建者"""
    db_agent = db.query(CustomAgentModel).filter(CustomAgentModel.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent未找到")
    if db_agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除其他用户的Agent")
    db.delete(db_agent)
    if agent_id in orchestrator.agents:
        del orchestrator.agents[agent_id]
    db.commit()
    logger.info(f"🗑️ 用户{current_user.id} 删除Agent {db_agent.name}")
    return {"success": True, "message": "Agent已成功删除"}