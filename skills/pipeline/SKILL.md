---
name: pipeline
description: AI Native开发全流程 - 需求到代码一键完成
model: sonnet
color: purple
---

# AI Native Pipeline

## 工作流

```
project-context → prd-agent → spec-agent → coding-agent
```

## 步骤

1. **project-context**: 感知项目（技术栈、目录结构、代码风格）
2. **prd-agent**: 需求分析，输出PRD
3. **spec-agent**: 技术规格，输出SPEC
4. **coding-agent**: 代码生成，写入文件

## 使用

```
/pipeline [需求描述]
```

## 后续扩展

- `/task-breakdown` - 任务拆解
- `/code-review` - 代码审查
- `/test-generator` - 测试生成