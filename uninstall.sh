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

# 要删除的组件列表
SKILLS_TO_REMOVE="pipeline task-breakdown code-review test-generator"
AGENTS_TO_REMOVE="impact-analyzer.md prd-agent.md spec-agent.md coding-agent.md verification-agent.md"
RULES_TO_REMOVE="task-spec-template.md api-spec-rules.md acceptance-criteria-rules.md frontend-coding-standards.md backend-coding-standards.md tdd-pattern.md user-story-template.md non-functional-requirements.md"

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
    echo -e "${GREEN}注意: 卸载只删除 ai-native-pipeline 的组件，不会影响其他 skills/agents${NC}"
    echo ""
}

# 检查是否有其他文件
check_other_files() {
    local target_dir="$1"
    local other_skills=0
    local other_agents=0
    local other_rules=0
    
    if [ -d "$target_dir/skills" ]; then
        for skill_dir in "$target_dir/skills"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                if [[ ! " $SKILLS_TO_REMOVE " =~ " $skill_name " ]]; then
                    other_skills=$((other_skills + 1))
                fi
            fi
        done
    fi
    
    if [ -d "$target_dir/agents" ]; then
        for agent_file in "$target_dir/agents"/*.md; do
            if [ -f "$agent_file" ]; then
                agent_name=$(basename "$agent_file")
                if [[ ! " $AGENTS_TO_REMOVE " =~ " $agent_name " ]]; then
                    other_agents=$((other_agents + 1))
                fi
            fi
        done
    fi
    
    if [ -d "$target_dir/rules" ]; then
        for rule_file in "$target_dir/rules"/*.md; do
            if [ -f "$rule_file" ]; then
                rule_name=$(basename "$rule_file")
                if [[ ! " $RULES_TO_REMOVE " =~ " $rule_name " ]]; then
                    other_rules=$((other_rules + 1))
                fi
            fi
        done
    fi
    
    if [ $other_skills -gt 0 ] || [ $other_agents -gt 0 ] || [ $other_rules -gt 0 ]; then
        echo -e "${GREEN}发现其他组件（将保留）:${NC}"
        [ $other_skills -gt 0 ] && echo -e "  ${GREEN}✓${NC} $other_skills 个其他 skills"
        [ $other_agents -gt 0 ] && echo -e "  ${GREEN}✓${NC} $other_agents 个其他 agents"
        [ $other_rules -gt 0 ] && echo -e "  ${GREEN}✓${NC} $other_rules 个其他 rules"
        echo ""
    fi
}

# 显示将要删除的文件
show_files_to_remove() {
    local target_dir="$1"
    
    echo -e "${YELLOW}将要删除的组件:${NC}"
    echo ""
    
    echo -e "  ${BLUE}Skills:${NC}"
    for skill in $SKILLS_TO_REMOVE; do
        if [ -d "$target_dir/skills/$skill" ]; then
            echo -e "    ${RED}✗${NC} $skill"
        else
            echo -e "    ${GREEN}✓${NC} $skill (未安装)"
        fi
    done
    
    echo ""
    echo -e "  ${BLUE}Agents:${NC}"
    for agent in $AGENTS_TO_REMOVE; do
        if [ -f "$target_dir/agents/$agent" ]; then
            echo -e "    ${RED}✗${NC} $agent"
        else
            echo -e "    ${GREEN}✓${NC} $agent (未安装)"
        fi
    done
    
    echo ""
    echo -e "  ${BLUE}Rules:${NC}"
    for rule in $RULES_TO_REMOVE; do
        if [ -f "$target_dir/rules/$rule" ]; then
            echo -e "    ${RED}✗${NC} $rule"
        else
            echo -e "    ${GREEN}✓${NC} $rule (未安装)"
        fi
    done
    
    echo ""
}

# 卸载函数
do_uninstall() {
    local target_dir="$1"
    local mode="$2"
    
    if [ ! -d "$target_dir" ]; then
        echo -e "${YELLOW}目录不存在: $target_dir${NC}"
        return 0
    fi
    
    echo -e "${BLUE}卸载模式: $mode${NC}"
    echo -e "${BLUE}目标目录: $target_dir${NC}"
    echo ""
    
    # 检查其他文件
    check_other_files "$target_dir"
    
    # 显示要删除的文件
    show_files_to_remove "$target_dir"
    
    # 删除 skills
    echo -e "${YELLOW}删除 Skills...${NC}"
    for skill in $SKILLS_TO_REMOVE; do
        if [ -d "$target_dir/skills/$skill" ]; then
            rm -rf "$target_dir/skills/$skill" 2>/dev/null && echo "  ✓ 删除 $skill" || echo "  ✗ 删除 $skill 失败"
        else
            echo "  - $skill (不存在)"
        fi
    done
    
    # 删除 agents
    echo -e "${YELLOW}删除 Agents...${NC}"
    for agent in $AGENTS_TO_REMOVE; do
        if [ -f "$target_dir/agents/$agent" ]; then
            rm -f "$target_dir/agents/$agent" 2>/dev/null && echo "  ✓ 删除 $agent" || echo "  ✗ 删除 $agent 失败"
        else
            echo "  - $agent (不存在)"
        fi
    done
    
    # 删除 rules
    echo -e "${YELLOW}删除 Rules...${NC}"
    for rule in $RULES_TO_REMOVE; do
        if [ -f "$target_dir/rules/$rule" ]; then
            rm -f "$target_dir/rules/$rule" 2>/dev/null && echo "  ✓ 删除 $rule" || echo "  ✗ 删除 $rule 失败"
        else
            echo "  - $rule (不存在)"
        fi
    done
    
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

# 显示卸载信息
echo -e "${BLUE}即将卸载: ${YELLOW}$UNINSTALL_MODE${NC}"
echo ""
echo -e "${GREEN}⚠ 此操作只删除 ai-native-pipeline 的组件${NC}"
echo -e "${GREEN}⚠ 其他 skills/agents/rules 将保留${NC}"
echo ""

# 确认卸载
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
echo -e "${GREEN}  其他组件已保留${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
