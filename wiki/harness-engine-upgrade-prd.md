# PRD: AI Native Pipeline → Harness Engine 升级

> 基于 Claude Code 已有能力，补充 Harness Engineering 核心能力

---

## Claude Code 已有能力（不重复）

| 能力 | Claude Code 实现 | 状态 |
|------|------------------|------|
| Skills / Commands | ✅ 已有 | 直接使用 |
| Agents 机制 | ✅ 已有 | 直接使用 |
| Planning Mode | ✅ `--plan` 参数 | 直接使用 |
| Hooks | ✅ PreToolUse / PostToolUse | 直接使用 |
| MCP 集成 | ✅ 已有 | 直接使用 |
| AGENTS.md 规范 | ✅ 已有 | 直接使用 |

---

## 需要补充的核心能力

### P0 - 必须实现

#### 1. Repository Impact Map（代码影响分析）

**问题**: Agent 不了解代码结构，容易产生文件路径幻觉

**解决方案**: 任务执行前，运行符号分析，生成结构化上下文

**实现**:
```bash
# 新增 Skill: /impact-map
# 调用 ctags / tree-sitter 分析代码
# 输出 Impact Map 供 Agent 参考
```

**输出格式**:
```markdown
## Impact Map: JWT Migration

### Core Files (可修改)
- `src/auth/session.py` - SessionManager (4 methods)
- `src/auth/middleware.py` - authenticate() (12 callers)

### Dependent Files (不可破坏)
- `src/api/routes/*.py` - imports authenticate
- `tests/auth/` - 23 tests

### Patterns (参考)
- `src/api_keys/jwt_util.py` - JWT pattern
```

---

#### 2. Acceptance Criteria 验证器

**问题**: 任务完成后无自动验证，依赖人工检查

**解决方案**: 在 `coding-agent` 后自动运行验证

**实现**:
```markdown
# 新增 Agent: verification-agent.md

---
name: verification-agent
description: 验证代码改动是否符合验收标准
tools: Read, Bash
---

# 验证流程

1. 读取验收标准
2. 执行验证命令
3. 输出验证结果
```

**验证类型**:
```yaml
verifications:
  - type: test
    command: pytest tests/ -v
    expect: exit 0
  
  - type: lint
    command: ruff check src/
    expect: exit 0
  
  - type: grep
    pattern: "Session"
    path: src/auth/
    expect: empty
```

---

#### 3. Feedback Log（错误归因）

**问题**: 重复犯同样的错误，没有学习机制

**解决方案**: 记录错误 → 分类 → 改进 Harness

**实现**:
```markdown
# 新增文件: .harness/feedback-log.md

## Error Log

| 时间 | 任务 | 错误 | 分类 | 改进 |
|------|------|------|------|------|
| 2026-04-27 | JWT迁移 | 用了 python-jose | pattern 缺失 | 添加 JWT pattern 引用 |
| 2026-04-27 | 登录模块 | 文件路径错误 | impact 不完整 | 添加到符号分析 |
```

---

### P1 - 增强体验

#### 4. Task Spec Template（任务规格模板）

**问题**: 任务描述模糊导致错误假设

**解决方案**: 标准化任务输入格式

**模板**:
```markdown
## Task: [任务名称]

### Scope
- Files to modify: [...]
- Files to read (不修改): [...]
- Boundary (不可触碰): [...]

### Pattern to follow
- 参考: `path/to/existing/pattern.py`

### Acceptance Criteria
- [ ] pytest tests/ -v 通过
- [ ] 无 lint 错误
- [ ] 文档已更新

### Out of Scope
- [...]
```

---

#### 5. Session State（会话状态）

**问题**: 中断后无法恢复

**解决方案**: 利用 Claude Code 的 memory 机制

**实现**:
```markdown
# .harness/sessions/{timestamp}/
├── impact-map.md
├── plan.md
├── verification-result.md
└── feedback.md
```

---

## 最小实现（MVP）

只需补充 **2 个核心组件**：

```
ai-native-pipeline/
├── agents/
│   ├── impact-analyzer.md     # 新增：代码影响分析
│   ├── verification-agent.md  # 新增：验收验证
│   ├── prd-agent.md
│   ├── spec-agent.md
│   └── coding-agent.md
│
├── skills/
│   └── pipeline/
│       └── SKILL.md           # 更新：集成新 Agent
│
└── rules/
    └── task-spec-template.md  # 新增：任务规格模板
```

---

## 更新后的 Pipeline 流程

```
用户需求
    │
    ▼
┌─────────────────┐
│ impact-analyzer │ ← 新增：符号分析
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   prd-agent     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   spec-agent    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  coding-agent   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ verification    │ ← 新增：自动验证
│   -agent        │
└────────┬────────┘
         │
         ▼
    完成 ✅
```

---

## 用户故事

### US-001: 代码影响分析
**作为** 开发者，**我希望** 任务开始前自动分析代码影响，**以便** 避免文件路径幻觉。

**验收标准**:
- [ ] 新增 `/impact-analyzer` agent
- [ ] 输出 Core Files / Dependent Files / Boundary
- [ ] 集成到 pipeline 流程

**优先级**: P0

---

### US-002: 自动验证
**作为** 开发者，**我希望** 代码生成后自动验证，**以便** 确保符合验收标准。

**验收标准**:
- [ ] 新增 `/verification-agent` agent
- [ ] 支持测试/lint/grep 验证
- [ ] 输出验证结果

**优先级**: P0

---

### US-003: 任务规格模板
**作为** 开发者，**我希望** 有标准化的任务输入格式，**以便** 减少模糊描述。

**验收标准**:
- [ ] 新增 `task-spec-template.md` rule
- [ ] 包含 Scope / Pattern / Criteria / Out-of-scope

**优先级**: P1

---

### US-004: 错误反馈学习
**作为** 开发者，**我希望** 系统能从错误中学习，**以便** 避免重复犯错。

**验收标准**:
- [ ] 新增 feedback-log 机制
- [ ] 错误分类（pattern 缺失、impact 不完整等）
- [ ] 生成改进建议

**优先级**: P1

---

### US-005: 会话状态持久化
**作为** 开发者，**我希望** 中断后能恢复进度，**以便** 继续未完成的任务。

**验收标准**:
- [ ] 保存 impact-map / plan / verification-result
- [ ] 支持断点续传

**优先级**: P2

---

## 实现计划

| Phase | 功能 | 分支名 | PR |
|-------|------|--------|-----|
| 1 | impact-analyzer | `feat/impact-analyzer` | #2 |
| 2 | verification-agent | `feat/verification-agent` | #3 |
| 3 | task-spec-template | `feat/task-spec-template` | #4 |
| 4 | pipeline 集成 | `feat/pipeline-integration` | #5 |
| 5 | feedback-log | `feat/feedback-log` | #6 |

---

## 参考

- [Harness Engineering Guide](https://www.verdent.ai/guides/harness-engineering-ai-coding-workflow)
- [OpenAI Harness Engineering Field Report](https://openai.com/index/harness-engineering/)
- [Claude Code Documentation](https://code.claude.com/docs)
