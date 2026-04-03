"""
密码重置服务模块

处理密码重置相关的业务逻辑：
1. 生成和发送验证码
2. 验证验证码
3. 重置密码
"""
import random
import string
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from DAO.user import get_user_by_email, update_user_password
from services.email import send_verification_email
from core.security import get_password_hash

# 开发模式：如果为 True，跳过邮箱存在性检查
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"

# 验证码存储（内存存储，实际项目应使用 Redis）
# 格式：{email: {"code": "123456", "expires_at": datetime}}
reset_codes: Dict[str, dict] = {}

# 验证码配置
CODE_LENGTH = 6  # 验证码长度
CODE_EXPIRE_MINUTES = 10  # 验证码有效期（分钟）
MAX_SEND_ATTEMPTS = 3  # 最大发送次数


def generate_verification_code(length: int = CODE_LENGTH) -> str:
    """
    生成随机验证码
    
    Args:
        length: 验证码长度
    
    Returns:
        str: 生成的验证码
    """
    return ''.join(random.choices(string.digits, k=length))


async def send_reset_code(email: str, db: AsyncSession) -> dict:
    """
    发送密码重置验证码
    
    Args:
        email: 用户邮箱
        db: 数据库会话
    
    Returns:
        dict: 返回成功消息
    
    Raises:
        HTTPException: 邮箱不存在、发送失败等异常
    """
    # 1. 检查邮箱是否存在
    user = await get_user_by_email(email, db)
    if not user and not DEV_MODE:
        raise HTTPException(
            status_code=404,
            detail="Email not found. Please check your email address."
        )
    
    # 开发模式提示
    if DEV_MODE and not user:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"开发模式：邮箱 {email} 不存在于数据库中，但仍允许发送验证码")
    
    # 2. 检查发送频率限制
    current_time = datetime.now()
    if email in reset_codes:
        last_send_time = reset_codes[email].get("last_send_time")
        if last_send_time:
            time_diff = (current_time - last_send_time).total_seconds()
            if time_diff < 60:  # 60 秒内只能发送一次
                raise HTTPException(
                    status_code=429,
                    detail="Please wait before requesting another code."
                )
        
        # 检查发送次数限制
        send_count = reset_codes[email].get("send_count", 0)
        if send_count >= MAX_SEND_ATTEMPTS:
            raise HTTPException(
                status_code=429,
                detail="Maximum send attempts reached. Please try again later."
            )
    
    # 3. 生成验证码
    code = generate_verification_code()
    expires_at = current_time + timedelta(minutes=CODE_EXPIRE_MINUTES)
    
    # 4. 存储验证码
    reset_codes[email] = {
        "code": code,
        "expires_at": expires_at,
        "last_send_time": current_time,
        "send_count": reset_codes.get(email, {}).get("send_count", 0) + 1
    }
    
    # 5. 发送邮件
    success = await send_verification_email(email, code)
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification code. Please try again."
        )
    
    return {
        "message": "Verification code sent successfully. Please check your email.",
        "expires_in_minutes": CODE_EXPIRE_MINUTES
    }


async def verify_reset_code(email: str, code: str) -> dict:
    """
    验证密码重置验证码
    
    Args:
        email: 用户邮箱
        code: 验证码
    
    Returns:
        dict: 验证成功消息
    
    Raises:
        HTTPException: 验证码错误、过期等异常
    """
    current_time = datetime.now()
    
    # 1. 检查验证码是否存在
    if email not in reset_codes:
        raise HTTPException(
            status_code=400,
            detail="No verification code found. Please request a new code."
        )
    
    code_data = reset_codes[email]
    
    # 2. 检查验证码是否过期
    if current_time > code_data["expires_at"]:
        # 删除过期的验证码
        del reset_codes[email]
        raise HTTPException(
            status_code=400,
            detail="Verification code has expired. Please request a new code."
        )
    
    # 3. 验证验证码是否正确
    if code_data["code"] != code:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code. Please try again."
        )
    
    # 4. 验证成功，标记为已验证（但不删除，等待重置密码）
    reset_codes[email]["verified"] = True
    
    return {
        "message": "Verification code verified successfully.",
        "email": email
    }


async def reset_password(email: str, code: str, new_password: str, db: AsyncSession) -> dict:
    """
    重置用户密码
    
    Args:
        email: 用户邮箱
        code: 验证码
        new_password: 新密码
        db: 数据库会话
    
    Returns:
        dict: 重置成功消息
    
    Raises:
        HTTPException: 验证失败、密码重置失败等异常
    """
    current_time = datetime.now()
    
    # 1. 验证验证码
    if email not in reset_codes:
        raise HTTPException(
            status_code=400,
            detail="No verification code found. Please request a new code."
        )
    
    code_data = reset_codes[email]
    
    # 2. 检查验证码是否过期
    if current_time > code_data["expires_at"]:
        del reset_codes[email]
        raise HTTPException(
            status_code=400,
            detail="Verification code has expired."
        )
    
    # 3. 检查验证码是否已验证
    if not code_data.get("verified", False):
        raise HTTPException(
            status_code=400,
            detail="Please verify the code first."
        )
    
    # 4. 验证验证码是否正确
    if code_data["code"] != code:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code."
        )
    
    # 5. 获取用户信息
    user = await get_user_by_email(email, db)
    if not user:
        if DEV_MODE:
            # 开发模式：模拟重置成功
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"开发模式：用户 {email} 不存在，模拟重置密码成功")
            del reset_codes[email]
            return {
                "message": "Password reset successfully. Please login with your new password. (DEV MODE)"
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )
    
    # 6. 检查新密码强度
    if len(new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long."
        )
    
    # 7. 更新密码
    hashed_password = get_password_hash(new_password)
    await update_user_password(user.id, hashed_password, db)
    
    # 8. 删除已使用的验证码
    del reset_codes[email]
    
    return {
        "message": "Password reset successfully. Please login with your new password."
    }


def cleanup_expired_codes():
    """
    清理过期的验证码（可定期调用）
    """
    current_time = datetime.now()
    expired_emails = [
        email for email, data in reset_codes.items()
        if current_time > data["expires_at"]
    ]
    
    for email in expired_emails:
        del reset_codes[email]
