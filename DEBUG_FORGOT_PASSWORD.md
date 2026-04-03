# 忘记密码功能调试指南

## 问题排查步骤

### 1. 检查前端路由是否工作

打开浏览器，手动访问以下 URL，看是否能正常显示页面：

- `http://localhost:5173/forgot-password` - 忘记密码页面
- `http://localhost:5173/reset-password` - 重置密码页面

**如果 404 或白屏**：
- 检查前端是否正常运行（终端是否有错误）
- 检查路由配置是否正确
- 查看浏览器控制台（F12）的错误信息

### 2. 检查"Forgot password?"链接

在登录页面 `http://localhost:5173/login`：
- 右键点击 "Forgot password?" 链接
- 选择"检查"（Inspect）
- 确认 HTML 是 `<a href="/forgot-password" ...>` 而不是普通的 `<a>` 标签
- 点击链接，看 URL 是否变化

### 3. 检查后端 API 是否可访问

在浏览器中访问后端 Swagger 文档：
- `http://localhost:8000/docs`
- 查看是否有 `/password-reset/` 相关的三个端点

或者使用 PowerShell 测试：
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method GET
```

### 4. 测试 API 调用

在浏览器控制台（F12）中执行：
```javascript
fetch('http://localhost:8000/password-reset/send-code?email=test@example.com', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
}).then(r => r.json()).then(console.log)
```

### 5. 查看网络请求

在浏览器控制台（F12）：
- 切换到 "Network"（网络）标签
- 点击 "Get Code" 按钮
- 查看是否有请求发出
- 请求的 URL、状态码、响应内容是什么

## 常见问题

### 问题 1：点击链接没反应
**原因**：路由配置错误或路由守卫拦截
**解决**：已修复路由守卫，将忘记密码页面加入公开访问列表

### 问题 2：页面 404
**原因**：路由未配置或前端未热更新
**解决**：重启前端开发服务器

### 问题 3：API 调用失败（Network Error）
**原因**：后端未启动或 CORS 配置问题
**解决**：
- 检查后端是否运行在 `http://localhost:8000`
- 检查 CORS 配置（已在 main.py 中配置）

### 问题 4：邮箱不存在错误
**原因**：数据库中无此邮箱
**解决**：先注册一个测试账号

## 快速测试命令

### 重启前端
```bash
cd frontend
npm run dev
```

### 重启后端
```bash
cd backend
python -m uvicorn main:app --reload
```

## 预期的完整流程

1. 访问 `http://localhost:5173/login`
2. 点击 "Forgot password?" → 跳转到 `/forgot-password`
3. 输入邮箱 → 点击 "Get Code" → 发送邮件
4. 输入验证码 → 点击 "Verify & Continue" → 跳转到 `/reset-password`
5. 输入新密码 → 点击 "Reset Password" → 跳转到 `/login`
6. 使用新密码登录
