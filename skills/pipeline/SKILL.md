---
name: pipeline
description: AI Native开发全流程
model: sonnet
color: purple
---

# Pipeline

## 工作流
module-context → prd-agent → spec-agent → coding-agent

## 会话机制

### 会话文件结构
```
.pipeline-sessions/
└── session-{timestamp}/
    ├── 00-module-context.md
    ├── 01-prd.md
    ├── 02-spec.md
    ├── 03-code.md
    └── meta.json
```

### 执行流程

```
1. 创建会话目录
2. Step1: 读取上一步(无) → module-context → 写入 00-module-context.md
3. Step2: 读取 00-module-context.md → prd-agent → 写入 01-prd.md
4. Step3: 读取 01-prd.md → spec-agent → 写入 02-spec.md
5. Step4: 读取 02-spec.md → coding-agent → 写入 03-code.md
```

### 断点续传
- 如果会话目录已存在，检查已完成的步骤
- 跳过的步骤直接读取上一步输出作为输入
- 从未完成的步骤继续执行

## 示例

### 输入
```
/pipeline 用户需要一个登录功能
```

### 执行
```
[创建] .pipeline-sessions/session-20260101-120000/

[Step1] module-context
  ← 读取: 无
  → 调用: /module-context
  → 写入: 00-module-context.md
  ← 读取: 00-module-context.md
  → 调用: /prd-agent "用户需要一个登录功能"
  → 写入: 01-prd.md

[Step2] prd-agent
  ← 读取: 00-module-context.md
  → 调用: /prd-agent
  → 写入: 01-prd.md

[Step3] spec-agent
  ← 读取: 01-prd.md
  → 调用: /spec-agent
  → 写入: 02-spec.md

[Step4] coding-agent
  ← 读取: 02-spec.md
  → 调用: /coding-agent
  → 写入: 03-code.md
```

### 输出
```markdown
# 开发完成 ✅

## 会话文件
.pipeline-sessions/session-20260101-120000/
├── 00-module-context.md
├── 01-prd.md
├── 02-spec.md
└── 03-code.md

## 代码文件
[写入的文件列表]
```

## 后续扩展
- `/task-breakdown` - 任务拆解
- `/code-review` - 代码审查
- `/test-generator` - 测试生成