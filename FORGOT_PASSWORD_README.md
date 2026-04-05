# 忘记密码功能实现说明

## 功能概述

忘记密码功能允许用户通过邮箱验证的方式重置密码。整个流程分为三个步骤：

1. **发送验证码** - 用户输入邮箱，系统发送验证码到该邮箱
2. **验证验证码** - 用户输入收到的验证码，系统验证其有效性
3. **重置密码** - 验证通过后，用户设置新密码

## 后端实现

### API 端点

所有密码重置相关的端点都在 `/password-reset` 路径下：

#### 1. 发送验证码
```http
POST /password-reset/send-code?email=user@example.com
```

**参数：**
- `email` (query): 用户的邮箱地址

**响应：**
```json
{
  "message": "Verification code sent successfully. Please check your email.",
  "expires_in_minutes": 10
}
```

**错误情况：**
- 404: 邮箱不存在
- 429: 发送频率过高或达到最大发送次数
- 500: 邮件发送失败

#### 2. 验证验证码
```http
POST /password-reset/verify-code?email=user@example.com&code=123456
```

**参数：**
- `email` (query): 用户的邮箱地址
- `code` (query): 验证码

**响应：**
```json
{
  "message": "Verification code verified successfully.",
  "email": "user@example.com"
}
```

**错误情况：**
- 400: 验证码错误、过期或不存在

#### 3. 重置密码
```http
POST /password-reset/reset-password?email=user@example.com&code=123456&new_password=newpass123
```

**参数：**
- `email` (query): 用户的邮箱地址
- `code` (query): 已验证的验证码
- `new_password` (query): 新密码（至少 6 个字符）

**响应：**
```json
{
  "message": "Password reset successfully. Please login with your new password."
}
```

### 后端文件修改

1. **DAO/user.py** - 添加了 `update_user_password` 函数
2. **routers/user.py** - 添加了密码重置路由和端点
3. **main.py** - 注册了 `password_reset_router`
4. **services/password_reset.py** - 已存在的密码重置服务（无需修改）

## 前端实现

### 页面路由

1. **/forgot-password** - 忘记密码页面（输入邮箱和验证码）
2. **/reset-password** - 重置密码页面（设置新密码）
3. **/reset-password-success** - 重置成功页面

### API 调用

在 `frontend/src/api/index.js` 中添加了三个新的 API 方法：

```javascript
export const authAPI = {
  // ... 其他方法
  sendResetCode: (email) => api.post('/password-reset/send-code', null, { params: { email } }),
  verifyResetCode: (email, code) => api.post('/password-reset/verify-code', null, { params: { email, code } }),
  resetPassword: (email, code, newPassword) => api.post('/password-reset/reset-password', null, { params: { email, code, new_password: newPassword } })
}
```

### 前端文件修改

1. **router/index.js** - 添加了忘记密码和重置密码的路由
2. **Login/ForgotPassword.vue** - 已存在的忘记密码页面（已更新跳转逻辑）
3. **Login/ResetPassword.vue** - 新创建的重置密码页面
4. **Login/ResetPasswordSuccess.vue** - 已存在的成功页面

## 用户流程

```
登录页面
   ↓ (点击 "Forgot password?")
忘记密码页面
   ↓ (输入邮箱 → 点击 "Get Code")
   ↓ (输入验证码 → 点击 "Verify & Continue")
重置密码页面
   ↓ (输入新密码 → 点击 "Reset Password")
登录页面 (自动跳转)
```

## 安全特性

1. **验证码有效期** - 10 分钟后自动过期
2. **发送频率限制** - 60 秒内只能发送一次
3. **最大发送次数** - 最多发送 3 次
4. **邮箱验证** - 只有已注册的邮箱才能请求验证码
5. **密码强度** - 新密码至少 6 个字符

## 测试方法

### 手动测试

1. 启动后端服务：
   ```bash
   cd backend
   python main.py
   ```

2. 启动前端服务：
   ```bash
   cd frontend
   npm run dev
   ```

3. 访问 `http://localhost:5173/login`

4. 点击 "Forgot password?" 链接

5. 按照流程完成密码重置

## 邮件配置

在 `backend/services/email.py` 中配置 SMTP 服务器：

```python
SMTP_CONFIG = {
    "hostname": "smtp.example.com",
    "port": 587,
    "username": "your-email@example.com",
    "password": "your-password",
    "use_tls": True,
    "from_email": "your-email@example.com",
    "from_name": "TestingMagPlm"
}
```

**注意：** 实际部署时应从环境变量读取这些配置。

## 注意事项

1. **开发环境** - 当前验证码存储在内存中（`reset_codes` 字典），重启服务后会丢失
2. **生产环境** - 建议使用 Redis 或其他持久化存储来保存验证码
3. **邮件服务** - 需要配置有效的 SMTP 服务器才能发送邮件
4. **CORS 配置** - 后端已配置允许跨域请求

## 常见问题

### Q: 验证码一直收不到？
A: 检查 SMTP 配置是否正确，或者查看后端日志中的错误信息。

### Q: 提示 "Email not found"？
A: 确保输入的邮箱地址已在数据库中注册。

### Q: 验证码验证失败？
A: 检查验证码是否正确输入，注意区分大小写（虽然当前实现是纯数字）。

## 下一步优化建议

1. 使用 Redis 存储验证码
2. 添加图形验证码防止机器人
3. 增加密码强度验证
4. 添加密码历史记录（防止重复使用旧密码）
5. 发送密码重置成功通知邮件
