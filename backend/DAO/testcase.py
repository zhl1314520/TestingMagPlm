from sqlalchemy import select, func, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models.testcase import TestCase
from models.project import Project


async def get_testcase_by_id(testcase_id: int, db: AsyncSession):
    stmt = select(TestCase).where(TestCase.id == testcase_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_testcase(testcase: TestCase, db: AsyncSession):
    db.add(testcase)
    await db.flush()
    return testcase


async def get_testcase_list(db: AsyncSession, created_by: int,
                            page: int, page_size: int,
                            project_id: int = None, module: str = None,status: str = None,
                            ):
    count_stmt = select(func.count()).select_from(TestCase)
    
    conditions = []
    if project_id:
        conditions.append(TestCase.project_id == project_id)
    if module:
        conditions.append(TestCase.module == module)
    if status:
        conditions.append(TestCase.status == status)

    # 必选参数，直接添加到查询条件中
    conditions.append(TestCase.created_by == created_by)
    
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(TestCase, Project.name)
        .join(Project, TestCase.project_id == Project.id, isouter=True)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(TestCase.id.desc())
    )
    
    if conditions:
        # # 假设三个条件都有值，conditions 列表就是：
        # # [
        # #     TestCase.project_id == 1,
        # #     TestCase.module == "登录模块",
        # #     TestCase.status == "有效"
        # # ]
        # *conditions 解包 -> and_(1, "登录模块", "有效")
        # and_(): 假如 用户传入 3 个条件，相当于 WHERE project_id = 1 AND module = '登录模块' AND status = '有效'
        stmt = stmt.where(and_(*conditions))
    
    result = await db.execute(stmt)
    """
    rows = [
    # 第 1 行（索引 0）
    (
        TestCase 对象 (id=1, project_id=101, module='登录模块', title='用户登录测试', ...),     -> 假设是表 test_cases 中的一行数据
        '电商平台'  # Project.name                                                           -> 假设是表 projects 中的一行数据，Project.name 列的值
    ),
    
    # 第 2 行（索引 1）
    (
        TestCase 对象 (id=2, project_id=101, module='登录模块', title='密码验证测试', ...),
        '电商平台'  # Project.name
    ),
    
    # 第 3 行（索引 2）
    (
        TestCase 对象 (id=3, project_id=102, module='支付模块', title='支付流程测试', ...),
        '支付系统'  # Project.name
    )
]
    """
    rows = result.all()
    
    items = []
    for row in rows:    # rows：整个列表，row：元组
        testcase = row[0]
        project_name = row[1] if row[1] else ""     # 3元表达式 if row[1] -> project_name = row[1], else project_name = ""
        testcase_dict = {
            'id': testcase.id,
            'project_id': testcase.project_id,
            'project_name': project_name,
            'module': testcase.module,
            'title': testcase.title,
            'steps': testcase.steps,
            'expected': testcase.expected,
            'status': testcase.status,
            'priority': testcase.priority,
            'created_by': testcase.created_by,
            'created_at': testcase.created_at,
            'updated_at': testcase.updated_at
        }
        items.append(testcase_dict)

    return total, items


async def delete_testcase(testcase_id: int, db: AsyncSession):
    stmt = delete(TestCase).where(TestCase.id == testcase_id)
    await db.execute(stmt)


async def update_testcase(testcase: TestCase, db: AsyncSession):
    await db.flush()
    return testcase
