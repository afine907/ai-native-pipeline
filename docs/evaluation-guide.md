# Agent 评估实战指南

## 快速开始（5 分钟）

```bash
# 步骤 1: 生成测试任务
python scripts/evaluate_interactive.py --generate-tasks

# 步骤 2: 运行 Agent 并记录输出
python scripts/evaluate_interactive.py --run-agent impact-analyzer --task 1

# 步骤 3: 评估输出（手动评分）
python scripts/evaluate_interactive.py --evaluate impact-analyzer

# 步骤 4: 查看报告
python scripts/evaluate_interactive.py --report impact-analyzer
```

---

## 方法 1: 手动评估（推荐入门）

### 步骤详解

#### 1. 生成测试任务

```bash
python scripts/evaluate_interactive.py --generate-tasks
```

输出：
```
✅ 已生成 5 个测试任务
   保存位置: .harness/eval/tasks.json
```

#### 2. 运行 Agent

```bash
python scripts/evaluate_interactive.py --run-agent impact-analyzer --task 1
```

你会看到：
```
============================================================
任务 1: 在用户模块增加手机号登录功能
============================================================

请在 Claude Code 中运行以下命令：

  /impact-analyzer 在用户模块增加手机号登录功能

Agent 输出完成后，请粘贴输出内容（输入空行结束）：
```

然后在 Claude Code 中运行命令，复制输出粘贴回来。

#### 3. 评估输出

```bash
python scripts/evaluate_interactive.py --evaluate impact-analyzer
```

系统会引导你打分：
```
任务 1: 在用户模块增加手机号登录功能
============================================================
输出行数: 25
输出预览: ## Impact Map: 手机号登录...

请评分 (1-5):
  完整性: 4
  准确性: 5
  简洁性: 4
  可读性: 5

平均分: 4.50/5
```

#### 4. 查看报告

```bash
python scripts/evaluate_interactive.py --report impact-analyzer
```

输出：
```
============================================================
Agent 评估报告: impact-analyzer
============================================================
评估日期: 2026-04-28T09:40:00
任务数量: 5
平均分数: 4.2/5

详细结果:
------------------------------------------------------------
任务 1: 在用户模块增加手机号登录功能
  完整性: 4/5
  准确性: 5/5
  简洁性: 4/5
  可读性: 5/5
  平均分: 4.5/5
...
```

---

## 方法 2: LLM 自动评估（推荐进阶）

### 前提条件

- 已有 LongCat API Key（或其他 OpenAI 兼容 API）
- 已运行 Agent 并保存输出

### 运行评估

```bash
export LONGCAT_API_KEY="ak_xxx"

python scripts/evaluate_llm_judge.py \
  --agent impact-analyzer \
  --api-key $LONGCAT_API_KEY
```

输出：
```
使用 LLM 自动评估 impact-analyzer...
找到 5 个输出文件

[1/5] 评估任务 1: 在用户模块增加手机号登录功能...
  完整性: 4/5
  准确性: 5/5
  简洁性: 4/5
  可读性: 5/5
  平均分: 4.50/5
  理由: 输出完整识别了核心文件和边界...

============================================================
✅ 评估完成
   平均分数: 4.20/5
   结果保存: .harness/eval/reports/impact-analyzer_llm_20260428_094000.json
```

---

## 对比版本效果

修改 Agent 后，重新运行评估并对比：

```bash
# 修改前评估
python scripts/evaluate_interactive.py --evaluate impact-analyzer

# 修改 Agent 文件
# ...

# 修改后评估
python scripts/evaluate_interactive.py --evaluate impact-analyzer

# 对比结果
python scripts/evaluate_interactive.py --compare impact-analyzer
```

输出：
```
版本对比:
============================================================
版本 1: 2026-04-27 - 平均分 3.8/5
版本 2: 2026-04-28 - 平均分 4.2/5

✅ 改进: +0.40
```

---

## 评估指标解读

### 分数含义

| 分数 | 含义 |
|------|------|
| 5 | 优秀 - 完全符合预期，无需改进 |
| 4 | 良好 - 基本符合预期，有小问题 |
| 3 | 及格 - 勉强可用，有明显问题 |
| 2 | 较差 - 问题很多，需要大改 |
| 1 | 很差 - 完全不可用 |

### 质量目标

| 指标 | 目标 | 说明 |
|------|------|------|
| 完整性 | > 4.0 | 不能遗漏重要信息 |
| 准确性 | > 4.0 | 信息必须正确 |
| 简洁性 | > 3.5 | 适度简洁，不冗余 |
| 可读性 | > 4.0 | 必须易于理解 |
| **平均分** | **> 4.0** | **整体质量达标** |

---

## 评估文件结构

```
.harness/eval/
├── tasks.json                      # 测试任务
├── outputs/                        # Agent 输出
│   └── impact-analyzer/
│       ├── task_1.md
│       ├── task_2.md
│       └── ...
└── reports/                        # 评估报告
    ├── impact-analyzer_20260427_100000.json
    ├── impact-analyzer_20260428_100000.json
    └── impact-analyzer_report.md
```

---

## 最佳实践

### 1. 测试集设计

测试集应该覆盖：
- **正常场景** - 典型任务（60%）
- **边界场景** - 全新模块、空输入（20%）
- **困难场景** - 复杂任务（20%）

### 2. 评估频率

- **修改 Agent 后** - 立即评估
- **每周** - 定期评估，跟踪趋势
- **发布前** - 必须评估通过

### 3. 评估团队

- **开发者** - 自评（快速迭代）
- **团队成员** - 交叉评估（客观）
- **用户** - 真实反馈（最终验证）

---

## 常见问题

### Q: 评估结果波动大怎么办？

A: 增加测试用例数量。建议至少 10 个，最好 20+。

### Q: LLM 评估不稳定怎么办？

A: 降低 temperature（默认 0.3），使用更稳定的模型。

### Q: 手动评估太慢怎么办？

A: 先用 LLM 评估筛选，只对低分输出手动复核。

### Q: 如何评估多个 Agent？

A: 对每个 Agent 单独运行评估，然后对比报告。
