#!/usr/bin/env python3
"""
自动运行 Agent 评估

用法:
    python scripts/run_agent_auto.py --agent impact-analyzer --task 1 --project /tmp/test-project
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


EVAL_DIR = Path(".harness/eval")
OUTPUTS_DIR = EVAL_DIR / "outputs"
AGENTS_DIR = Path("agents")


def read_agent_instructions(agent_name: str) -> str:
    """读取 Agent 指令"""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if not agent_file.exists():
        raise FileNotFoundError(f"Agent 文件不存在: {agent_file}")
    
    with open(agent_file, 'r', encoding='utf-8') as f:
        return f.read()


def analyze_project(project_path: str, task_description: str) -> dict:
    """分析项目代码（简化版 impact-analyzer）"""
    import subprocess
    
    project_dir = Path(project_path)
    
    # 判断是否是全新模块
    if "全新模块" in task_description or "新模块" in task_description:
        return {
            "type": "new_module",
            "recommendation": "跳过模块分析，直接进入 PRD 阶段"
        }
    
    # 查找相关文件
    keywords = extract_keywords(task_description)
    
    core_files = []
    dependent_files = []
    boundary = []
    risks = []
    
    # 扫描项目
    for py_file in project_dir.rglob("*.py"):
        content = py_file.read_text(encoding='utf-8')
        relative_path = str(py_file.relative_to(project_dir))
        
        # 检查是否包含关键词
        for keyword in keywords:
            if keyword.lower() in content.lower():
                core_files.append(relative_path)
                break
    
    # 去重
    core_files = list(set(core_files))
    
    # 查找依赖关系
    for py_file in project_dir.rglob("*.py"):
        relative_path = str(py_file.relative_to(project_dir))
        if relative_path not in core_files:
            content = py_file.read_text(encoding='utf-8')
            for core_file in core_files:
                module_name = Path(core_file).stem
                if f"from {module_name}" in content or f"import {module_name}" in content:
                    dependent_files.append(relative_path)
                    break
    
    dependent_files = list(set(dependent_files))
    
    # 识别风险
    for core_file in core_files:
        # 统计调用次数
        call_count = 0
        for dep_file in dependent_files:
            dep_content = (project_dir / dep_file).read_text(encoding='utf-8')
            module_name = Path(core_file).stem
            call_count += dep_content.count(module_name)
        
        if call_count > 5:
            risks.append(f"{Path(core_file).stem} 被 {call_count} 处调用")
    
    return {
        "type": "incremental",
        "core_files": core_files,
        "dependent_files": dependent_files[:5],  # 限制数量
        "boundary": boundary,
        "risks": risks
    }


def extract_keywords(task_description: str) -> list:
    """从任务描述中提取关键词"""
    keywords = []
    
    # 常见关键词
    keyword_map = {
        "登录": ["auth", "login", "session", "user"],
        "用户": ["user", "auth"],
        "认证": ["auth", "session", "token"],
        "商品": ["product", "item", "goods"],
        "订单": ["order"],
        "支付": ["payment", "pay"],
        "消息": ["message", "notification", "notify"],
        "数据库": ["db", "database", "query", "model"],
    }
    
    for key, values in keyword_map.items():
        if key in task_description:
            keywords.extend(values)
    
    return list(set(keywords))


def generate_impact_map(task_description: str, analysis: dict) -> str:
    """生成 Impact Map"""
    
    if analysis["type"] == "new_module":
        return f"""## Impact Map: {task_description}

**类型**: 全新模块

### 建议
- 参考 `src/user/` 模块结构
- 遵循项目 API 规范
"""
    
    output = f"""## Impact Map: {task_description}

**类型**: 增量开发

### Core Files (可修改)
"""
    
    for f in analysis["core_files"]:
        output += f"- `{f}`\n"
    
    output += "\n### Dependent Files (不可破坏)\n"
    
    if analysis["dependent_files"]:
        for f in analysis["dependent_files"]:
            output += f"- `{f}`\n"
    else:
        output += "- 无\n"
    
    output += "\n### Boundary (不可触碰)\n"
    
    if analysis["boundary"]:
        for f in analysis["boundary"]:
            output += f"- `{f}`\n"
    else:
        output += "- 无明确边界\n"
    
    output += "\n### Risks\n"
    
    if analysis["risks"]:
        for risk in analysis["risks"]:
            output += f"- {risk}\n"
    else:
        output += "- 无明显风险\n"
    
    return output


def run_agent(agent_name: str, task_id: int, project_path: str):
    """运行 Agent"""
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 读取任务
    tasks_file = EVAL_DIR / "tasks.json"
    with open(tasks_file, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        return
    
    print(f"\n运行 {agent_name}...")
    print(f"任务: {task['description']}")
    print(f"项目: {project_path}\n")
    
    # 分析项目
    analysis = analyze_project(project_path, task['description'])
    
    # 生成 Impact Map
    impact_map = generate_impact_map(task['description'], analysis)
    
    print(impact_map)
    
    # 保存输出
    output_file = OUTPUTS_DIR / agent_name / f"task_{task_id}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Agent: {agent_name}\n")
        f.write(f"# Task: {task['description']}\n")
        f.write(f"# Time: {datetime.now().isoformat()}\n\n")
        f.write(impact_map)
    
    print(f"\n✅ 输出已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='自动运行 Agent')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--task', type=int, required=True, help='任务 ID')
    parser.add_argument('--project', default='/tmp/test-project', help='项目路径')
    
    args = parser.parse_args()
    
    run_agent(args.agent, args.task, args.project)


if __name__ == '__main__':
    main()
