---
name: pipeline
description: AI Native开发全流程 - 从需求到测试一键完成，自动化调用5个Agent完成PRD、任务拆解、代码生成、代码审查、单元测试
model: sonnet
color: purple
---

# AI Native Pipeline

一键执行完整的AI Native开发流程：需求 → 设计 → 编码 → 审查 → 测试

## 使用方式

```bash
/pipeline [功能描述]
```

## 工作流程

这个Skill会按顺序调用5个Agent完成整个开发流程：

```
用户需求 → PRD Agent → Task Agent → Coding Agent → Review Agent → Test Agent → 完成
```

### 第一步：PRD生成 (PRD Agent)

调用 `prd-agent` 生成结构化需求文档。

**输入**: 用户描述的功能需求
**输出**: 完整的PRD文档

### 第二步：任务拆解 (Task Agent)

调用 `task-agent` 将PRD拆解为可执行的技术任务。

**输入**: PRD文档
**输出**: 任务列表

### 第三步：代码生成 (Coding Agent)

调用 `coding-agent` 根据任务列表生成代码。

**输入**: 任务描述和验收标准
**输出**: 完整的代码实现

### 第四步：代码审查 (Review Agent)

调用 `review-agent` 对生成的代码进行审查。

**输入**: 生成的代码
**输出**: 审查报告和改进建议

### 第五步：测试生成 (Test Agent)

调用 `test-agent` 为代码生成单元测试和E2E测试。

**输入**: 代码实现
**输出**: 测试文件

## 执行模式

### 全流程模式
```
/pipeline 用户需要一个小程序，可以展示商品列表并下单
```
自动执行全部5个步骤。

### 单步模式
也可以单独调用某个Agent：
```
/prd-agent 用户需要...
/task-agent PRD内容...
/coding-agent 任务描述...
/review-agent 代码路径...
/test-agent 代码路径...
```

## 输出示例

执行完成后，会输出：

```markdown
# 开发流程完成 ✅

## 流程回顾
- [x] PRD生成 - 完成
- [x] 任务拆解 - 完成  
- [x] 代码生成 - 完成
- [x] 代码审查 - 完成
- [x] 测试生成 - 完成

## 产出物
- PRD文档: [链接]
- 任务列表: [链接]
- 代码文件: [列表]
- 测试文件: [列表]

## 下一步
[建议的后续操作]
```

## 注意事项

- 首次使用会较慢，后续调用会更快
- 某些步骤可能需要用户确认
- 如果某一步失败，会停止并提示用户