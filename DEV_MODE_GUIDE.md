# 忘记密码功能 - 开发模式说明

## 修改内容

已修改以下文件，添加开发模式支持：

1. **backend/services/email.py**
   - 添加 `DEV_MODE` 环境变量支持（默认为 true）
   - 邮件发送失败时，在控制台打印验证码并返回成功

2. **backend/services/password_reset.py**
   - 添加 `DEV_MODE` 环境变量支持（默认为 true）
   - 跳过邮箱存在性检查，允许任意邮箱发送验证码
   - 重置密码时，如果用户不存在，模拟重置成功

## 如何测试

### 1. 重启后端服务

**重要：必须重启后端服务才能生效！**

```bash
# 停止当前运行的后端服务（Ctrl+C）
# 然后重新启动
cd backend
python -m uvicorn main:app --reload
```

### 2. 测试忘记密码流程

1. 访问 `http://localhost:5173/login`
2. 点击 "Forgot password?"
3. 输入任意邮箱地址（例如：`test@example.com`）
4. 点击 "Get Code" 按钮
5. 查看后端控制台，会打印验证码：
   ```
   ============================================================
   开发模式：验证码
   收件人：test@example.com
   验证码：123456
   ============================================================
   ```
6. 复制验证码，输入到前端页面
7. 点击 "Verify & Continue"
8. 设置新密码
9. 完成！

## 预期效果

### 前端
- 点击 "Get Code" 后，按钮显示 60s 倒计时
- 显示成功消息："Verification code sent to your email!"
- 可以输入验证码并继续

### 后端控制台
```
开发模式：邮箱 test@example.com 不存在于数据库中，但仍允许发送验证码
============================================================
开发模式：验证码
收件人：test@example.com
验证码：123456
============================================================
```

## 生产环境配置

在生产环境中，需要设置环境变量：

```bash
# 禁用开发模式
export DEV_MODE=false

# 配置真实的 SMTP 服务器
export SMTP_HOSTNAME=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export SMTP_FROM_EMAIL=your-email@gmail.com
export SMTP_FROM_NAME=TestingMagPlm
```

## 常见问题

### Q: 点击 "Get Code" 没有反应？
A: 
1. 检查后端是否重启
2. 查看浏览器控制台（F12）是否有错误
3. 查看后端控制台是否有错误日志

### Q: 验证码在哪里查看？
A: 在开发模式下，验证码会打印在后端控制台中。

### Q: 倒计时没有开始？
A: 这意味着 API 调用失败了。请检查：
1. 后端是否正常运行
2. 后端是否已重启
3. 浏览器控制台的错误信息

## 开发模式的好处

1. **无需配置邮件服务器** - 开发时不需要真实的 SMTP 服务器
2. **测试任意邮箱** - 不需要邮箱在数据库中存在
3. **快速验证流程** - 验证码直接打印在控制台，方便测试
4. **生产安全** - 生产环境设置 `DEV_MODE=false` 即可启用完整验证
