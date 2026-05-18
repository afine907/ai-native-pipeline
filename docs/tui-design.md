# T3-1 TUI 界面设计

## 目标
基于 Textual 实现交互式终端 UI，支持命令补全、进度展示、Agent 状态可视化。

## 界面布局

```
┌─────────────────────────────────────────────────────────┐
│  🤖 AI Native Pipeline                    [状态指示器]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────────────────────────┐  │
│  │   Agent     │  │        Main Panel               │  │
│  │   Panel     │  │                                 │  │
│  │             │  │  - 对话区域                     │  │
│  │  • impact   │  │  - Agent 输出                   │  │
│  │  • prd      │  │  - 进度条                       │  │
│  │  • spec     │  │  - 代码块展示                   │  │
│  │  • coding   │  │                                 │  │
│  │  • verify   │  │                                 │  │
│  │             │  │                                 │  │
│  └─────────────┘  └─────────────────────────────────┘  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ > _                                                     │
│ [命令补全建议]                                          │
└─────────────────────────────────────────────────────────┘
```

## 核心功能

| 功能 | 说明 |
|------|------|
| **Agent 面板** | 显示 5 个 Agent 状态（等待/运行/完成/错误） |
| **主面板** | 对话记录 + Agent 输出 + 进度条 |
| **命令输入** | 支持 Tab 补全、命令历史 |
| **进度展示** | 每个 Agent 执行时的进度条 |
| **代码高亮** | 输出代码块语法高亮 |

## 命令补全

| 命令 | 说明 |
|------|------|
| `/pipeline` | 完整流水线 |
| `/impact` | 影响分析 |
| `/prd` | 需求分析 |
| `/spec` | 技术规格 |
| `/coding` | 代码生成 |
| `/verify` | 验收验证 |
| `/breakdown` | 任务拆解 |
| `/review` | 代码审查 |
| `/test` | 测试生成 |
| `/clear` | 清除屏幕 |
| `/help` | 帮助信息 |

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 取消当前任务 |
| `Ctrl+L` | 清除屏幕 |
| `Tab` | 命令补全 |
| `↑/↓` | 命令历史 |
| `Ctrl+Q` | 退出 |

## 实现计划

1. **基础框架** - Textual App + 布局 ✅
2. **Agent 面板** - 状态显示 ✅
3. **主面板** - 输出区域 ✅
4. **命令输入** - 补全 + 历史 ✅
5. **进度条** - Agent 执行进度 ✅ (模拟)

## 文件结构

```
tui/
├── __init__.py       # 版本信息
├── app.py            # 主应用 (Textual)
└── cli.py            # CLI 入口
```

## 使用方式

```bash
# 激活虚拟环境
source ~/.venv/ai-pipeline/bin/activate

# 启动 TUI
python -m tui.cli
# 或
python tui/cli.py
```

## 已实现功能

- ✅ 5 个 Agent 状态面板
- ✅ 4 个 Skill 面板
- ✅ 主输出区域 (Log 组件)
- ✅ 命令输入 + 历史记录
- ✅ Tab 补全支持
- ✅ 快捷键 (Ctrl+C/L/Q, F1)
- ✅ 完整流水线模拟
- ✅ 单个 Agent 执行模拟
- ✅ Skill 调用 (breakdown/review/test)

---

# T3-2 Skills 增强

## B. Agent 转 Skills ✅

| 原 Agent | 新 Skill 位置 |
|----------|---------------|
| impact-analyzer | `skills/impact-analyzer/SKILL.md` |
| prd-agent | `skills/prd-agent/SKILL.md` |
| spec-agent | `skills/spec-agent/SKILL.md` |
| coding-agent | `skills/coding-agent/SKILL.md` |
| verification-agent | `skills/verification-agent/SKILL.md` |

## C. TUI 集成 Skills ✅

TUI 新增命令：
- `/skills` - 列出所有 skills
- `/breakdown` - 调用 task-breakdown
- `/review` - 调用 code-review
- `/test` - 调用 test-generator