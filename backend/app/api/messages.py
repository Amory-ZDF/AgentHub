# app/api/messages.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.schemas import Message as MessageSchema
from backend.app.dependencies import get_db
from backend.models.message import Message as MessageModel
from backend.models.conversation import Conversation as ConversationModel
from backend.app.api.auth import get_current_user
from backend.models.user import User as UserModel
from backend.utils.logger import logger

router = APIRouter()


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageSchema])
async def get_messages_for_conversation(
        conversation_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """
    获取指定对话的所有历史消息，仅限对话创建者。
    """
    # 首先验证对话是否存在且属于当前用户
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id,
        ConversationModel.user_id == current_user.id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    # 查询所有关联的消息，并按创建时间升序排列
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at.asc()).all()

    logger.info(f"✅ 用户{current_user.id} 为对话 {conversation_id} 检索到 {len(messages)} 条消息。")

    return messages