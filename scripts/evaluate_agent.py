#!/usr/bin/env python3
"""
Agent 评估脚本 - 支持 mock 和真实 LLM 两种模式

用法:
    # Mock 模式（无需 API，用于本地调试）
    python scripts/evaluate_agent.py --agent impact-analyzer --test-cases tests/eval/test_cases_impact_analyzer.json

    # 真实模式（使用 LLM API）
    python scripts/evaluate_agent.py --agent impact-analyzer --test-cases tests/eval/test_cases_impact_analyzer.json --api-key $LONGCAT_API_KEY
"""

import json
import re
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Any, Optional


# LLM API 配置
API_BASE = "https://api.longcat.chat/openai/v1"
DEFAULT_MODEL = "LongCat-Flash-Chat"

# 评估目录
EVAL_DIR = Path(".harness/eval")
OUTPUTS_DIR = EVAL_DIR / "outputs"
REPORTS_DIR = EVAL_DIR / "reports"
AGENTS_DIR = Path("agents")


def read_agent_prompt(agent_name: str) -> str:
    """读取 Agent 提示词"""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if not agent_file.exists():
        raise FileNotFoundError(f"Agent 文件不存在: {agent_file}")

    with open(agent_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 跳过 frontmatter
    lines = content.split('\n')
    start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---' and i > 0:
            start = i + 1
            break

    return '\n'.join(lines[start:])


def call_llm(system_prompt: str, user_message: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """调用 LLM API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
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
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"API 调用失败 ({response.status_code}): {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def judge_output(agent_name: str, task_description: str, output: str, api_key: str) -> dict:
    """使用 LLM-as-Judge 评估输出质量"""
    prompt = f"""你是一个专业的代码评审专家。请评估以下 Agent 的输出质量。

## Agent: {agent_name}
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
        response = call_llm(prompt, "", api_key)
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            result = json.loads(json_match.group())
            return {
                'completeness': result.get('completeness', 3),
                'accuracy': result.get('accuracy', 3),
                'conciseness': result.get('conciseness', 3),
                'readability': result.get('readability', 3),
                'reasoning': result.get('reasoning', '')
            }
    except Exception as e:
        print(f"  ⚠️ LLM 评估失败: {e}")

    return {
        'completeness': 3, 'accuracy': 3,
        'conciseness': 3, 'readability': 3,
        'reasoning': '评估失败，使用默认分数'
    }


class AgentEvaluator:
    """Agent 评估器 - 支持 mock 和真实模式"""

    def __init__(self, agent_name: str, test_cases_path: str, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.agent_name = agent_name
        self.test_cases = self._load_test_cases(test_cases_path)
        self.api_key = api_key
        self.model = model
        self.results = []
        self.is_real_mode = api_key is not None

    def _load_test_cases(self, path: str) -> list:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def run(self) -> dict:
        """运行评估"""
        mode = "真实 LLM" if self.is_real_mode else "Mock"
        print(f"\n{'=' * 50}")
        print(f"评估 Agent: {self.agent_name}  模式: {mode}")
        print(f"测试用例数: {len(self.test_cases)}")
        print(f"{'=' * 50}\n")

        if self.is_real_mode:
            agent_prompt = read_agent_prompt(self.agent_name)

        for i, case in enumerate(self.test_cases, 1):
            print(f"[{i}/{len(self.test_cases)}] {case['input']}")

            start_time = time.time()

            if self.is_real_mode:
                # 真实模式：调用 LLM
                try:
                    output_text = call_llm(
                        agent_prompt,
                        f"任务: {case['input']}\n\n请按照你的核心指令执行。",
                        self.api_key,
                        self.model
                    )
                    # 用 LLM-as-Judge 评分
                    score = judge_output(self.agent_name, case['input'], output_text, self.api_key)
                    output = {'raw_output': output_text}
                except Exception as e:
                    print(f"  ❌ LLM 调用失败: {e}")
                    output = {'error': str(e)}
                    score = {'completeness': 0, 'accuracy': 0, 'conciseness': 0, 'readability': 0, 'reasoning': f'调用失败: {e}'}
            else:
                # Mock 模式
                output = self._mock_agent(case['input'])
                score = self._evaluate_output(output, case.get('expected', {}))

            duration = time.time() - start_time

            total = sum(score[k] for k in ['completeness', 'accuracy', 'conciseness', 'readability']) / 4

            self.results.append({
                'case_id': case.get('id', i),
                'input': case['input'],
                'output': output,
                'score': score,
                'total': round(total, 2),
                'duration': round(duration, 2)
            })

            print(f"  完整性: {score['completeness']}/5  准确性: {score['accuracy']}/5  "
                  f"简洁性: {score['conciseness']}/5  可读性: {score['readability']}/5")
            print(f"  平均分: {total:.2f}/5  耗时: {duration:.1f}s")
            if score.get('reasoning'):
                print(f"  理由: {score['reasoning'][:80]}")
            print()

        return self._generate_report()

    def _mock_agent(self, input_text: str) -> dict:
        """Mock Agent 输出（用于无 API 时的本地调试）"""
        return {
            'core_files': ['src/auth/session.py'],
            'boundary': ['src/payments/'],
            'risks': ['authenticate() 被多处调用']
        }

    def _evaluate_output(self, output: dict, expected: dict) -> dict:
        """评估输出质量（mock 模式专用）"""
        scores = {}

        if expected:
            coverage = len(set(output.keys()) & set(expected.keys())) / max(len(expected.keys()), 1)
            scores['completeness'] = round(coverage * 5, 1)
        else:
            scores['completeness'] = 4.0

        if expected and 'core_files' in expected:
            accuracy = len(set(output.get('core_files', [])) & set(expected['core_files'])) / max(len(expected['core_files']), 1)
            scores['accuracy'] = round(accuracy * 5, 1)
        else:
            scores['accuracy'] = 4.0

        output_size = len(str(output))
        scores['conciseness'] = 5.0 if output_size < 500 else (4.0 if output_size < 1000 else 3.0)

        scores['readability'] = 4.5 if isinstance(output, dict) else 3.0
        scores['reasoning'] = 'Mock 模式自动评分'

        return scores

    def _generate_report(self) -> dict:
        """生成评估报告"""
        total_score = sum(r['total'] for r in self.results) / len(self.results)
        avg_duration = sum(r['duration'] for r in self.results) / len(self.results)

        report = {
            'agent': self.agent_name,
            'mode': 'real' if self.is_real_mode else 'mock',
            'model': self.model if self.is_real_mode else None,
            'date': datetime.now().isoformat(),
            'test_cases': len(self.test_cases),
            'avg_score': round(total_score, 2),
            'avg_duration': round(avg_duration, 2),
            'results': self.results
        }

        # 保存报告
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path = REPORTS_DIR / f'report_{self.agent_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 打印摘要
        print(f"\n{'=' * 50}")
        print("评估报告")
        print(f"{'=' * 50}")
        print(f"Agent: {self.agent_name}")
        print(f"模式: {'真实 LLM' if self.is_real_mode else 'Mock'}")
        print(f"测试用例: {len(self.test_cases)}")
        print(f"平均得分: {total_score:.2f}/5")
        print(f"平均耗时: {avg_duration:.1f}s")

        # 质量门禁
        if total_score < 3.5:
            print(f"❌ 未通过质量门禁 (3.5/5)")
        else:
            print(f"✅ 通过质量门禁 (3.5/5)")

        print(f"\n报告已保存: {report_path}")

        return report


def main():
    parser = argparse.ArgumentParser(description='Agent 评估脚本')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--test-cases', required=True, help='测试用例文件路径')
    parser.add_argument('--api-key', help='LLM API Key（不提供则使用 mock 模式）')
    parser.add_argument('--model', default=DEFAULT_MODEL, help=f'LLM 模型名（默认: {DEFAULT_MODEL}）')

    args = parser.parse_args()

    evaluator = AgentEvaluator(args.agent, args.test_cases, args.api_key, args.model)
    evaluator.run()


if __name__ == '__main__':
    main()
