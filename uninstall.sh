#!/bin/bash

# =============================================================================
# AI Native Pipeline - Harness Engine 卸载脚本
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PLUGIN_NAME="ai-native-pipeline"

echo -e "${YELLOW}"
echo "═══════════════════════════════════════════════════════════════"
echo "        AI Native Pipeline - 卸载程序"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# 检测操作系统
case "$(uname -s)" in
    Darwin*)    CLAUDE_DIR="$HOME/.claude" ;;
    Linux*)     CLAUDE_DIR="$HOME/.claude" ;;
    CYGWIN*|MINGW*|MSYS*)    CLAUDE_DIR="$USERPROFILE/.claude" ;;
    *)          CLAUDE_DIR="$HOME/.claude" ;;
esac

echo -e "${BLUE}Claude 配置目录: $CLAUDE_DIR${NC}"
echo ""

# 确认卸载
read -p "确定要卸载 ai-native-pipeline 吗？(y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消卸载${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}正在卸载...${NC}"

# 删除 skills
echo -e "${YELLOW}删除 Skills...${NC}"
rm -rf "$CLAUDE_DIR/skills/pipeline" 2>/dev/null && echo "  ✓ pipeline" || echo "  - pipeline (未安装)"
rm -rf "$CLAUDE_DIR/skills/task-breakdown" 2>/dev/null && echo "  ✓ task-breakdown" || echo "  - task-breakdown (未安装)"
rm -rf "$CLAUDE_DIR/skills/code-review" 2>/dev/null && echo "  ✓ code-review" || echo "  - code-review (未安装)"
rm -rf "$CLAUDE_DIR/skills/test-generator" 2>/dev/null && echo "  ✓ test-generator" || echo "  - test-generator (未安装)"

# 删除 agents
echo -e "${YELLOW}删除 Agents...${NC}"
rm -f "$CLAUDE_DIR/agents/impact-analyzer.md" 2>/dev/null && echo "  ✓ impact-analyzer.md" || echo "  - impact-analyzer.md (未安装)"
rm -f "$CLAUDE_DIR/agents/prd-agent.md" 2>/dev/null && echo "  ✓ prd-agent.md" || echo "  - prd-agent.md (未安装)"
rm -f "$CLAUDE_DIR/agents/spec-agent.md" 2>/dev/null && echo "  ✓ spec-agent.md" || echo "  - spec-agent.md (未安装)"
rm -f "$CLAUDE_DIR/agents/coding-agent.md" 2>/dev/null && echo "  ✓ coding-agent.md" || echo "  - coding-agent.md (未安装)"
rm -f "$CLAUDE_DIR/agents/verification-agent.md" 2>/dev/null && echo "  ✓ verification-agent.md" || echo "  - verification-agent.md (未安装)"

# 删除 rules
echo -e "${YELLOW}删除 Rules...${NC}"
rm -f "$CLAUDE_DIR/rules/task-spec-template.md" 2>/dev/null && echo "  ✓ task-spec-template.md" || echo "  - task-spec-template.md (未安装)"
rm -f "$CLAUDE_DIR/rules/api-spec-rules.md" 2>/dev/null && echo "  ✓ api-spec-rules.md" || echo "  - api-spec-rules.md (未安装)"
rm -f "$CLAUDE_DIR/rules/acceptance-criteria-rules.md" 2>/dev/null && echo "  ✓ acceptance-criteria-rules.md" || echo "  - acceptance-criteria-rules.md (未安装)"
rm -f "$CLAUDE_DIR/rules/frontend-coding-standards.md" 2>/dev/null && echo "  ✓ frontend-coding-standards.md" || echo "  - frontend-coding-standards.md (未安装)"
rm -f "$CLAUDE_DIR/rules/backend-coding-standards.md" 2>/dev/null && echo "  ✓ backend-coding-standards.md" || echo "  - backend-coding-standards.md (未安装)"
rm -f "$CLAUDE_DIR/rules/tdd-pattern.md" 2>/dev/null && echo "  ✓ tdd-pattern.md" || echo "  - tdd-pattern.md (未安装)"
rm -f "$CLAUDE_DIR/rules/user-story-template.md" 2>/dev/null && echo "  ✓ user-story-template.md" || echo "  - user-story-template.md (未安装)"
rm -f "$CLAUDE_DIR/rules/non-functional-requirements.md" 2>/dev/null && echo "  ✓ non-functional-requirements.md" || echo "  - non-functional-requirements.md (未安装)"

# 删除数据目录
echo -e "${YELLOW}删除数据目录...${NC}"
rm -rf "$CLAUDE_DIR/plugins/data/$PLUGIN_NAME" 2>/dev/null && echo "  ✓ 插件数据目录" || echo "  - 插件数据目录 (不存在)"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  卸载完成！${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
