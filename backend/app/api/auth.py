# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from backend.app.dependencies import get_db
from backend.app.schemas import UserCreate, UserLogin, UserResponse, Token
from backend.models.user import User as UserModel
from backend.utils.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

# 配置
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-keep-it-safe")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30天

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT认证方案
security = HTTPBearer()

router = APIRouter()

# 工具函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """获取当前认证用户的依赖项"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        logger.info(f"[AUTH] get_current_user: token开头={str(token)[:20]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        logger.info(f"[AUTH] jwt解码成功, sub(用户ID)={user_id}")
        if user_id is None:
            logger.warning("[AUTH] token中sub为空")
            raise credentials_exception
    except JWTError as e:
        logger.warning(f"[AUTH] jwt解码失败: {e}")
        raise credentials_exception
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        logger.warning(f"[AUTH] 数据库中未找到用户ID={user_id}")
        raise credentials_exception
    logger.info(f"[AUTH] 认证成功: user={user.username} id={user.id}")
    return user


async def try_get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)), db: Session = Depends(get_db)):
    """尝试获取当前用户，未登录返回None（不抛401）"""
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


# API端点
@router.post("/register")
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    existing_email = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="邮箱已被注册")
    
    # 创建新用户
    hashed_password = get_password_hash(user_in.password)
    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"✅ 新用户注册成功: {db_user.username}")
    # 返回格式匹配前端期望
    return {
        "ok": True,
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "createdAt": db_user.created_at
        },
        "token": access_token
    }

@router.post("/login")
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """用户登录 - 使用 email + password"""
    # 按 email 查找用户（前端传的是 email）
    user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="账户已被禁用")
    
    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"✅ 用户登录成功: {user.username}")
    # 返回格式匹配前端期望
    return {
        "ok": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "createdAt": user.created_at
        },
        "token": access_token
    }

@router.get("/me")
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """获取当前用户信息 - 返回格式匹配前端期望"""
    return {
        "ok": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "createdAt": current_user.created_at
        }
    }