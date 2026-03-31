# 二、后端 API 设计规范文档（Backend API Spec）

## 1️⃣ 分层架构（推荐）

```
router → service → DAO → model

backend/
│
├── router/        # 路由层
├── service/       # 业务层
├── DAO/           # 数据访问层				 怎么操作这些数据（增删改查）
├── model/         # 数据库模型（ORM）			数据结构（表长什么样）
├── schema/        # 入参/出参（Pydantic）	API 的数据契约（输入 + 输出格式）,
											  👉 用来“约束前后端传的数据长什么样”
├── core/          # 配置、权限、中间件
```

------

## 2️⃣ 命名规范

| 类型    | 规范        |
| ------- | ----------- |
| 路由    | RESTful     |
| 方法名  | 动词+名词   |
| Service | xxx_service |
| 表名    | snake_case  |

------

## 3️⃣ 示例（FastAPI）

### Router

```
@router.post("/users")
async def create_user(user: UserCreate, db: Session):
    return await user_service.create_user(user, db)
```

------

### Service

```
class UserService:

    async def create_user(self, user, db):
        return await user_repo.create(db, user)
```

------

### DAO

```
class UserDAO:

    async def create(self, db, user):
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
```

------

## 4️⃣ 通用能力设计

### 分页

```
{
  "list": [],
  "total": 100,
  "page": 1,
  "page_size": 10
}
```

------

### 权限（RBAC）

中间件实现：

```
@require_role("admin")
```

------

### 日志

- 操作日志
- API日志
- 错误日志

------

### 异常处理

```
raise HTTPException(status_code=400, detail="参数错误")
```

------

### 鉴权

- JWT
- Token 过期刷新

------

## 5️⃣ CI/CD 集成点

```
POST /executions/trigger
```

支持：

- Jenkins webhook
- GitLab webhook