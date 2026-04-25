---
name: pipeline
description: AI Native开发全流程
model: sonnet
color: purple
---

# Pipeline

## 工作流
project-context → prd-agent → spec-agent → coding-agent

## 关键原则（参考，非强制）
- 每一步的输出作为下一步的输入
- 代码生成后写入文件
- 支持后续扩展（task-breakdown, code-review, test-generator）

## 示例

### 输入
```
/pipeline 用户需要一个登录功能
```

### 执行
1. project-context: 扫描项目
2. prd-agent: 生成PRD
3. spec-agent: 生成技术规格
4. coding-agent: 生成代码，写入文件

### 输出
```markdown
# 开发完成 ✅
- PRD: [内容]
- SPEC: [内容]
- 代码: [文件列表]
```

## 后续扩展
- `/task-breakdown` - 任务拆解
- `/code-review` - 代码审查
- `/test-generator` - 测试生成