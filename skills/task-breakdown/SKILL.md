---
name: task-breakdown
description: 任务拆解与编排
model: sonnet
color: blue
---

# Task Breakdown

## 工作流
SPEC → 任务拆解 → 执行顺序

## 示例

### 输入
```markdown
# 技术规格: 用户登录
## API
- POST /api/auth/login
- POST /api/auth/send-code
## 数据模型
- User, AuthCode
```

### 输出
```markdown
## 任务总览
| ID | 任务 | 依赖 | 执行 |
|----|------|------|------|
| T1 | 后端 - 登录API | - | 串行 |
| T2 | 后端 - 验证码API | T1 | 串行 |
| T3 | 前端 - 登录页 | - | 并行 |
| T4 | 前端 - API调用 | T2 | 串行 |

## 执行阶段
### 阶段1（并行）: T3
### 阶段2（串行）: T1 → T2 → T4
```