#!/usr/bin/env python3
"""
真实评估 - 使用 LLM API 执行 Agent 任务

用法:
    python scripts/evaluate_real.py --agent impact-analyzer --api-key $API_KEY
"""

import json
import argparse
import requests
from pathlib import Path
from datetime import datetime


EVAL_DIR = Path(".harness/eval")
OUTPUTS_DIR = EVAL_DIR / "outputs"
AGENTS_DIR = Path("agents")

API_BASE = "https://api.longcat.chat/openai/v1"
DEFAULT_MODEL = "LongCat-Flash-Chat"


def read_agent_prompt(agent_name: str) -> str:
    """读取 Agent 提示词"""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    with open(agent_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取核心指令部分
    lines = content.split('\n')
    # 跳过 frontmatter
    start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---' and i > 0:
            start = i + 1
            break
    
    return '\n'.join(lines[start:])


def call_llm(system_prompt: str, user_message: str, api_key: str) -> str:
    """调用 LLM"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3
    }
    
    response = requests.post(
        f"{API_BASE}/chat/completions",
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"API 调用失败: {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]


def evaluate_agent(agent_name: str, api_key: str):
    """真实评估 Agent"""
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 读取任务
    tasks_file = EVAL_DIR / "tasks.json"
    with open(tasks_file, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    # 读取 Agent 提示词
    agent_prompt = read_agent_prompt(agent_name)
    
    # 读取项目代码
    project_path = Path("/tmp/test-project")
    project_context = ""
    for py_file in project_path.rglob("*.py"):
        relative_path = py_file.relative_to(project_path)
        content = py_file.read_text(encoding='utf-8')
        project_context += f"\n### {relative_path}\n```\n{content}\n```\n"
    
    print(f"\n真实评估 {agent_name}（使用 LLM API）...")
    print(f"任务数: {len(tasks)}\n")
    
    for task in tasks:
        print(f"[任务 {task['id']}] {task['description'][:30]}...")
        
        # 构建完整提示
        user_message = f"""项目代码:
{project_context}

任务: {task['description']}

请生成 Impact Map。"""
        
        # 调用 LLM
        try:
            output = call_llm(agent_prompt, user_message, api_key)
            
            # 保存输出
            output_file = OUTPUTS_DIR / agent_name / f"task_{task['id']}.md"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Agent: {agent_name}\n")
                f.write(f"# Task: {task['description']}\n")
                f.write(f"# Time: {datetime.now().isoformat()}\n\n")
                f.write(output)
            
            print(f"  ✅ 完成")
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
    
    print(f"\n✅ 评估完成，输出保存到: {OUTPUTS_DIR / agent_name}/")


def main():
    parser = argparse.ArgumentParser(description='真实评估 Agent')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--api-key', required=True, help='API Key')
    
    args = parser.parse_args()
    
    evaluate_agent(args.agent, args.api_key)


if __name__ == '__main__':
    main()
