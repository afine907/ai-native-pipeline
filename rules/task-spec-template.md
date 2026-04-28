---
paths: ".harness/tasks/*.md, **/task-*.md"
---

# Task Spec 模板（精简版）

> **核心原则**: AI 自动理解上下文，无需人工标注追溯关系

## 模板

```markdown
# Task Spec: [任务名称]

## 1. Impact Map（impact-analyzer）

### 影响范围
| 类型 | 文件 |
|------|------|
| 可修改 | src/auth/session.py, middleware.py |
| 不可触碰 | src/payments/, src/admin/auth.py |

### 风险
- authenticate() 被 12 处调用

---

## 2. Task Spec（prd-agent）

### 功能优先级
| 功能 | 优先级 |
|------|--------|
| JWT Token 生成 | P0 |
| JWT Token 验证 | P0 |

### 验收标准
- [ ] `pytest tests/auth/ -v` 全部通过
- [ ] `grep "Session" src/auth/` 无匹配

---

## 3. Technical Spec（spec-agent）

### API
```
POST /api/auth/login
  Request:  { phone, code }
  Response: { token, user }
```

### 技术选型
| 决策点 | 选择 | 理由 |
|--------|------|------|
| JWT 库 | PyJWT | 项目已有 |
| 算法 | HS256 | 与 api_keys 一致 |

---

## 4. Code（coding-agent）

### 修改文件
- src/auth/jwt_manager.py (新建)
- src/auth/middleware.py (修改)

### 注意事项
- ⚠️ 需要设置环境变量 JWT_SECRET

---

## 5. Verification（verification-agent）

| 检查项 | 状态 |
|--------|------|
| 测试 | ✅ 23 passed |
| Lint | ✅ No issues |
| Session 检查 | ✅ 无匹配 |
```

## 使用方式

- 每个 Agent 追加自己的章节
- 后续 Agent 自动读取前面的内容
- AI 理解上下文，无需人工标注"基于"+"理由"

## 文件命名

```
.harness/sessions/session-{timestamp}/
└── task-spec.md    # 所有内容合并到一个文件
```
