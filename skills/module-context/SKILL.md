---
name: module-context
description: 模块感知 - 了解目标模块的代码结构、依赖、现有实现
model: sonnet
color: cyan
---

# Module Context

## 工作流
判断模块类型 → 扫描/跳过 → 上下文报告

## 关键原则（参考，非强制）
- 首次使用需确认模块类型
- 增量开发需要分析现有模块
- 全新模块直接跳过，进入 PRD 阶段

## 流程

### Step 1: 询问用户
```
Q: 这是全新模块还是增量开发？
A: 1) 全新模块
   2) 增量开发
```

### Step 2A: 全新模块
```
→ 直接跳过 module-context
→ 进入 prd-agent
```

### Step 2B: 增量开发
```
Q: 请输入目标模块路径（如 src/features/user）
→ 扫描目录结构
→ 分析现有 API 和组件
→ 输出模块上下文
```

## 示例

### 示例1: 全新模块
**输入**:
```
/pipeline 用户需要一个全新的商品模块
```
**执行**:
```
Q: 这是全新模块还是增量开发？
A: 全新模块

→ 跳过 module-context
→ 直接进入 prd-agent
```

### 示例2: 增量开发
**输入**:
```
/pipeline 需要在用户模块增加手机号登录功能
```
**执行**:
```
Q: 这是全新模块还是增量开发？
A: 增量开发

Q: 请输入目标模块路径
A: src/features/user

→ 扫描 src/features/user
→ 输出模块上下文
→ 进入 prd-agent（包含增量功能分析）
```

### 输出（增量开发）
```markdown
# 模块上下文: user

## 现有API
- getUser()
- updateUser()
- login(email, password)

## 现有组件
- UserList
- UserDetail
- UserForm

## 增量功能点
- 新增: 手机号登录 (login(phone, code))

## 依赖
- 需调用现有的 AuthService
- 复用 User 类型
```

> 项目级上下文见 CLAUDE.md