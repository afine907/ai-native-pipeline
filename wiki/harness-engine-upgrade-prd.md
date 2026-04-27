# PRD: AI Native Pipeline - 核心流程打磨

> Less is More. 专注全流程编码，打磨核心 Agent 能力。

---

## 核心定位

**一个流程，五个节点**

```
用户需求 → impact-analyzer → prd-agent → spec-agent → coding-agent → verification-agent
```

**目标**: 从自然语言需求，到可运行代码，全自动完成。

---

## 当前流程节点

| 节点 | 职责 | 输出 |
|------|------|------|
| impact-analyzer | 代码影响分析 | Impact Map |
| prd-agent | 需求分析 | Task Spec + PRD |
| spec-agent | 技术规格 | API + 数据模型 |
| coding-agent | 代码实现 | 代码文件 |
| verification-agent | 验收验证 | 验证结果 |

---

## 核心痛点分析

### 痛点 1: impact-analyzer 能力不足

**问题**: 符号分析依赖外部工具（ctags/tree-sitter），不总是可用

**当前实现**: 描述了"怎么做"，但实际执行时：
- ctags 可能未安装
- 不同语言需要不同工具
- 调用关系分析不够智能

**打磨方向**:
- 提供纯文本分析能力（grep + AST）
- 支持无工具降级方案
- 增强"模式发现"能力

---

### 痛点 2: 各 Agent 上下文传递不清晰

**问题**: Agent 之间靠文件传递，但不知道"上一个 Agent 看到了什么"

**示例**:
```
coding-agent 收到 spec.md，但不知道：
- impact-analyzer 发现了哪些风险
- prd-agent 为什么这样划分优先级
- spec-agent 为什么选择这个 API 设计
```

**打磨方向**:
- 强化 task-spec 的"单一事实源"地位
- 让每个 Agent 的关键决策写入 task-spec
- 后续 Agent 从 task-spec 获取完整上下文

---

### 痛点 3: verification 依赖预设标准

**问题**: 验收标准需要人工预定义

**当前实现**:
```yaml
verifications:
  - type: test
    command: pytest tests/ -v
```

**问题**:
- 用户可能不知道怎么写验收标准
- 验收标准可能不完整

**打磨方向**:
- verification-agent 应能"推断"验收标准
- 从 spec 中自动提取验证项
- 例如：spec 定义了 API → 自动生成 API 测试验证

---

### 痛点 4: 单个 Agent 能力可提升

**每个 Agent 都可以更聪明**:

| Agent | 当前 | 可提升 |
|-------|------|--------|
| impact-analyzer | 文件列表 | 调用关系图、风险评分 |
| prd-agent | 功能列表 | 用户旅程、边界场景 |
| spec-agent | API 定义 | 接口契约、错误处理 |
| coding-agent | TDD | 增量修改、代码复用 |
| verification-agent | 执行命令 | 智能推断验证项 |

---

## 去掉的功能

| 功能 | 原因 |
|------|------|
| ❌ Feedback Log | 不在工作流中，事后分析 |
| ❌ MCP 集成 | 系统集成，非核心能力 |
| ❌ 会话断点续传 | 锦上添花 |
| ❌ 智能 Planning Gate | 体验优化，非核心 |
| ❌ code-review 集成 | 可独立使用 |

---

## 打磨计划

### Phase 1: 强化 task-spec（1天）

**目标**: task-spec 成为"单一事实源"

```markdown
# Task Spec

## 上下文（来自 impact-analyzer）
- Core Files: ...
- Risks: ...

## 需求（来自 prd-agent）
- 功能列表: ...
- 验收标准: ...

## 技术决策（来自 spec-agent）
- API 设计: ...
- 为什么这样设计: ...

## 实现记录（来自 coding-agent）
- 修改文件: ...
- 关键改动: ...
```

---

### Phase 2: 提升 impact-analyzer（1天）

**目标**: 无外部依赖也能分析

**增强能力**:
- 纯文本 grep 分析
- import/require 依赖分析
- 函数调用关系（简单版）
- 风险评分算法

---

### Phase 3: 增强 verification-agent（1天）

**目标**: 从 spec 自动推断验收标准

**示例**:
```
spec 定义: POST /api/auth/login
→ 自动添加验证: curl 测试登录接口

spec 定义: 数据模型 User
→ 自动添加验证: 检查数据库 schema
```

---

### Phase 4: Agent 决策可追溯（1天）

**目标**: 每个 Agent 输出"为什么这样做"

**示例**:
```markdown
## spec-agent 决策记录

### 为什么选择 REST API 而非 GraphQL？
- 项目已有 REST 基础设施
- 团队更熟悉 REST
- 性能要求不高

### 为什么用 JWT 而非 Session？
- 需要跨服务认证
- 项目已有 JWT 工具类（参考 src/api_keys/jwt_util.py）
```

---

## 成功指标

| 指标 | 目标 |
|------|------|
| 无外部依赖 | impact-analyzer 在无 ctags 时仍能工作 |
| 上下文完整 | coding-agent 看到完整决策链 |
| 验收自动化 | 80% 验收标准自动推断 |
| 决策可追溯 | 每个 Agent 输出决策理由 |

---

## 总结

**Keep Focus**: 五个节点，每个打磨到极致

```
impact-analyzer  →  更智能的代码分析
prd-agent        →  更完整的需求规格
spec-agent       →  更清晰的技术决策
coding-agent     →  更精准的代码实现
verification-agent → 更智能的验收验证
```

**Less is More**: 不加节点，只增强能力
