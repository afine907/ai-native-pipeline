# PRD: AI Native Pipeline - 后续迭代计划

> 当前版本 v1.0 已实现核心 Harness Engine 能力，本文档记录后续迭代方向

---

## v1.0 已完成 ✅

| 功能 | 说明 | 状态 |
|------|------|------|
| impact-analyzer | 代码影响分析，生成 Impact Map | ✅ |
| verification-agent | 验收标准验证（测试/lint/grep） | ✅ |
| task-spec-template | 标准化任务规格模板 | ✅ |
| task-breakdown | 复杂任务自动拆解 | ✅ |
| Planning Gate | 关键节点人工确认 | ✅ |
| install.sh | 一键安装脚本（支持全局/项目级） | ✅ |

---

## v1.1 待实现 - 错误学习闭环

### US-006: Feedback Log（错误学习机制）

**问题**: 重复犯同样错误，无学习改进机制

**解决方案**: 记录错误 → 归因分类 → 生成改进建议

**输出格式**:
```markdown
# Feedback Log

## 错误记录

| 时间 | 任务 | 错误描述 | 分类 | 改进建议 |
|------|------|----------|------|----------|
| 2026-04-27 | JWT迁移 | 使用了 python-jose 而非 PyJWT | pattern缺失 | 在 task-spec 中明确指定库名 |
| 2026-04-27 | 登录模块 | 文件路径错误 | impact不完整 | 增强 impact-analyzer 的依赖分析 |

## 错误分类统计

| 分类 | 次数 | 占比 |
|------|------|------|
| pattern缺失 | 5 | 35% |
| impact不完整 | 3 | 21% |
| 验收标准模糊 | 4 | 29% |
| 其他 | 2 | 15% |

## 改进建议

### 高优先级
1. 在 task-spec-template 中增加 "Pattern to Follow" 的必填提示
2. impact-analyzer 增加传递依赖分析
```

**实现**:
- 新增 `skills/feedback-log/SKILL.md`
- 在 verification 失败时提示记录反馈
- 支持手动记录：`/feedback-log 记录一次错误：xxx`

**工作量**: 1 天

---

## v1.2 待实现 - 系统集成

### US-007: MCP 集成示例

**问题**: 无法获取实时系统状态（CI、部署、日志）

**解决方案**: 通过 MCP 连接外部系统

**集成目标**:

| 系统 | 用途 | 触发场景 |
|------|------|----------|
| GitHub Actions | CI 状态、失败日志 | 调试任务开始前 |
| 部署系统 | 当前版本、部署状态 | 重构任务 |
| 日志系统 | 错误日志、堆栈 | Bug 修复任务 |
| 监控系统 | 性能指标、告警 | 性能优化任务 |

**示例 - CI 状态检查**:
```yaml
# 调试任务开始前自动检查 CI
if task.type == "debug":
  ci_status = mcp.call("github-actions", "get_workflow_run", {branch: current_branch})
  if ci_status.status == "failure":
    logs = mcp.call("github-actions", "get_logs", {run_id: ci_status.id})
    context.add("CI已在失败状态，错误日志：\n" + logs)
```

**工作量**: 2-3 天

---

### US-008: code-review 集成

**当前**: code-review skill 独立存在

**改进**: 集成到 pipeline 流程

```
verification-agent 
    │
    ▼
┌─────────────────┐
│ 结果判断        │
└────────┬────────┘
         │
    ┌────┴────┐
   通过       失败
    │          │
    ▼          ▼
code-review  停止，修复
(可选)
```

**工作量**: 0.5 天

---

## v1.3 待实现 - 体验优化

### US-009: 智能 Planning Gate

**当前**: 所有任务都需人工确认

**改进**: 根据风险等级自动判断

| 风险等级 | 条件 | 处理 |
|----------|------|------|
| 🟢 低 | 影响文件 < 3，非核心模块 | 自动通过 |
| 🟡 中 | 影响文件 3-10 个 | 提示确认 |
| 🔴 高 | 影响文件 > 10 或核心模块 | 必须确认 |

**实现**: 在 prd-agent 输出中增加风险等级评估

**工作量**: 1 天

---

### US-010: 会话断点续传

**当前**: `.harness/sessions/` 保存记录，但无法恢复执行

**改进**: 支持从中断点继续

```bash
# 查看可恢复的会话
/pipeline --list-sessions

# 恢复执行
/pipeline --resume session-20260427-120000
```

**工作量**: 1-2 天

---

## v2.0 待实现 - 生态扩展

### US-011: 更多语言/框架支持

**当前**: rules 主要覆盖 Go + React/TypeScript

**扩展**:

| 语言/框架 | rules 文件 | 优先级 |
|-----------|------------|--------|
| Python (FastAPI) | `python-fastapi-rules.md` | P0 |
| Python (Django) | `python-django-rules.md` | P1 |
| Java (Spring Boot) | `java-spring-rules.md` | P1 |
| Rust | `rust-rules.md` | P2 |
| Vue 3 | `vue-coding-standards.md` | P1 |

**工作量**: 每个语言/框架 0.5-1 天

---

### US-012: 项目模板库

**目标**: 预置常见项目模板，快速启动

**模板示例**:
- `template-fastapi-crud` - FastAPI CRUD 项目
- `template-react-admin` - React 管理后台
- `template-go-microservice` - Go 微服务

**用法**:
```bash
/pipeline --template fastapi-crud 创建一个用户管理API
```

**工作量**: 按需积累

---

## 迭代优先级排序

| 版本 | 功能 | 工作量 | 价值 | 优先级 |
|------|------|--------|------|--------|
| v1.1 | Feedback Log | 1天 | 高 - 形成学习闭环 | 🥇 |
| v1.2 | code-review 集成 | 0.5天 | 中 - 质量保障 | 🥈 |
| v1.2 | MCP 集成示例 | 2-3天 | 高 - 实时上下文 | 🥉 |
| v1.3 | 智能 Planning Gate | 1天 | 中 - 提升效率 | 4 |
| v1.3 | 会话断点续传 | 1-2天 | 低 - 锦上添花 | 5 |
| v2.0 | 更多语言支持 | 按需 | 中 - 扩展场景 | 6 |

---

## 下一步行动

**推荐先做**: Feedback Log（工作量小，价值高）

要开始实现吗？
