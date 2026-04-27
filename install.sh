#!/bin/bash

# =============================================================================
# AI Native Pipeline - Harness Engine 安装脚本
# =============================================================================
# 用法: curl -fsSL https://your-server/ai-native-pipeline/install.sh | bash
# 或: ./install.sh
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 插件名称
PLUGIN_NAME="ai-native-pipeline"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos" ;;
        Linux*)     echo "linux" ;;
        CYGWIN*|MINGW*|MSYS*)    echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

# 获取 Claude Code 配置目录
get_claude_dir() {
    local os=$(detect_os)
    case "$os" in
        macos|linux)
            echo "$HOME/.claude"
            ;;
        windows)
            echo "$USERPROFILE/.claude"
            ;;
        *)
            echo "$HOME/.claude"
            ;;
    esac
}

# 打印 banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║        AI Native Pipeline - Harness Engine                   ║"
    echo "║                                                               ║"
    echo "║   5 AI Agents | Impact Map | Planning Gate | Auto Verify     ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 创建目录结构
create_directories() {
    local claude_dir="$1"
    
    echo -e "${BLUE}[1/4] 创建目录结构...${NC}"
    
    mkdir -p "$claude_dir/skills"
    mkdir -p "$claude_dir/agents"
    mkdir -p "$claude_dir/rules"
    mkdir -p "$claude_dir/plugins/data/$PLUGIN_NAME"
    
    echo -e "  ${GREEN}✓${NC} $claude_dir/skills/"
    echo -e "  ${GREEN}✓${NC} $claude_dir/agents/"
    echo -e "  ${GREEN}✓${NC} $claude_dir/rules/"
    echo -e "  ${GREEN}✓${NC} $claude_dir/plugins/data/$PLUGIN_NAME/"
}

# 安装 Skills
install_skills() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[2/4] 安装 Skills...${NC}"
    
    if [ -d "$source_dir/skills" ]; then
        for skill_dir in "$source_dir/skills"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                cp -r "$skill_dir" "$target_dir/skills/"
                echo -e "  ${GREEN}✓${NC} skill: $skill_name"
            fi
        done
    else
        echo -e "  ${YELLOW}!${NC} 未找到 skills 目录"
    fi
}

# 安装 Agents
install_agents() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[3/4] 安装 Agents...${NC}"
    
    if [ -d "$source_dir/agents" ]; then
        for agent_file in "$source_dir/agents"/*.md; do
            if [ -f "$agent_file" ]; then
                agent_name=$(basename "$agent_file")
                cp "$agent_file" "$target_dir/agents/"
                echo -e "  ${GREEN}✓${NC} agent: $agent_name"
            fi
        done
    else
        echo -e "  ${YELLOW}!${NC} 未找到 agents 目录"
    fi
}

# 安装 Rules
install_rules() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[4/4] 安装 Rules...${NC}"
    
    if [ -d "$source_dir/rules" ]; then
        for rule_file in "$source_dir/rules"/*.md; do
            if [ -f "$rule_file" ]; then
                rule_name=$(basename "$rule_file")
                cp "$rule_file" "$target_dir/rules/"
                echo -e "  ${GREEN}✓${NC} rule: $rule_name"
            fi
        done
    else
        echo -e "  ${YELLOW}!${NC} 未找到 rules 目录"
    fi
}

# 显示已安装组件
show_installed() {
    local claude_dir="$1"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  安装完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${BLUE}已安装组件:${NC}"
    echo ""
    
    # Skills
    echo -e "${YELLOW}Skills (4):${NC}"
    echo "  - pipeline        # 一键全流程"
    echo "  - task-breakdown  # 任务拆解"
    echo "  - code-review     # 代码审查"
    echo "  - test-generator  # 测试生成"
    echo ""
    
    # Agents
    echo -e "${YELLOW}Agents (5):${NC}"
    echo "  - impact-analyzer     # 代码影响分析"
    echo "  - prd-agent           # 需求分析"
    echo "  - spec-agent          # 技术规格"
    echo "  - coding-agent        # 代码生成"
    echo "  - verification-agent  # 验收验证"
    echo ""
    
    # Rules
    echo -e "${YELLOW}Rules (8):${NC}"
    echo "  - task-spec-template.md"
    echo "  - api-spec-rules.md"
    echo "  - acceptance-criteria-rules.md"
    echo "  - frontend-coding-standards.md"
    echo "  - backend-coding-standards.md"
    echo "  - tdd-pattern.md"
    echo "  - user-story-template.md"
    echo "  - non-functional-requirements.md"
    echo ""
    
    echo -e "${BLUE}使用方法:${NC}"
    echo ""
    echo -e "  ${GREEN}/pipeline${NC} 在现有登录模块基础上，增加 JWT 认证"
    echo ""
    echo -e "  或分步使用:"
    echo "  ${GREEN}/impact-analyzer${NC}    # 分析代码影响"
    echo "  ${GREEN}/prd-agent${NC}          # 需求分析"
    echo "  ${GREEN}/spec-agent${NC}         # 技术规格"
    echo "  ${GREEN}/coding-agent${NC}       # 代码生成"
    echo "  ${GREEN}/verification-agent${NC} # 验收验证"
    echo ""
}

# 检查是否已安装
check_existing() {
    local claude_dir="$1"
    
    if [ -d "$claude_dir/skills/pipeline" ] || [ -f "$claude_dir/agents/impact-analyzer.md" ]; then
        echo -e "${YELLOW}检测到已安装的版本，将进行更新...${NC}"
        echo ""
        return 0
    fi
    return 1
}

# 卸载函数
uninstall() {
    local claude_dir=$(get_claude_dir)
    
    echo -e "${YELLOW}正在卸载 $PLUGIN_NAME...${NC}"
    
    # 删除 skills
    rm -rf "$claude_dir/skills/pipeline" 2>/dev/null || true
    rm -rf "$claude_dir/skills/task-breakdown" 2>/dev/null || true
    rm -rf "$claude_dir/skills/code-review" 2>/dev/null || true
    rm -rf "$claude_dir/skills/test-generator" 2>/dev/null || true
    
    # 删除 agents
    rm -f "$claude_dir/agents/impact-analyzer.md" 2>/dev/null || true
    rm -f "$claude_dir/agents/prd-agent.md" 2>/dev/null || true
    rm -f "$claude_dir/agents/spec-agent.md" 2>/dev/null || true
    rm -f "$claude_dir/agents/coding-agent.md" 2>/dev/null || true
    rm -f "$claude_dir/agents/verification-agent.md" 2>/dev/null || true
    
    # 删除 rules
    rm -f "$claude_dir/rules/task-spec-template.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/api-spec-rules.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/acceptance-criteria-rules.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/frontend-coding-standards.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/backend-coding-standards.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/tdd-pattern.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/user-story-template.md" 2>/dev/null || true
    rm -f "$claude_dir/rules/non-functional-requirements.md" 2>/dev/null || true
    
    # 删除数据目录
    rm -rf "$claude_dir/plugins/data/$PLUGIN_NAME" 2>/dev/null || true
    
    echo -e "${GREEN}✓ 卸载完成${NC}"
}

# 主函数
main() {
    print_banner
    
    # 检查参数
    if [ "$1" = "--uninstall" ] || [ "$1" = "-u" ]; then
        uninstall
        exit 0
    fi
    
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  -h, --help       显示帮助信息"
        echo "  -u, --uninstall  卸载插件"
        echo "  -v, --version    显示版本信息"
        echo ""
        echo "无参数运行将安装插件"
        exit 0
    fi
    
    if [ "$1" = "--version" ] || [ "$1" = "-v" ]; then
        echo "ai-native-pipeline v1.0.0"
        exit 0
    fi
    
    # 确定源目录
    local source_dir
    if [ -n "$1" ] && [ -d "$1" ]; then
        source_dir="$1"
    elif [ -d "$(dirname "$0")" ] && [ -f "$(dirname "$0")/install.sh" ]; then
        # 从脚本所在目录安装
        source_dir="$(dirname "$0")"
    else
        echo -e "${RED}错误: 无法找到插件源文件${NC}"
        echo "请指定源目录: $0 <source-dir>"
        exit 1
    fi
    
    # 获取 Claude 目录
    local claude_dir=$(get_claude_dir)
    
    echo -e "${BLUE}安装目录: $claude_dir${NC}"
    echo ""
    
    # 检查现有安装
    check_existing "$claude_dir"
    
    # 创建目录
    create_directories "$claude_dir"
    
    # 安装组件
    install_skills "$source_dir" "$claude_dir"
    install_agents "$source_dir" "$claude_dir"
    install_rules "$source_dir" "$claude_dir"
    
    # 显示结果
    show_installed "$claude_dir"
}

# 运行主函数
main "$@"
