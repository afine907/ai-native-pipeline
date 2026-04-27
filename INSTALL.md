# AI Native Pipeline - 内网安装指南

## 快速安装

### 方式一：从本地目录安装

```bash
# 1. 下载或复制项目到本地
# 2. 进入项目目录
cd ai-native-pipeline

# 3. 运行安装脚本
chmod +x install.sh
./install.sh

# 或指定源目录
./install.sh /path/to/ai-native-pipeline
```

### 方式二：从内网服务器安装

```bash
# 如果部署到内网服务器
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash

# 或
wget -qO- http://your-server/ai-native-pipeline/install.sh | bash
```

---

## 验证安装

安装完成后，重启 Claude Code 并验证：

```bash
# 检查 skills 目录
ls ~/.claude/skills/

# 应该看到:
# pipeline/  task-breakdown/  code-review/  test-generator/

# 检查 agents 目录
ls ~/.claude/agents/

# 应该看到:
# impact-analyzer.md  prd-agent.md  spec-agent.md  coding-agent.md  verification-agent.md

# 检查 rules 目录
ls ~/.claude/rules/

# 应该看到 8 个 .md 文件
```

---

## 使用方法

### 一键全流程

```bash
/pipeline 在现有登录模块基础上，增加 JWT 认证
```

### 分步使用

```bash
# 1. 分析代码影响
/impact-analyzer 在用户模块增加手机号登录

# 2. 需求分析
/prd-agent 用户需要一个商品列表页

# 3. 技术规格
/spec-agent

# 4. 代码生成
/coding-agent

# 5. 验收验证
/verification-agent

# 6. 任务拆解（复杂任务）
/task-breakdown
```

---

## 卸载

```bash
# 方式一：运行卸载脚本
./uninstall.sh

# 方式二：使用安装脚本卸载
./install.sh --uninstall
```

---

## 目录结构

安装后的文件位置：

```
~/.claude/
├── skills/
│   ├── pipeline/
│   │   └── SKILL.md
│   ├── task-breakdown/
│   │   └── SKILL.md
│   ├── code-review/
│   │   └── SKILL.md
│   └── test-generator/
│       └── SKILL.md
│
├── agents/
│   ├── impact-analyzer.md
│   ├── prd-agent.md
│   ├── spec-agent.md
│   ├── coding-agent.md
│   └── verification-agent.md
│
├── rules/
│   ├── task-spec-template.md
│   ├── api-spec-rules.md
│   ├── acceptance-criteria-rules.md
│   ├── frontend-coding-standards.md
│   ├── backend-coding-standards.md
│   ├── tdd-pattern.md
│   ├── user-story-template.md
│   └── non-functional-requirements.md
│
└── plugins/
    └── data/
        └── ai-native-pipeline/   # 插件数据目录
```

---

## 工作流

```
用户需求
    │
    ▼
impact-analyzer → prd-agent → spec-agent → coding-agent → verification-agent
    │               │            │              │                │
    │               │            │              │                │
    ▼               ▼            ▼              ▼                ▼
Impact Map    Task Spec + PRD   技术规格       代码实现          验证结果
```

---

## 常见问题

### Q: 安装后不生效？

A: 请重启 Claude Code，或执行 `/reload-plugins`（如果支持）。

### Q: 如何更新？

A: 重新运行 `./install.sh` 即可覆盖更新。

### Q: 如何检查版本？

A: 运行 `./install.sh --version` 查看版本信息。

### Q: 安装到项目而非全局？

A: 修改脚本中的目标目录，从 `~/.claude/` 改为项目内的 `.claude/`。

---

## 内网服务器部署

### 部署步骤

1. 将整个项目复制到内网 Web 服务器

```bash
# 例如部署到 Nginx
cp -r ai-native-pipeline /var/www/html/
```

2. 确保文件可访问

```bash
# 测试访问
curl http://your-server/ai-native-pipeline/install.sh
```

3. 告知同事安装命令

```bash
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-server;
    
    location /ai-native-pipeline/ {
        alias /var/www/html/ai-native-pipeline/;
        index install.sh;
        autoindex on;
    }
}
```

---

## 技术支持

- 项目地址：https://github.com/afine907/ai-native-pipeline
- 问题反馈：提交 GitHub Issue
