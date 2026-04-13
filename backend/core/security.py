from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

"""

认证与鉴权核心模块（Authentication + Authorization）
    包含：
        密码安全（加密 / 校验）
        JWT Token 生成与解析
        接口鉴权（依赖注入获取当前用户）

"""

SECRET_KEY: str = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天后 token 过期

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 解码
def decode_token(token: str) -> dict:
    try:
        # payload 载荷包含用户信息和过期时间等数据
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:    # HTTPException: 如果令牌无效（签名错误、过期、格式错误等）
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            # 设置响应头，提示客户端需要使用 Bearer 方案进行身份验证。
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    # credentials 包含 token 和 scheme（如 Bearer）
    token = credentials.credentials

    payload = decode_token(token)
    # 从 payload 中获取用户名（通常在 "sub" 字段中）
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "username": username,
        "user_id": payload.get("user_id"),
        "role": payload.get("role")
    }
