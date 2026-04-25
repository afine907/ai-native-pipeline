# AI Native Pipeline

Claude Code 插件 - 自动化AI Native开发全流程

## 功能简介

这是一个AI Native开发流程自动化插件，包含3个核心Agent和4个Skills，完整覆盖需求到代码的开发链路。

## 包含组件

### Agents (3个核心Agent)

| Agent | 功能 | 使用方式 |
|-------|------|----------|
| `prd-agent` | 需求分析 - 生成结构化PRD | `/prd-agent [需求描述]` |
| `spec-agent` | 技术规格 - PRD转技术规格说明书 | `/spec-agent [PRD内容]` |
| `coding-agent` | 代码生成 - 根据技术规格生成代码 | `/coding-agent [规格描述]` |

### Skills (4个可复用技能)

| Skill | 功能 | 使用方式 |
|-------|------|----------|
| `pipeline` | 主流程编排 - 一键调用3个Agent | `/pipeline [需求描述]` |
| `task-breakdown` | 任务拆解 - SPEC转执行计划 | `/task-breakdown [规格描述]` |
| `code-review` | 代码审查 - 检查代码质量 | `/code-review [代码路径]` |
| `test-generator` | 测试生成 - 单元测试/E2E测试 | `/test-generator [代码路径]` |

## 安装方式

### 方式一：克隆到本地插件目录

```bash
# 克隆仓库
git clone https://github.com/your-repo/ai-native-pipeline.git

# 复制到 Claude Code 插件目录
# Windows
copy -r ai-native-pipeline %APPDATA%\\Claude\\plugins\\ai-native-pipeline

# macOS / Linux
cp -r ai-native-pipeline ~/.claude/plugins/ai-native-pipeline
```

### 方式二：手动放置

1. 找到 Claude Code 的插件目录：
   - Windows: `%APPDATA%\Claude\plugins\`
   - macOS: `~/.claude/plugins/`
   - Linux: `~/.claude/plugins/`

2. 将 `ai-native-pipeline` 文件夹复制到上述目录

3. 重启 Claude Code 或 reload 插件

### 方式三：从市场安装

Claude Code 插件市场开放后，可直接在市场中搜索 "ai-native-pipeline" 一键安装。

## 使用方法

### 方式一：一键全流程

```bash
/pipeline 用户需要一个小程序，可以展示商品列表并下单
```

完整流程：`需求分析 → 技术规格 → 代码生成`

### 方式二：单步使用

```bash
# 1. 需求分析
/prd-agent 用户需要一个登录功能

# 2. 技术规格（需要先有PRD）
/spec-agent PRD内容...

# 3. 代码生成（需要先有技术规格）
/coding-agent 技术规格描述...
```

### 方式三：扩展能力

完成核心流程后，可根据需要调用扩展技能：

```bash
# 任务拆解与编排
/task-breakdown

# 代码审查
/code-review src/main.ts

# 测试生成
/test-generator src/main.ts
```

## 工作流程

```
用户需求
    ↓
 PRD Agent (需求分析)
    ↓
SPEC Agent (技术规格)
    ↓
Coding Agent (代码生成)
    ↓
   完成 ✅

# 可选扩展
   ↓
task-breakdown (任务拆解)
code-review (代码审查)
test-generator (测试生成)
```

## 项目结构

```
ai-native-pipeline/
├── agents/                    # 3个核心Agent
│   ├── prd-agent.md           # 需求分析
│   ├── spec-agent.md          # 技术规格
│   └── coding-agent.md        # 代码生成
├── skills/                    # 4个Skills
│   ├── pipeline/              # 主流程编排
│   ├── task-breakdown/        # 任务拆解
│   ├── code-review/           # 代码审查
│   └── test-generator/        # 测试生成
├── rules/                     # 规范文档
│   ├── api-spec-rules.md
│   ├── acceptance-criteria-rules.md
│   ├── frontend-coding-standards.md
│   └── backend-coding-standards.md
├── .claude-plugin/
│   └── plugin.json
└── CLAUDE.md
```

## 适用场景

- 快速原型开发
- 需求到代码一键落地
- 学习AI Agent开发
- 项目代码自动化生成

## 技术栈

- 纯提示词工程，无需额外依赖
- 支持多语言代码生成（React/TypeScript + Golang）
- 遵循现有项目代码规范

## 注意事项

1. 首次生成需要较多token，后续会更快
2. 代码生成后建议使用 `/code-review` 进行审查
3. 测试用例需要根据实际情况调整
4. 建议在测试项目中使用，验证后再应用到生产

## License

MIT