#!/usr/bin/env python3
"""
LLM-as-Judge 自动评估工具

用法:
    # 自动评估 Agent 输出
    python scripts/evaluate_llm_judge.py \
      --agent impact-analyzer \
      --api-key $LONGCAT_API_KEY
"""

import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional


EVAL_DIR = Path(".harness/eval")
OUTPUTS_DIR = EVAL_DIR / "outputs"
REPORTS_DIR = EVAL_DIR / "reports"

# LongCat API 配置
API_BASE = "https://api.longcat.chat/openai/v1"
DEFAULT_MODEL = "LongCat-Flash-Chat"


def call_llm(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """调用 LLM API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3  # 低温度，更稳定的评分
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


def evaluate_with_llm(agent_name: str, task_description: str, output: str, api_key: str) -> dict:
    """使用 LLM 评估输出"""
    
    prompt = f"""你是一个专业的代码评审专家。请评估以下 Agent 的输出质量。

## 任务描述
{task_description}

## Agent 输出
```
{output}
```

## 评估维度
请从以下 4 个维度评分（1-5 分）：

1. **完整性** - 是否覆盖了任务的所有要求？
2. **准确性** - 输出内容是否正确、有价值？
3. **简洁性** - 是否简洁，没有冗余信息？
4. **可读性** - 是否易于理解，结构清晰？

## 输出格式
请严格按照以下 JSON 格式输出：

```json
{{
  "completeness": <1-5>,
  "accuracy": <1-5>,
  "conciseness": <1-5>,
  "readability": <1-5>,
  "reasoning": "<简要说明评分理由>"
}}
```

只输出 JSON，不要有其他内容。"""

    try:
        response = call_llm(prompt, api_key)
        
        # 提取 JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            result = json.loads(json_match.group())
            return {
                'scores': {
                    '完整性': result.get('completeness', 3),
                    '准确性': result.get('accuracy', 3),
                    '简洁性': result.get('conciseness', 3),
                    '可读性': result.get('readability', 3)
                },
                'reasoning': result.get('reasoning', ''),
                'raw_response': response
            }
    except Exception as e:
        print(f"  ⚠️ LLM 评估失败: {e}")
    
    # 默认分数
    return {
        'scores': {
            '完整性': 3,
            '准确性': 3,
            '简洁性': 3,
            '可读性': 3
        },
        'reasoning': '评估失败，使用默认分数',
        'raw_response': ''
    }


def auto_evaluate(agent_name: str, api_key: str):
    """自动评估所有输出"""
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    output_dir = OUTPUTS_DIR / agent_name
    if not output_dir.exists():
        print(f"❌ 没有找到 {agent_name} 的输出")
        print(f"   请先运行: python scripts/evaluate_interactive.py --run-agent {agent_name} --task 1")
        return
    
    output_files = list(output_dir.glob("task_*.md"))
    if not output_files:
        print(f"❌ 没有找到 {agent_name} 的输出文件")
        return
    
    # 读取任务
    tasks_file = EVAL_DIR / "tasks.json"
    if not tasks_file.exists():
        print(f"❌ 请先生成任务: python scripts/evaluate_interactive.py --generate-tasks")
        return
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    print(f"\n使用 LLM 自动评估 {agent_name}...")
    print(f"找到 {len(output_files)} 个输出文件\n")
    
    results = []
    
    for i, output_file in enumerate(sorted(output_files), 1):
        task_id = int(output_file.stem.split("_")[1])
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            continue
        
        print(f"[{i}/{len(output_files)}] 评估任务 {task_id}: {task['description'][:30]}...")
        
        # 读取输出
        with open(output_file, 'r', encoding='utf-8') as f:
            output = f.read()
        
        # LLM 评估
        eval_result = evaluate_with_llm(agent_name, task['description'], output, api_key)
        
        avg_score = sum(eval_result['scores'].values()) / len(eval_result['scores'])
        
        print(f"  完整性: {eval_result['scores']['完整性']}/5")
        print(f"  准确性: {eval_result['scores']['准确性']}/5")
        print(f"  简洁性: {eval_result['scores']['简洁性']}/5")
        print(f"  可读性: {eval_result['scores']['可读性']}/5")
        print(f"  平均分: {avg_score:.2f}/5")
        print(f"  理由: {eval_result['reasoning'][:50]}...\n")
        
        results.append({
            'task_id': task_id,
            'description': task['description'],
            'scores': eval_result['scores'],
            'avg_score': round(avg_score, 2),
            'reasoning': eval_result['reasoning']
        })
    
    # 保存结果
    result_file = REPORTS_DIR / f"{agent_name}_llm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'agent': agent_name,
            'method': 'llm_judge',
            'date': datetime.now().isoformat(),
            'results': results,
            'summary': {
                'avg_score': round(sum(r['avg_score'] for r in results) / len(results), 2),
                'total_tasks': len(results)
            }
        }, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(f"✅ 评估完成")
    print(f"   平均分数: {sum(r['avg_score'] for r in results) / len(results):.2f}/5")
    print(f"   结果保存: {result_file}")


def main():
    parser = argparse.ArgumentParser(description='LLM-as-Judge 自动评估工具')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--api-key', required=True, help='LLM API Key')
    
    args = parser.parse_args()
    
    auto_evaluate(args.agent, args.api_key)


if __name__ == '__main__':
    main()
