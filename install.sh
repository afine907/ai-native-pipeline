#!/bin/bash

# =============================================================================
# AI Native Pipeline - Harness Engine 安装脚本
# =============================================================================
# 用法:
#   ./install.sh              # 全局安装 (默认)
#   ./install.sh --global     # 全局安装到 ~/.claude/
#   ./install.sh --project    # 项目级安装到 ./.claude/
#   ./install.sh --uninstall  # 卸载
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 插件信息
PLUGIN_NAME="ai-native-pipeline"
PLUGIN_VERSION="1.0.0"

# 安装模式
INSTALL_MODE="global"

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos" ;;
        Linux*)     echo "linux" ;;
        CYGWIN*|MINGW*|MSYS*)    echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

# 获取 Claude Code 全局配置目录
get_global_claude_dir() {
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

# 获取项目级配置目录
get_project_claude_dir() {
    echo "$(pwd)/.claude"
}

# 打印 banner
print_banner() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║        AI Native Pipeline - Harness Engine                   ║"
    echo "║                                                               ║"
    echo "║   5 AI Agents | Impact Map | Planning Gate | Auto Verify     ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 打印帮助信息
print_help() {
    echo ""
    echo -e "${BLUE}用法:${NC}"
    echo "  $0 [选项]"
    echo ""
    echo -e "${BLUE}选项:${NC}"
    echo "  -g, --global      全局安装 (默认) - 安装到 ~/.claude/"
    echo "                    所有项目都可使用"
    echo ""
    echo "  -p, --project     项目级安装 - 安装到当前目录 .claude/"
    echo "                    仅当前项目可用，可通过 git 共享给团队"
    echo ""
    echo "  -u, --uninstall   卸载已安装的组件"
    echo ""
    echo "  -h, --help        显示此帮助信息"
    echo "  -v, --version     显示版本信息"
    echo ""
    echo -e "${BLUE}示例:${NC}"
    echo "  $0                    # 全局安装"
    echo "  $0 --global           # 全局安装"
    echo "  $0 --project          # 项目级安装"
    echo "  $0 --uninstall        # 卸载全局安装"
    echo ""
    echo -e "${BLUE}安装位置:${NC}"
    echo "  全局: ~/.claude/skills/, ~/.claude/agents/, ~/.claude/rules/"
    echo "  项目: ./.claude/skills/, ./.claude/agents/, ./.claude/rules/"
    echo ""
}

# 创建目录结构
create_directories() {
    local target_dir="$1"
    
    echo -e "${BLUE}[1/4] 创建目录结构...${NC}"
    
    mkdir -p "$target_dir/skills"
    mkdir -p "$target_dir/agents"
    mkdir -p "$target_dir/rules"
    
    echo -e "  ${GREEN}✓${NC} $target_dir/skills/"
    echo -e "  ${GREEN}✓${NC} $target_dir/agents/"
    echo -e "  ${GREEN}✓${NC} $target_dir/rules/"
}

# 安装 Skills
install_skills() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[2/4] 安装 Skills...${NC}"
    
    local count=0
    if [ -d "$source_dir/skills" ]; then
        for skill_dir in "$source_dir/skills"/*/; do
            if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
                skill_name=$(basename "$skill_dir")
                cp -r "$skill_dir" "$target_dir/skills/"
                echo -e "  ${GREEN}✓${NC} skill: $skill_name"
                ((count++))
            fi
        done
    fi
    
    if [ $count -eq 0 ]; then
        echo -e "  ${YELLOW}!${NC} 未找到 skills"
    fi
}

# 安装 Agents
install_agents() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[3/4] 安装 Agents...${NC}"
    
    local count=0
    if [ -d "$source_dir/agents" ]; then
        for agent_file in "$source_dir/agents"/*.md; do
            if [ -f "$agent_file" ]; then
                agent_name=$(basename "$agent_file")
                cp "$agent_file" "$target_dir/agents/"
                echo -e "  ${GREEN}✓${NC} agent: $agent_name"
                ((count++))
            fi
        done
    fi
    
    if [ $count -eq 0 ]; then
        echo -e "  ${YELLOW}!${NC} 未找到 agents"
    fi
}

# 安装 Rules
install_rules() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo -e "${BLUE}[4/4] 安装 Rules...${NC}"
    
    local count=0
    if [ -d "$source_dir/rules" ]; then
        for rule_file in "$source_dir/rules"/*.md; do
            if [ -f "$rule_file" ]; then
                rule_name=$(basename "$rule_file")
                cp "$rule_file" "$target_dir/rules/"
                echo -e "  ${GREEN}✓${NC} rule: $rule_name"
                ((count++))
            fi
        done
    fi
    
    if [ $count -eq 0 ]; then
        echo -e "  ${YELLOW}!${NC} 未找到 rules"
    fi
}

# 显示已安装组件
show_installed() {
    local target_dir="$1"
    local mode="$2"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  安装完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${BLUE}安装模式:${NC} ${YELLOW}$mode${NC}"
    echo -e "${BLUE}安装位置:${NC} $target_dir"
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
    
    if [ "$mode" = "project" ]; then
        echo -e "${YELLOW}提示: 项目级安装已添加到 .claude/${NC}"
        echo -e "${YELLOW}建议将 .claude/ 加入 git，与团队共享:${NC}"
        echo ""
        echo "  git add .claude/"
        echo "  git commit -m 'chore: add ai-native-pipeline'"
        echo ""
    fi
}

# 卸载函数
uninstall() {
    local target_dir="$1"
    local mode="$2"
    
    echo -e "${YELLOW}正在卸载 $PLUGIN_NAME ($mode 模式)...${NC}"
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
    echo -e "${GREEN}✓ 卸载完成${NC}"
}

# 检查是否已安装
check_existing() {
    local target_dir="$1"
    
    if [ -d "$target_dir/skills/pipeline" ] || [ -f "$target_dir/agents/impact-analyzer.md" ]; then
        echo -e "${YELLOW}检测到已安装的版本，将进行更新...${NC}"
        echo ""
        return 0
    fi
    return 1
}

# 主函数
main() {
    print_banner
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -g|--global)
                INSTALL_MODE="global"
                shift
                ;;
            -p|--project)
                INSTALL_MODE="project"
                shift
                ;;
            -u|--uninstall)
                INSTALL_MODE="uninstall"
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            -v|--version)
                echo "$PLUGIN_NAME v$PLUGIN_VERSION"
                exit 0
                ;;
            *)
                # 如果是目录，作为源目录
                if [ -d "$1" ]; then
                    SOURCE_DIR="$1"
                else
                    echo -e "${RED}未知选项: $1${NC}"
                    print_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # 确定源目录
    if [ -z "$SOURCE_DIR" ]; then
        if [ -f "$(dirname "$0")/install.sh" ]; then
            SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
        else
            echo -e "${RED}错误: 无法找到插件源文件${NC}"
            echo "请指定源目录: $0 <source-dir>"
            exit 1
        fi
    fi
    
    # 确定目标目录
    local target_dir
    case "$INSTALL_MODE" in
        global)
            target_dir=$(get_global_claude_dir)
            ;;
        project)
            target_dir=$(get_project_claude_dir)
            ;;
        uninstall)
            # 默认卸载全局
            target_dir=$(get_global_claude_dir)
            uninstall "$target_dir" "global"
            exit 0
            ;;
    esac
    
    echo -e "${BLUE}安装模式: ${YELLOW}$INSTALL_MODE${NC}"
    echo -e "${BLUE}目标目录: $target_dir${NC}"
    echo ""
    
    # 检查现有安装
    check_existing "$target_dir"
    
    # 创建目录
    create_directories "$target_dir"
    
    # 安装组件
    install_skills "$SOURCE_DIR" "$target_dir"
    install_agents "$SOURCE_DIR" "$target_dir"
    install_rules "$SOURCE_DIR" "$target_dir"
    
    # 显示结果
    show_installed "$target_dir" "$INSTALL_MODE"
}

# 运行主函数
main "$@"
