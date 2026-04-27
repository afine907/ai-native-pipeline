---
name: task-breakdown
description: 任务拆解与编排 - 当 SPEC 复杂度高时自动触发
model: sonnet
color: blue
---

# Task Breakdown

## 触发条件

Pipeline 会自动判断是否触发此 Skill：

| 条件 | 阈值 | 触发 |
|------|------|------|
| API 数量 | > 3 | ✅ 自动触发 |
| 涉及模块 | > 2 | ✅ 自动触发 |
| 前后端 | 都有 | ✅ 自动触发 |

## 工作流

```
SPEC → 复杂度判断 → 任务拆解 → 执行计划
```

## 输入格式

```markdown
# 技术规格: [模块名称]

## API
- POST /api/auth/login
- POST /api/auth/send-code
- GET /api/auth/user
- POST /api/auth/logout
- POST /api/auth/refresh

## 数据模型
- User
- AuthCode
- Session

## 前端组件
- LoginPage
- UserProfile
```

## 输出格式

```markdown
# Task Breakdown: [模块名称]

Generated: 2026-04-27T12:00:00Z

## 复杂度分析
- API 数量: 5 (高)
- 涉及模块: 2 (后端 + 前端)
- 自动触发: ✅ 是

## 任务总览

| ID | 任务 | 依赖 | 执行 | 估时 |
|----|------|------|------|------|
| T1 | 后端 - 登录 API | - | 并行 | 2h |
| T2 | 后端 - 验证码 API | - | 并行 | 1h |
| T3 | 后端 - 用户信息 API | T1 | 串行 | 1h |
| T4 | 后端 - Token 刷新 API | T1 | 串行 | 1h |
| T5 | 前端 - 登录页 | - | 并行 | 2h |
| T6 | 前端 - 用户信息页 | T3 | 串行 | 1h |
| T7 | 集成测试 | T1-T6 | 串行 | 2h |

## 执行阶段

### 阶段 1（并行）
- T1: 后端 - 登录 API
- T2: 后端 - 验证码 API
- T5: 前端 - 登录页

### 阶段 2（串行）
- T3: 后端 - 用户信息 API (依赖 T1)
- T4: 后端 - Token 刷新 API (依赖 T1)

### 阶段 3（串行）
- T6: 前端 - 用户信息页 (依赖 T3)

### 阶段 4（串行）
- T7: 集成测试 (依赖 T1-T6)

## 风险点
- T1 是关键路径，延迟会影响 T3, T4, T6
- 前后端可并行，但需要提前约定 API 接口

## 验收标准
- [ ] 所有 API 测试通过
- [ ] 前端页面功能正常
- [ ] 集成测试覆盖核心流程
```

## 任务依赖图

```
      T1 ─────┬───── T3 ─── T6
       │      │
       │      └───── T4
       │
      T2      T5
       │       │
       └───┬───┘
           │
          T7
```

## 与 Pipeline 集成

此 Skill 在 Pipeline 中自动调用：

```
Pipeline Step3: spec-agent
         │
         ▼
  复杂度判断 → 高 → 自动调用 task-breakdown
         │
         ▼
  按阶段逐个执行 coding-agent + verification-agent
```

## 手动调用

也可以手动触发：

```bash
/task-breakdown
# 输入从上下文或 03-spec.md 读取
```