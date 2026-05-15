# GitHub Actions 配置指南

## 1. 配置 API Keys

### LongCat API Key（Agent 评估）

1. 进入 GitHub 仓库
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 填写：
   - **Name**: `LONGCAT_API_KEY`
   - **Value**: 你的 LongCat API Key（格式：`ak_xxx`）
5. 点击 `Add secret`

配置完成后，现有的 CI 流水线（lint + test + plugin 验证 + Agent 评估）会自动使用该 Key 运行评估。

### Claude Code 集成（自动复用 LongCat API Key）

Claude Code CI 集成**复用已有的 `LONGCAT_API_KEY`**，通过配置 `ANTHROPIC_BASE_URL` 路由到 LongCat 的 Anthropic 兼容端点，无需额外密钥。

配置详情：[LongCat Claude Code 文档](https://longcat.chat/platform/docs/ClaudeCode.html)

## 2. 工作流说明

### CI（`ci.yml` — 自动触发）

每次 push 或 PR 到 master 分支自动运行：

```
jobs:
  lint:              # ruff 代码检查
  test:              # Python 脚本语法验证 + 测试任务生成
  plugin-test:       # Claude Code Plugin 文件结构验证
  agent-evaluation:  # Agent 效果评估（需要 LONGCAT_API_KEY）
```

### E2E Test（`e2e-test.yml` — 手动/定时）

完整流水线端到端测试，每天凌晨 2 点自动运行。

```
1. 创建测试项目
2. 运行 impact-analyzer
3. 运行 prd-agent
4. 运行 spec-agent
5. LLM Judge 评估所有 Agent
6. 质量门禁检查（均分 ≥ 3.5）
```

### Claude Code Integration（`claude-code-test.yml` — 自动/手动）

**真正运行 Claude Code CLI** 来测试 Agent 行为，而不是只检查文件结构。

**触发条件**：
- 手动触发（`workflow_dispatch`）
- Agent / Skill / Rule 文件变更的 PR
- Agent / Skill 文件变更的 push

**包含 3 个 Job**：

| Job | 说明 |
|-----|------|
| `plugin-smoke-test` | 安装 Claude Code CLI，创建测试项目，运行 `impact-analyzer`，验证输出包含关键字段 |
| `agent-eval` | 矩阵并行评估 3 个 Agent（impact-analyzer / prd-agent / spec-agent），分别提交不同测试任务 |
| `notify` | 汇总测试结果 |

**前提**：设置了 `ANTHROPIC_API_KEY` Secret。

### Release（`release.yml` — 自动）

Release 发布时：

```
1. 生成 Changelog
2. 打包 artifacts（agents/, skills/, rules/ 等）
```

### Security（`security.yml` — 定时/手动）

每周一执行安全扫描：

```
1. Bandit 安全审计
2. Safety 依赖检查
```

## 3. 质量门禁

### Agent 评估门禁（ci.yml）

| 指标 | 最低要求 |
|------|----------|
| 平均分 | ≥ 3.5/5 |
| 完整性 | ≥ 3.0/5 |
| 准确性 | ≥ 3.0/5 |

### Claude Code 验证门禁（claude-code-test.yml）

- 输出结果必须包含「impact / file / risk / scope」等关键字段
- 输出长度 ≥ 50 字符
- 缺失关键字段 ≤ 2 个

## 4. PR 自动评估

给 PR 添加标签 `needs-evaluation`，自动运行 Agent 评估并评论结果。

## 5. 手动触发

### E2E Test
```
Actions → E2E Test → Run workflow
选择 test_scenario（phone-login / jwt-migration 等）
```

### Agent Evaluation
```
Actions → Agent Evaluation → Run workflow
选择要评估的 Agent

评估使用 LongCat API（不是 Claude Code），无需 Anthropic API Key
```

### Claude Code Integration
```
Actions → Claude Code Integration → Run workflow
直接运行完整测试套件（需要 ANTHROPIC_API_KEY）
```
