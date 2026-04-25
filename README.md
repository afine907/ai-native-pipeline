# AI Native Pipeline

Claude Code 插件 - 自动化AI Native开发全流程

## 功能简介

这是一个AI Native开发流程自动化插件，包含5个独立的Agent和1个主流程编排Skill，完整覆盖需求到测试的开发链路。

## 包含组件

### Agents (5个独立Agent)

| Agent | 功能 | 使用方式 |
|-------|------|----------|
| `prd-agent` | 需求分析 - 生成结构化PRD | `/agents` 选择调用 |
| `task-agent` | 任务拆解 - PRD转技术任务 | `/agents` 选择调用 |
| `coding-agent` | 代码生成 - 根据任务生成代码 | `/agents` 选择调用 |
| `review-agent` | 代码审查 - 代码质量检查 | `/agents` 选择调用 |
| `test-agent` | 测试生成 - 单元测试/E2E测试 | `/agents` 选择调用 |

### Skills (1个主流程)

| Skill | 功能 | 使用方式 |
|-------|------|----------|
| `pipeline` | 全流程编排 - 一键跑通5个Agent | `/pipeline [需求描述]` |

## 安装方式

```bash
# 方式1: 复制到本地插件目录
cp -r ai-native-pipeline ~/.claude/plugins/ai-native-pipeline

# 方式2: 启用本地插件 (在 settings.json 中配置)
```

## 使用方法

### 方式一：一键全流程

```bash
/pipeline 用户需要一个小程序，可以展示商品列表并下单
```

### 方式二：单独使用某个Agent

```bash
# 需求分析
/prd-agent 用户需要...

# 任务拆解
/task-agent [PRD内容]

# 代码生成
/coding-agent [任务描述]

# 代码审查
/review-agent [代码路径或内容]

# 测试生成
/test-agent [代码路径]
```

## 工作流程

```
用户需求
    ↓
 PRD Agent (需求分析)
    ↓
 Task Agent (任务拆解)
    ↓
Coding Agent (代码生成)
    ↓
Review Agent (代码审查)
    ↓
 Test Agent (测试生成)
    ↓
   完成 ✅
```

## 产出物

- **PRD文档**: 结构化的产品需求文档
- **任务列表**: 可执行的技术任务清单
- **代码文件**: 符合项目规范的实现代码
- **测试文件**: 单元测试 + E2E测试

## 示例

### 完整流程示例

```
> /pipeline 我需要一个简单的Todo应用，包含添加、删除、列表展示功能
```

Agent会依次执行：
1. 生成PRD文档（功能列表、用户故事、验收标准）
2. 拆解为具体任务（组件划分、API设计、测试任务）
3. 生成代码（组件、样式、逻辑）
4. 代码审查（问题发现、改进建议）
5. 生成测试（单元测试、E2E测试）

### 单独使用示例

```
> 调用 prd-agent
> 输入: 用户需要一个登录功能，支持手机号和邮箱登录
> 输出: 完整的PRD文档
```

## 配置说明

暂无必需配置项，开箱即用。

## 适用场景

- 快速原型开发
- 需求到代码一键落地
- 学习AI Agent开发
- 项目代码自动化生成

## 技术栈

- 纯提示词工程，无需额外依赖
- 支持多语言代码生成
- 遵循现有项目代码规范

## 注意事项

1. 首次生成需要较多token，后续会更快
2. 代码生成后建议人工review
3. 测试用例需要根据实际情况调整

## License

MIT