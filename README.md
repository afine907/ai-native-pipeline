# AI Native Pipeline

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.com/claude-code)

> 用自然语言描述需求 → 自动输出可运行代码
>
> 支持全新项目开发 & 增量功能扩展

---

## ✨ 特性

- 🤖 **4 大 AI Agent** - 需求分析、技术规格、代码生成、代码审查
- ⚡ **一键全流程** - 从需求到代码全自动
- 🔄 **增量开发** - 自动分析现有模块，生成增量代码
- 🎯 **精准代码生成** - 遵循项目规范，支持 React/TypeScript + Golang
- 🛠️ **可扩展** - 支持代码审查、测试生成等扩展能力

---

## 📦 安装

### 方式一：在线安装（推荐）

```bash
/plugin install https://github.com/afine907/ai-native-pipeline.git
/reload-plugins
```

### 方式二：本地安装

```bash
# 克隆仓库
git clone https://github.com/afine907/ai-native-pipeline.git

# 本地安装
/plugin install ./ai-native-pipeline
/reload-plugins
```

安装完成后，执行 `/plugin` 验证是否出现 `ai-native-pipeline`

---

## 🚀 快速开始

### 方式一：一键全流程（推荐）

```bash
# 全新项目需求
/pipeline 用户需要一个小程序，可以展示商品列表并下单

# 增量需求（在已有项目中添加功能）
/pipeline 在现有登录模块基础上，增加第三方登录（微信、Google）
```

### 方式二：分步使用

```bash
# 第 1 步：需求分析
/prd-agent 用户需要一个登录功能，包含用户名密码和验证码

# 第 2 步：先分析现有模块（增量开发时）
/module-context src/auth/

# 第 3 步：生成技术规格
/spec-agent [粘贴上一步的 PRD 内容]

# 第 4 步：代码生成
/coding-agent [粘贴上一步的技术规格]
```

### 方式三：扩展能力

```bash
/code-review src/main.ts      # 代码审查
/test-generator src/main.ts   # 生成测试
```

---

## 🔄 工作流

```
┌──────────┐    ┌──────────────┐    ┌─────────┐    ┌────────┐    ┌─────────┐
│  用户需求  │───▶│ Module Context │───▶│ PRD Agent│───▶│ SPEC    │───▶│ Coding  │
└──────────┘    └──────────────┘    └─────────┘    └────────┘    └─────────┘
                                                                         │
                                                                         ▼
                                                                      完成 ✅
```

> 💡 **增量开发**：Pipeline 自动先调用 Module Context 分析现有代码结构，再生成符合现有架构的增量代码

---

## 📂 项目结构

```
ai-native-pipeline/
├── agents/                    # 4 个核心 Agent
│   ├── module-context.md      # 模块感知（分析现有代码）
│   ├── prd-agent.md           # 需求分析
│   ├── spec-agent.md          # 技术规格
│   └── coding-agent.md        # 代码生成
├── skills/pipeline/           # 主流程编排 Skill
├── rules/                     # 编码规范
├── .claude-plugin/
│   └── plugin.json            # 插件配置
└── CLAUDE.md                  # 项目说明
```

---

## 🎯 使用场景

| 场景 | 说明 |
|------|------|
| 🔵 全新项目 | 从 0 开始，快速生成完整功能模块 |
| 🟢 增量开发 | 在现有项目中添加新功能，保持代码一致性 |
| ⚡ 快速原型 | 几分钟内从想法到可运行代码 |
| 📚 学习参考 | 学习 AI Agent 的最佳实践 |

---

## 📝 示例输出

**全新项目输入：**
```
/pipeline 用户需要一个待办事项列表，包含增删改查功能
```

**增量需求输入：**
```
/pipeline 在现有用户模块中增加会员等级功能
```

**输出：**
```
✅ Module Context 已分析（现有代码结构）
✅ PRD 已生成（用户故事、验收标准）
✅ 技术规格已生成（API 接口、数据结构）
✅ 代码已生成（组件、接口、数据库）
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 License

MIT

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/afine907">afine907</a></sub>
</p>