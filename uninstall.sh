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
UNINSTALL_MODE="global"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos" ;;
        Linux*)     echo "linux" ;;
        CYGWIN*|MINGW*|MSYS*)    echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

# 获取全局目录
get_global_dir() {
    local os=$(detect_os)
    case "$os" in
        macos|linux) echo "$HOME/.claude" ;;
        windows)     echo "$USERPROFILE/.claude" ;;
        *)           echo "$HOME/.claude" ;;
    esac
}

# 获取项目级目录
get_project_dir() {
    echo "$(pwd)/.claude"
}

# 显示帮助
print_help() {
    echo ""
    echo -e "${BLUE}用法:${NC}"
    echo "  $0 [选项]"
    echo ""
    echo -e "${BLUE}选项:${NC}"
    echo "  -g, --global      卸载全局安装 (默认)"
    echo "  -p, --project     卸载项目级安装"
    echo "  -a, --all         卸载全部（全局 + 项目级）"
    echo "  -h, --help        显示帮助信息"
    echo ""
    echo -e "${BLUE}示例:${NC}"
    echo "  $0                # 卸载全局安装"
    echo "  $0 --project      # 卸载当前目录的项目级安装"
    echo "  $0 --all          # 卸载全部"
    echo ""
}

# 卸载函数
do_uninstall() {
    local target_dir="$1"
    local mode="$2"
    
    if [ ! -d "$target_dir" ]; then
        echo -e "${YELLOW}目录不存在: $target_dir${NC}"
        return 1
    fi
    
    echo -e "${BLUE}卸载模式: $mode${NC}"
    echo -e "${BLUE}目标目录: $target_dir${NC}"
    echo ""
    
    # 删除 skills
    echo -e "${YELLOW}删除 Skills...${NC}"
    rm -rf "$target_dir/skills/pipeline" 2>/dev/null && echo "  ✓ pipeline" || true
    rm -rf "$target_dir/skills/task-breakdown" 2>/dev/null && echo "  ✓ task-breakdown" || true
    rm -rf "$target_dir/skills/code-review" 2>/dev/null && echo "  ✓ code-review" || true
    rm -rf "$target_dir/skills/test-generator" 2>/dev/null && echo "  ✓ test-generator" || true
    
    # 删除 agents
    echo -e "${YELLOW}删除 Agents...${NC}"
    rm -f "$target_dir/agents/impact-analyzer.md" 2>/dev/null && echo "  ✓ impact-analyzer.md" || true
    rm -f "$target_dir/agents/prd-agent.md" 2>/dev/null && echo "  ✓ prd-agent.md" || true
    rm -f "$target_dir/agents/spec-agent.md" 2>/dev/null && echo "  ✓ spec-agent.md" || true
    rm -f "$target_dir/agents/coding-agent.md" 2>/dev/null && echo "  ✓ coding-agent.md" || true
    rm -f "$target_dir/agents/verification-agent.md" 2>/dev/null && echo "  ✓ verification-agent.md" || true
    
    # 删除 rules
    echo -e "${YELLOW}删除 Rules...${NC}"
    rm -f "$target_dir/rules/task-spec-template.md" 2>/dev/null && echo "  ✓ task-spec-template.md" || true
    rm -f "$target_dir/rules/api-spec-rules.md" 2>/dev/null && echo "  ✓ api-spec-rules.md" || true
    rm -f "$target_dir/rules/acceptance-criteria-rules.md" 2>/dev/null && echo "  ✓ acceptance-criteria-rules.md" || true
    rm -f "$target_dir/rules/frontend-coding-standards.md" 2>/dev/null && echo "  ✓ frontend-coding-standards.md" || true
    rm -f "$target_dir/rules/backend-coding-standards.md" 2>/dev/null && echo "  ✓ backend-coding-standards.md" || true
    rm -f "$target_dir/rules/tdd-pattern.md" 2>/dev/null && echo "  ✓ tdd-pattern.md" || true
    rm -f "$target_dir/rules/user-story-template.md" 2>/dev/null && echo "  ✓ user-story-template.md" || true
    rm -f "$target_dir/rules/non-functional-requirements.md" 2>/dev/null && echo "  ✓ non-functional-requirements.md" || true
    
    echo ""
}

# 打印 banner
echo -e "${YELLOW}"
echo "═══════════════════════════════════════════════════════════════"
echo "        AI Native Pipeline - 卸载程序"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--global)
            UNINSTALL_MODE="global"
            shift
            ;;
        -p|--project)
            UNINSTALL_MODE="project"
            shift
            ;;
        -a|--all)
            UNINSTALL_MODE="all"
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 确认卸载
echo -e "${BLUE}即将卸载: ${YELLOW}$UNINSTALL_MODE${NC}"
echo ""
read -p "确定要继续吗？(y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消卸载${NC}"
    exit 0
fi

echo ""

# 执行卸载
case "$UNINSTALL_MODE" in
    global)
        do_uninstall "$(get_global_dir)" "全局"
        ;;
    project)
        do_uninstall "$(get_project_dir)" "项目级"
        ;;
    all)
        do_uninstall "$(get_global_dir)" "全局"
        echo ""
        do_uninstall "$(get_project_dir)" "项目级"
        ;;
esac

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  卸载完成！${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
