# AI Native Pipeline

[![CI](https://github.com/afine907/ai-native-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/afine907/ai-native-pipeline/actions/workflows/ci.yml)
[![Agent Evaluation](https://github.com/afine907/ai-native-pipeline/actions/workflows/evaluate.yml/badge.svg)](https://github.com/afine907/ai-native-pipeline/actions/workflows/evaluate.yml)
[![Claude Code Integration](https://github.com/afine907/ai-native-pipeline/actions/workflows/claude-code-test.yml/badge.svg)](https://github.com/afine907/ai-native-pipeline/actions/workflows/claude-code-test.yml)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.com/claude-code)
[![Harness Engine](https://img.shields.io/badge/Harness-Engine-purple)](https://openai.com/index/harness-engineering/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 从需求到代码，全自动 AI 开发流水线
>
> 基于 Harness Engineering 最佳实践，支持增量开发 & 自动验证

---

## ✨ 特性

### 🎯 Harness Engine 核心能力

| 能力 | 说明 |
|------|------|
| **Impact Map First** | 任务执行前自动分析代码影响范围 |
| **Structured Task Spec** | 标准化任务规格，减少歧义和错误假设 |
| **Planning Gate** | 关键节点人工确认，捕获错误于编码前 |
| **Auto Verification** | 自动运行测试、Lint、类型检查等验收标准 |
| **Task Breakdown** | 复杂任务自动拆解，支持并行/串行执行 |

### 🤖 5 大 AI Agent

| Agent | 职责 |
|-------|------|
| `impact-analyzer` | 代码影响分析，生成 Impact Map |
| `prd-agent` | 需求分析，输出 Task Spec + PRD |
| `spec-agent` | 技术规格设计，API + 数据模型 |
| `coding-agent` | 代码实现，TDD 模式 |
| `verification-agent` | 验收标准验证 |

### 🛠️ 扩展能力

- `task-breakdown` - 复杂任务拆解与编排
- `code-review` - 代码审查
- `test-generator` - 测试生成

---

## 📦 安装

### 推荐方式：使用安装脚本

**全局安装**（所有项目可用）：

```bash
# 克隆或下载项目
git clone https://github.com/afine907/ai-native-pipeline.git
cd ai-native-pipeline

# 全局安装
chmod +x install.sh
./install.sh

# 或简写
./install.sh --global
```

**项目级安装**（仅当前项目，可 git 共享给团队）：

```bash
# 在项目根目录执行
./install.sh --project

# 安装位置: ./.claude/
# 建议提交到 git，团队成员自动获得相同能力
git add .claude/
git commit -m "chore: add ai-native-pipeline"
```

### 安装选项

| 选项 | 说明 |
|------|------|
| `--global` | 全局安装到 `~/.claude/`，所有项目可用 |
| `--project` | 项目级安装到 `./.claude/`，可 git 共享 |
| `--uninstall` | 卸载已安装的组件 |
| `--help` | 显示帮助信息 |

### 内网服务器部署

```bash
# 部署到内网服务器后，同事可一键安装
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash

# 项目级安装
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash -s -- --project
```

### Claude Code 插件市场（外网）

```bash
/plugin install https://github.com/afine907/ai-native-pipeline.git
/reload-plugins
```

### 验证安装

```bash
# 全局安装
ls ~/.claude/skills/     # pipeline/  task-breakdown/  ...
ls ~/.claude/agents/     # impact-analyzer.md  prd-agent.md  ...

# 项目级安装
ls ./.claude/skills/
ls ./.claude/agents/
```

---

## 🚀 快速开始

### 一键全流程

```bash
# 增量开发：在现有项目中添加功能
/pipeline 在现有登录模块基础上，增加 JWT 认证

# 全新项目
/pipeline 用户需要一个待办事项应用，包含增删改查功能
```

### 执行过程

```
[创建] .harness/sessions/session-20260427-120000/

[Step1] impact-analyzer
  → 分析代码影响
  → 写入: 00-impact-map.md
  
  Impact Map:
  - Core Files: src/auth/session.py, src/auth/middleware.py
  - Dependent Files: src/api/routes/*.py (12 callers)
  - Boundary: src/payments/, src/admin/auth.py

[Step2] prd-agent
  → 生成任务规格和 PRD
  → 写入: 01-task-spec.md, 02-prd.md
  
  [PAUSE] 等待用户确认任务规格
  用户输入: [APPROVED]

[Step3] spec-agent
  → 设计技术规格
  → 写入: 03-spec.md

[Step4] coding-agent
  → 实现代码（TDD 模式）
  → 写入: 04-code.md
  
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

---

## 🔄 工作流

### 完整流程

```
用户需求
    │
    ▼
┌─────────────────┐
│ impact-analyzer │ ← 代码影响分析
└────────┬────────┘
         │ 00-impact-map.md
         ▼
┌─────────────────┐
│   prd-agent     │ ← 需求分析
└────────┬────────┘
         │ 01-task-spec.md + 02-prd.md
         │ [PAUSE] Planning Gate
         ▼
┌─────────────────┐
│   spec-agent    │ ← 技术规格
└────────┬────────┘
         │ 03-spec.md
         ▼
┌─────────────────┐
│ 复杂度判断      │
└────────┬────────┘
         │
    ┌────┴────┐
   简单       复杂
    │          │
    ▼          ▼
coding-agent  task-breakdown
    │          │
    │     按阶段执行
    │          │
    ▼          ▼
┌─────────────────┐
│ verification    │ ← 自动验证
│   -agent        │
└────────┬────────┘
         │
         ▼
    完成 ✅
```

### Planning Gate

在关键节点设置人工确认：
- **Step2 后**：确认任务规格（Scope、Acceptance Criteria）
- **Step4 后**：确认代码改动

用户输入：
- `[APPROVED]` - 继续执行
- `[REJECTED: 反馈内容]` - 返回重做

### Task Breakdown 自动触发

当 SPEC 复杂度高时（API > 3 或跨模块或前后端都有），自动触发任务拆解：

```
任务拆解:
| ID | 任务 | 依赖 | 执行 |
|----|------|------|------|
| T1 | 后端 - 登录 API | - | 并行 |
| T2 | 后端 - 验证码 API | - | 并行 |
| T3 | 前端 - 登录页 | - | 并行 |

执行计划:
- 阶段1（并行）: T1, T2, T3
- 阶段2（串行）: T4 → T5
```

---

## 📂 项目结构

```
ai-native-pipeline/
├── agents/                    # 5 个核心 Agent
│   ├── impact-analyzer.md     # 代码影响分析（整合 module-context）
│   ├── prd-agent.md           # 需求分析
│   ├── spec-agent.md          # 技术规格
│   ├── coding-agent.md        # 代码生成
│   └── verification-agent.md  # 验收验证
│
├── skills/                    # 4 个 Skill
│   ├── pipeline/              # 主流程编排
│   ├── task-breakdown/        # 任务拆解
│   ├── code-review/           # 代码审查
│   └── test-generator/        # 测试生成
│
├── rules/                     # 编码规范
│   ├── task-spec-template.md  # 任务规格模板
│   ├── api-spec-rules.md      # API 规范
│   ├── frontend-coding-standards.md
│   ├── backend-coding-standards.md
│   └── ...
│
└── .claude-plugin/
    └── plugin.json
```

---

## 🎯 使用场景

| 场景 | 说明 |
|------|------|
| 🔵 全新项目 | 从 0 开始，快速生成完整功能模块 |
| 🟢 增量开发 | 在现有项目中添加新功能，自动分析影响范围 |
| ⚡ 快速原型 | 几分钟内从想法到可运行代码 |
| 🔄 重构迁移 | 自动分析依赖关系，确保不破坏现有功能 |

---

## 📝 会话文件结构

每次执行会保存完整的会话记录：

```
.harness/sessions/session-{timestamp}/
├── 00-impact-map.md      # 代码影响分析
├── 01-task-spec.md       # 任务规格
├── 02-prd.md             # PRD 文档
├── 03-spec.md            # 技术规格
├── 04-code.md            # 代码实现
├── 05-verification.md    # 验证结果
└── meta.json             # 元数据
```

---

## 🔧 单独使用 Agent

```bash
# 代码影响分析
/impact-analyzer 在用户模块增加手机号登录

# 需求分析
/prd-agent 用户需要一个商品列表页

# 验收验证
/verification-agent

# 任务拆解
/task-breakdown
```

---

## 📊 Agent 评估与 AgentOps

### 评估 Agent 效果

修改 Agent 后，如何验证改进？

```bash
# 运行评估
python scripts/evaluate_agent.py \
  --agent impact-analyzer \
  --test-cases tests/eval/test_cases_impact_analyzer.json

# 查看报告
cat .harness/eval/report_*.json
```

评估维度：
- **准确率** - 输出是否正确
- **完整性** - 是否覆盖所有要求
- **简洁性** - 是否冗余
- **可读性** - 是否易于理解

详细文档: [docs/agent-evaluation.md](docs/agent-evaluation.md)

### AgentOps 监控

```
┌─────────────────────────────────────────┐
│          Agent 监控面板                  │
├─────────────────────────────────────────┤
│  今日执行: 42 次                         │
│  成功率: 90%                            │
│  平均耗时: 45s                          │
│  Token 消耗: 12K/任务                   │
└─────────────────────────────────────────┘
```

AgentOps 能力：
- **监控** - 实时监控 Agent 状态
- **日志** - 完整执行日志
- **告警** - 异常自动告警
- **版本管理** - Agent 版本控制
- **A/B 测试** - 对比不同版本
- **回滚** - 快速回滚到稳定版本

详细文档: [docs/agentops.md](docs/agentops.md)

---

## 🔄 CI/CD

### GitHub Actions 工作流

| 工作流 | 触发条件 | 功能 |
|--------|----------|------|
| **CI** | Push/PR to master | 代码检查、测试、Plugin 验证、Agent 评估 |
| **E2E Test** | 手动触发 / 每天 | 端到端流水线测试 |
| **Agent Evaluation** | 手动触发 / PR label | Agent 效果评估 |
| **Release** | 发布 Release | 构建发布产物 |
| **Security** | 每周一 | 安全检查 |

### 配置 Secret

在 GitHub 仓库设置中添加 Secret：

```
Settings → Secrets and variables → Actions → New repository secret

Name: LONGCAT_API_KEY
Value: ak_xxx（你的 LongCat API Key）
```

### 运行 E2E 测试

1. **手动触发**：
   ```
   Actions → E2E Test → Run workflow → 选择 test_scenario
   ```

2. **自动运行**：
   - 每天凌晨 2 点自动运行
   - 测试所有 Agent 的完整流程

### 质量门禁

Agent 评估结果必须满足：
- **平均分 ≥ 3.5/5**
- **完整性 ≥ 3.0/5**
- **准确性 ≥ 3.0/5**

### PR 自动评估

1. 给 PR 添加标签 `needs-evaluation`
2. 自动运行 Agent 评估
3. 结果评论到 PR

---

## 📖 Harness Engineering 原则

本项目遵循 [Harness Engineering](https://openai.com/index/harness-engineering/) 最佳实践：

1. **Impact Map First** - 先分析代码影响，再开始编码
2. **Structured Task Spec** - 标准化任务规格，减少歧义
3. **Planning Gate** - 关键节点人工确认，捕获错误假设
4. **Auto Verification** - 自动验证验收标准，确保质量
5. **Feedback Loop** - 记录错误，持续改进 Harness

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 License

MIT

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/afine907">afine907</a></sub>
</p>
