from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from backend.db.database import Base

class CustomAgent(Base):
    __tablename__ = 'custom_agents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    agent_id = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, default=None)
    icon = Column(String, default="smart_toy")
    description = Column(String, default="")
    system_prompt = Column(String, nullable=False)
    llm_adapter = Column(String, default="tongyi")
    tools = Column(JSON, default=list)
    # 新增 3 个 JSON 配置字段（A 档功能）
    # NULL 表示该 Agent 走默认策略，保持对老数据的零回归兼容
    memory_config = Column(JSON, nullable=True, default=None)
    planning_config = Column(JSON, nullable=True, default=None)
    validation_config = Column(JSON, nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
