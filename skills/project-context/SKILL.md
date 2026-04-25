---
name: project-context
description: 项目感知
model: sonnet
color: cyan
---

# Project Context

## 工作流
项目目录 → 扫描关键文件 → 上下文报告

## 关键原则（参考，非强制）
- 扫描关键配置文件（package.json, go.mod, tsconfig.json）
- 了解目录结构
- 提取代码风格

## 示例

### 输入
```
/project-context
```

### 输出
```markdown
# 项目上下文

## 技术栈
- 前端: React 18 + TypeScript + antd
- 后端: Go 1.21 + Gin

## 目录结构
src/
├── api/
├── components/
└── pages/

## 代码风格
- 组件: PascalCase
- API: RESTful
```