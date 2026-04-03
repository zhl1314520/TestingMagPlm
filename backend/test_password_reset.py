# 测试忘记密码流程
# 使用此脚本测试密码重置 API 端点

import requests
import random
import string

BASE_URL = "http://localhost:8000"

def generate_test_email():
    """生成一个测试邮箱地址"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

def test_password_reset_flow():
    """测试完整的密码重置流程"""
    print("=" * 60)
    print("忘记密码流程测试")
    print("=" * 60)
    
    # 步骤 1: 使用已存在的邮箱（需要先创建一个测试用户）
    print("\n[步骤 1] 发送密码重置验证码")
    print("-" * 60)
    
    # 注意：这里应该使用数据库中已存在的邮箱
    test_email = "test@example.com"  # 替换为实际的测试邮箱
    
    try:
        response = requests.post(
            f"{BASE_URL}/password-reset/send-code",
            params={"email": test_email}
        )
        
        if response.status_code == 200:
            print(f"✓ 验证码发送成功")
            print(f"响应：{response.json()}")
        else:
            print(f"✗ 验证码发送失败")
            print(f"状态码：{response.status_code}")
            print(f"响应：{response.json()}")
            return
            
    except Exception as e:
        print(f"✗ 请求失败：{str(e)}")
        return
    
    # 步骤 2: 验证验证码（需要输入实际收到的验证码）
    print("\n[步骤 2] 验证验证码")
    print("-" * 60)
    print("请输入您收到的验证码（或输入 'skip' 跳过）：")
    test_code = input("验证码：").strip()
    
    if test_code.lower() != 'skip':
        try:
            response = requests.post(
                f"{BASE_URL}/password-reset/verify-code",
                params={"email": test_email, "code": test_code}
            )
            
            if response.status_code == 200:
                print(f"✓ 验证码验证成功")
                print(f"响应：{response.json()}")
            else:
                print(f"✗ 验证码验证失败")
                print(f"状态码：{response.status_code}")
                print(f"响应：{response.json()}")
                return
                
        except Exception as e:
            print(f"✗ 请求失败：{str(e)}")
            return
    
    # 步骤 3: 重置密码
    print("\n[步骤 3] 重置密码")
    print("-" * 60)
    new_password = "newpassword123"  # 测试用新密码
    
    try:
        response = requests.post(
            f"{BASE_URL}/password-reset/reset-password",
            params={
                "email": test_email,
                "code": test_code,
                "new_password": new_password
            }
        )
        
        if response.status_code == 200:
            print(f"✓ 密码重置成功")
            print(f"响应：{response.json()}")
        else:
            print(f"✗ 密码重置失败")
            print(f"状态码：{response.status_code}")
            print(f"响应：{response.json()}")
            return
            
    except Exception as e:
        print(f"✗ 请求失败：{str(e)}")
        return
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print(f"\n新密码：{new_password}")
    print(f"邮箱：{test_email}")
    print("\n请使用新密码登录测试。")

if __name__ == "__main__":
    test_password_reset_flow()
