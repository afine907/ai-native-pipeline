---
name: pipeline
description: AI Native开发全流程 - Harness Engine
model: sonnet
color: purple
---

# Pipeline (Harness Engine)

## 工作流

```
impact-analyzer → prd-agent → spec-agent → coding-agent → verification-agent
```

### 阶段说明

| 阶段 | Agent | 职责 |
|------|-------|------|
| 1️⃣ 分析 | impact-analyzer | 代码影响分析，生成 Impact Map |
| 2️⃣ 需求 | prd-agent | 需求分析，生成 PRD |
| 3️⃣ 规格 | spec-agent | 技术规格设计 |
| 4️⃣ 编码 | coding-agent | 代码实现 |
| 5️⃣ 验证 | verification-agent | 验收标准验证 |

## 会话机制

### 会话文件结构
```
.harness/sessions/
└── session-{timestamp}/
    ├── 00-impact-map.md      # 代码影响分析
    ├── 01-task-spec.md       # 任务规格
    ├── 02-prd.md             # PRD 文档
    ├── 03-spec.md            # 技术规格
    ├── 04-code.md            # 代码实现
    ├── 05-verification.md    # 验证结果
    └── meta.json             # 元数据
```

### 执行流程

```
1. 创建会话目录 .harness/sessions/session-{timestamp}/
2. Step1: impact-analyzer → 分析代码影响 → 写入 00-impact-map.md
3. Step2: prd-agent → 需求分析 → 写入 01-task-spec.md + 02-prd.md
4. Step3: spec-agent → 技术规格 → 写入 03-spec.md
5. Step4: coding-agent → 代码实现 → 写入 04-code.md
6. Step5: verification-agent → 验证结果 → 写入 05-verification.md
```

### 断点续传
- 如果会话目录已存在，检查已完成的步骤
- 跳过的步骤直接读取上一步输出作为输入
- 从未完成的步骤继续执行

### Planning Gate（人工审核点）

在关键阶段设置人工确认：

```
Step2 完成后 → [PAUSE] 用户确认任务规格 → 继续 Step3
Step4 完成后 → [PAUSE] 用户确认代码改动 → 继续 Step5
```

用户输入：
- `[APPROVED]` - 继续执行
- `[REJECTED: 反馈内容]` - 返回上一步重新执行

## 示例

### 输入
```
/pipeline 将登录模块从 session 改为 JWT
```

### 执行
```
[创建] .harness/sessions/session-20260427-120000/

[Step1] impact-analyzer
  → 分析代码影响
  → 写入: 00-impact-map.md
  
  Impact Map:
  - Core Files: src/auth/session.py, src/auth/middleware.py
  - Dependent Files: src/api/routes/*.py (12 callers)
  - Boundary: src/payments/, src/admin/auth.py
  - Pattern: src/api_keys/jwt_util.py

[Step2] prd-agent
  ← 读取: 00-impact-map.md
  → 生成任务规格和 PRD
  → 写入: 01-task-spec.md, 02-prd.md
  
  Task Spec:
  - Files to Modify: session.py, middleware.py
  - Acceptance Criteria: tests pass, no Session references
  
  [PAUSE] 等待用户确认任务规格
  用户输入: [APPROVED]

[Step3] spec-agent
  ← 读取: 02-prd.md
  → 设计技术规格
  → 写入: 03-spec.md
  
  API Design:
  - POST /auth/login → JWT token
  - Middleware: validate JWT header

[Step4] coding-agent
  ← 读取: 03-spec.md
  → 实现代码
  → 写入: 04-code.md
  
  Modified Files:
  - src/auth/jwt_manager.py
  - src/auth/middleware.py
  
  [PAUSE] 等待用户确认代码改动
  用户输入: [APPROVED]

[Step5] verification-agent
  → 执行验收标准验证
  → 写入: 05-verification.md
  
  Results:
  | Check | Status |
  |-------|--------|
  | pytest tests/auth/ | ✅ Pass |
  | ruff check src/auth/ | ✅ Pass |
  | grep "Session" src/auth/ | ✅ Pass |
```

### 输出
```markdown
# 开发完成 ✅

## 会话文件
.harness/sessions/session-20260427-120000/
├── 00-impact-map.md      # 代码影响分析
├── 01-task-spec.md       # 任务规格
├── 02-prd.md             # PRD 文档
├── 03-spec.md            # 技术规格
├── 04-code.md            # 代码实现
└── 05-verification.md    # 验证结果

## 修改的文件
- src/auth/jwt_manager.py (新建)
- src/auth/middleware.py (修改)
- src/auth/models.py (修改)

## 验证结果
✅ 所有验收标准通过
```

## 后续扩展

- `/task-breakdown` - 任务拆解
- `/code-review` - 代码审查
- `/test-generator` - 测试生成
- `/feedback-log` - 错误反馈学习

## Harness Engineering 原则

本 Pipeline 遵循 Harness Engineering 最佳实践：

1. **Impact Map First** - 先分析代码影响，再开始编码
2. **Structured Task Spec** - 标准化任务规格，减少歧义
3. **Planning Gate** - 关键节点人工确认，捕获错误假设
4. **Auto Verification** - 自动验证验收标准，确保质量
5. **Feedback Loop** - 记录错误，持续改进 Harness