---
paths: ".harness/tasks/*.md, **/task-*.md"
---

# 任务规格模板

本文档定义任务规格的标准格式，确保任务描述清晰、无歧义。

---

## 为什么需要标准化任务规格

模糊的任务描述是 AI Agent 出错的主要原因：
- Agent 做了不需要做的事
- Agent 没做需要做的事
- Agent 假设了错误的实现方式

**解决**: 标准化的任务规格模板，明确边界和期望。

---

## 任务规格模板

```markdown
# Task: [任务名称]

## Summary
[一句话描述任务目标]

## Scope

### Files to Modify
可修改的文件列表：

- `path/to/file1.py` - 修改说明
- `path/to/file2.py` - 修改说明

### Files to Read (不修改)
需要参考但不可修改的文件：

- `path/to/pattern.py` - 参考模式

### Boundary (不可触碰)
绝对不可修改的区域：

- `src/other_module/` - 与本任务无关
- `migrations/` - 数据库迁移文件
- `third_party/` - 第三方代码

## Pattern to Follow
可参考的现有实现：

- **JWT 实现**: `src/api_keys/jwt_util.py` - 使用 PyJWT 库
- **中间件模式**: `src/auth/middleware.py` - 认证中间件结构

## Acceptance Criteria
验证标准（执行 verification-agent）：

- [ ] `pytest tests/auth/ -v` 全部通过
- [ ] `ruff check src/auth/` 无错误
- [ ] `grep "Session" src/auth/` 无匹配
- [ ] `docs/auth-architecture.md` 已更新

## Out of Scope
明确不在本次任务范围的内容：

- Refresh token rotation（单独 ticket）
- 前端改动
- 管理员认证

## Assumptions
已做的假设（如有变化需重新评估）：

- 使用 PyJWT 库（项目已有）
- Token 有效期 2 小时
- 使用 HS256 算法

## Notes
其他注意事项：

- 需要考虑向后兼容
- 周五前完成
- 有安全问题需及时上报
```

---

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| Summary | ✅ | 一句话描述目标 |
| Files to Modify | ✅ | 可修改的文件列表 |
| Files to Read | ⭕ | 需参考的文件 |
| Boundary | ✅ | 不可触碰的区域 |
| Pattern to Follow | ⭕ | 可参考的现有实现 |
| Acceptance Criteria | ✅ | 验证标准 |
| Out of Scope | ⭕ | 明确不在范围的内容 |
| Assumptions | ⭕ | 已做的假设 |
| Notes | ⭕ | 其他注意事项 |

---

## 示例：完整的任务规格

```markdown
# Task: JWT Migration for Auth Module

## Summary
将登录认证从 session-based 迁移到 JWT-based

## Scope

### Files to Modify
- `src/auth/session.py` → 重命名为 `jwt_manager.py`，SessionManager 改为 JWTManager
- `src/auth/middleware.py` → authenticate() 改为 JWT 验证
- `src/auth/models.py` → 添加 token 相关字段

### Files to Read (不修改)
- `src/api_keys/jwt_util.py` - 参考 JWT 编解码实现

### Boundary (不可触碰)
- `src/payments/` - 使用独立的认证流程
- `src/admin/auth.py` - 管理员认证，本次不涉及
- `migrations/` - 数据库迁移需单独处理

## Pattern to Follow
- **JWT 实现**: `src/api_keys/jwt_util.py` - 使用 PyJWT 2.x + HS256
- **中间件模式**: `src/auth/middleware.py` - 保持中间件接口不变

## Acceptance Criteria
- [ ] `pytest tests/auth/ -v` 全部通过（23 个测试）
- [ ] `ruff check src/auth/` 无错误
- [ ] `grep "Session" src/auth/` 无匹配（除注释外）
- [ ] `grep "JWT_SECRET" src/auth/` 有匹配（从环境变量读取）
- [ ] `docs/auth-architecture.md` 包含 "JWT" 关键字

## Out of Scope
- Refresh token rotation（#123 单独处理）
- 前端 token 存储改动
- OAuth 第三方登录

## Assumptions
- 使用 PyJWT 库（已在 requirements.txt）
- Token 有效期 2 小时（可配置）
- 使用 HS256 算法（与 api_keys 一致）

## Notes
- authenticate() 被 12 个路由调用，签名变更需全量更新
- 测试覆盖率要求 ≥80%
- 有 3 个 open issues 涉及 auth 模块，需关注
```

---

## 与 Agent 的配合

### impact-analyzer
任务开始前，impact-analyzer 会自动分析并填充：
- Files to Modify
- Files to Read
- Boundary
- Pattern to Follow

### verification-agent
任务完成后，verification-agent 会自动验证：
- Acceptance Criteria 中的每一项

### Pipeline 流程
```
用户描述 → impact-analyzer → 生成任务规格 → 用户确认 → coding-agent → verification-agent
```

---

## 检查清单

编写任务规格时，必须检查：

- [ ] Summary 清晰，一句话能说清目标
- [ ] Files to Modify 列表完整
- [ ] Boundary 明确，防止越界修改
- [ ] Acceptance Criteria 可验证（有明确的命令或条件）
- [ ] Out of Scope 清晰，防止需求蔓延
- [ ] Assumptions 列出所有假设
