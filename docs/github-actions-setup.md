# GitHub Actions 配置指南

## 1. 配置 LongCat API Key

### 步骤

1. 进入 GitHub 仓库
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 填写：
   - **Name**: `LONGCAT_API_KEY`
   - **Value**: 你的 LongCat API Key（格式：`ak_xxx`）
5. 点击 `Add secret`

### 验证

配置完成后，CI 流水线会自动使用该 Secret 运行 Agent 评估。

## 2. 工作流说明

### CI（自动触发）

每次 push 或 PR 到 master 分支自动运行：

```
jobs:
  lint:          # 代码检查
  test:          # 脚本测试
  plugin-test:   # Plugin 结构验证
  agent-evaluation:  # Agent 效果评估（需要 API Key）
```

### E2E Test（手动/定时）

完整流水线测试：

```
1. 创建测试项目
2. 运行 impact-analyzer
3. 运行 prd-agent
4. 运行 spec-agent
5. 评估所有 Agent
6. 质量门禁检查
```

## 3. 质量门禁

Agent 评估必须满足：

| 指标 | 最低要求 |
|------|----------|
| 平均分 | ≥ 3.5/5 |
| 完整性 | ≥ 3.0/5 |
| 准确性 | ≥ 3.0/5 |

未达标则 CI 失败。

## 4. PR 自动评估

给 PR 添加标签 `needs-evaluation`，自动运行评估并评论结果。

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
```
