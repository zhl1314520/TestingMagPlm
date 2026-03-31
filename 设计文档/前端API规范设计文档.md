# 一、前端 API 设计规范文档（Frontend API Spec）

## 1️⃣ 基础规范

### 1.1 请求基础

- Base URL：

```
/api/v1
```

- 请求格式：

```
Content-Type: application/json
Authorization: Bearer <token>
```

------

### 1.2 统一响应格式

```
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": 1710000000
}
```

### 状态码定义

| code | 含义       |
| ---- | ---------- |
| 0    | 成功       |
| 400  | 参数错误   |
| 401  | 未认证     |
| 403  | 无权限     |
| 404  | 资源不存在 |
| 500  | 系统错误   |

------

## 2️⃣ 用户与权限模块

### 登录

```
POST /auth/login
```

**请求**

```
{
  "username": "admin",
  "password": "123456"
}
```

**响应**

```
{
  "token": "xxx",
  "user_info": {
    "id": 1,
    "role": "admin"
  }
}
```

------

### 获取当前用户信息

```
GET /auth/me
```

------

### 用户列表

```
GET /users?page=1&page_size=10
```

------

### 创建用户

```
POST /users
```

------

### 删除用户

```
DELETE /users/{id}
```

------

## 3️⃣ 项目管理

### 项目列表

```
GET /projects
```

### 创建项目

```
POST /projects
{
  "name": "测试平台",
  "description": "xxx",
  "owner_id": 1
}
```

------

### 项目成员管理

```
POST /projects/{id}/members
```

------

## 4️⃣ 测试用例模块

### 用例列表

```
GET /testcases
```

支持参数：

- project_id
- module
- status

------

### 创建用例

```
POST /testcases
```

------

### 导入用例

```
POST /testcases/import
```

------

### 导出用例

```
GET /testcases/export
```

------

## 5️⃣ 测试执行

### 执行测试

```
POST /executions/run
{
  "project_id": 1,
  "type": "auto",
  "env": "test"
}
```

------

### 执行记录

```
GET /executions
```

------

## 6️⃣ 缺陷管理

### 缺陷列表

```
GET /bugs
```

------

### 创建缺陷

```
POST /bugs
```

------

### 更新缺陷状态

```
PUT /bugs/{id}/status
```

------

## 7️⃣ 报告模块

```
GET /reports
```

------

## 8️⃣ 数据统计

```
GET /metrics/overview
GET /metrics/trend
```