# AI Native Pipeline - 安装指南

## 安装模式

| 模式 | 安装位置 | 适用场景 | Git 共享 |
|------|----------|----------|----------|
| **全局安装** | `~/.claude/` | 个人使用，所有项目可用 | ❌ 不可共享 |
| **项目级安装** | `./.claude/` | 团队协作，统一工作流 | ✅ 可共享 |

---

## 快速安装

### 全局安装（推荐个人使用）

```bash
# 克隆项目
git clone https://github.com/afine907/ai-native-pipeline.git
cd ai-native-pipeline

# 安装
chmod +x install.sh
./install.sh

# 或明确指定全局安装
./install.sh --global
```

**安装位置**：
```
~/.claude/
├── skills/
│   ├── pipeline/
│   ├── task-breakdown/
│   ├── code-review/
│   └── test-generator/
├── agents/
│   ├── impact-analyzer.md
│   ├── prd-agent.md
│   ├── spec-agent.md
│   ├── coding-agent.md
│   └── verification-agent.md
└── rules/
    └── ... (8 个规范文件)
```

**特点**：
- ✅ 所有项目都可使用
- ✅ 个人配置，独立管理
- ❌ 不可通过 git 共享给团队

---

### 项目级安装（推荐团队使用）

```bash
# 在项目根目录执行
cd /path/to/your-project

# 下载并安装（假设已有 install.sh）
/path/to/ai-native-pipeline/install.sh --project

# 或从内网服务器安装
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash -s -- --project
```

**安装位置**：
```
your-project/
└── .claude/
    ├── skills/
    ├── agents/
    └── rules/
```

**特点**：
- ✅ 仅当前项目可用
- ✅ 可通过 git 共享给团队
- ✅ 团队成员 clone 后自动获得相同工作流
- ✅ 与项目代码版本同步

**推荐做法**：
```bash
# 安装后提交到 git
git add .claude/
git commit -m "chore: add ai-native-pipeline for team"

# 团队成员 pull 后立即可用
git pull
```

---

## 内网服务器部署

### 1. 部署到内网 Web 服务器

```bash
# 复制到 Web 目录
cp -r ai-native-pipeline /var/www/html/

# Nginx 配置示例
cat > /etc/nginx/conf.d/ai-native-pipeline.conf << 'EOF'
server {
    listen 80;
    server_name your-server;
    
    location /ai-native-pipeline/ {
        alias /var/www/html/ai-native-pipeline/;
        autoindex on;
    }
}
EOF

# 重启 Nginx
nginx -s reload
```

### 2. 告知同事安装命令

**全局安装**：
```bash
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash
```

**项目级安装**：
```bash
curl -fsSL http://your-server/ai-native-pipeline/install.sh | bash -s -- --project
```

---

## 安装脚本完整用法

```bash
Usage: ./install.sh [选项]

选项:
  -g, --global      全局安装 (默认) - 安装到 ~/.claude/
                    所有项目都可使用

  -p, --project     项目级安装 - 安装到当前目录 .claude/
                    仅当前项目可用，可通过 git 共享给团队

  -u, --uninstall   卸载已安装的组件

  -h, --help        显示帮助信息
  -v, --version     显示版本信息

示例:
  ./install.sh                    # 全局安装
  ./install.sh --global           # 全局安装
  ./install.sh --project          # 项目级安装
  ./install.sh --uninstall        # 卸载全局安装
```

---

## 卸载

```bash
# 卸载全局安装
./install.sh --uninstall

# 或运行卸载脚本
./uninstall.sh
```

---

## 验证安装

### 检查全局安装

```bash
ls ~/.claude/skills/
# 应该看到: pipeline/  task-breakdown/  code-review/  test-generator/

ls ~/.claude/agents/
# 应该看到: impact-analyzer.md  prd-agent.md  spec-agent.md  coding-agent.md  verification-agent.md

ls ~/.claude/rules/
# 应该看到 8 个 .md 文件
```

### 检查项目级安装

```bash
ls ./.claude/skills/
ls ./.claude/agents/
ls ./.claude/rules/
```

### 在 Claude Code 中验证

重启 Claude Code 后：

```bash
# 测试 pipeline skill
/pipeline 用户需要一个登录功能

# 测试 agent
/impact-analyzer 分析用户模块
```

---

## 常见问题

### Q: 全局安装和项目级安装可以同时存在吗？

A: 可以。项目级安装会覆盖全局安装的同名组件。Claude Code 会优先加载项目级的组件。

### Q: 如何更新？

A: 重新运行安装脚本即可覆盖更新：
```bash
./install.sh --global   # 更新全局
./install.sh --project  # 更新项目级
```

### Q: 团队成员如何使用项目级安装？

A: 项目级安装会提交到 git，团队成员 pull 后自动可用。无需单独安装。

### Q: 如何切换安装模式？

A: 直接运行另一种模式的安装命令即可。例如从全局切换到项目级：
```bash
./install.sh --project
```

### Q: 安装后不生效？

A: 请重启 Claude Code，或执行 `/reload-plugins`（如果支持）。

---

## 目录结构对比

### 全局安装

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
├── agents/
│   ├── impact-analyzer.md
│   ├── prd-agent.md
│   ├── spec-agent.md
│   ├── coding-agent.md
│   └── verification-agent.md
└── rules/
    ├── task-spec-template.md
    ├── api-spec-rules.md
    ├── acceptance-criteria-rules.md
    ├── frontend-coding-standards.md
    ├── backend-coding-standards.md
    ├── tdd-pattern.md
    ├── user-story-template.md
    └── non-functional-requirements.md
```

### 项目级安装

```
your-project/
├── .claude/
│   ├── skills/
│   ├── agents/
│   └── rules/
├── src/
├── tests/
└── ... (其他项目文件)
```

---

## 使用方法

安装完成后，在 Claude Code 中使用：

```bash
# 一键全流程
/pipeline 在现有登录模块基础上，增加 JWT 认证

# 分步使用
/impact-analyzer    # 代码影响分析
/prd-agent          # 需求分析
/spec-agent         # 技术规格
/coding-agent       # 代码生成
/verification-agent # 验收验证
/task-breakdown     # 任务拆解
```
