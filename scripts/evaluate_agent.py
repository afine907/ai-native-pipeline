#!/usr/bin/env python3
"""
Agent 评估脚本

用法:
    python evaluate_agent.py --agent impact-analyzer --test-cases test_cases.json
"""

import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Any


class AgentEvaluator:
    """Agent 评估器"""
    
    def __init__(self, agent_name: str, test_cases_path: str):
        self.agent_name = agent_name
        self.test_cases = self._load_test_cases(test_cases_path)
        self.results = []
        
    def _load_test_cases(self, path: str) -> list:
        """加载测试用例"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run(self) -> dict:
        """运行评估"""
        print(f"\n开始评估 {self.agent_name}")
        print(f"测试用例数: {len(self.test_cases)}")
        print("-" * 50)
        
        for i, case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}] {case['input']}")
            
            # 模拟运行 Agent（实际使用时替换为真实调用）
            start_time = time.time()
            output = self._run_agent(case['input'])
            duration = time.time() - start_time
            
            # 评估输出
            score = self._evaluate_output(output, case.get('expected', {}))
            
            self.results.append({
                'case_id': case.get('id', i),
                'input': case['input'],
                'output': output,
                'score': score,
                'duration': duration
            })
            
            print(f"  得分: {score['total']:.1f}/5")
            print(f"  耗时: {duration:.1f}s")
        
        return self._generate_report()
    
    def _run_agent(self, input_text: str) -> dict:
        """运行 Agent（模拟）"""
        # 这里应该调用真实的 Agent
        # 目前返回模拟数据
        return {
            'core_files': ['src/auth/session.py'],
            'boundary': ['src/payments/'],
            'risks': ['authenticate() 被多处调用']
        }
    
    def _evaluate_output(self, output: dict, expected: dict) -> dict:
        """评估输出质量"""
        scores = {}
        
        # 完整性 (0-5)
        if expected:
            coverage = len(set(output.keys()) & set(expected.keys())) / max(len(expected.keys()), 1)
            scores['completeness'] = coverage * 5
        else:
            scores['completeness'] = 4.0  # 无预期时给默认分
        
        # 准确性 (0-5)
        if expected and 'core_files' in expected:
            accuracy = len(set(output.get('core_files', [])) & set(expected['core_files'])) / max(len(expected['core_files']), 1)
            scores['accuracy'] = accuracy * 5
        else:
            scores['accuracy'] = 4.0
        
        # 简洁性 (0-5)
        output_size = len(str(output))
        if output_size < 500:
            scores['conciseness'] = 5.0
        elif output_size < 1000:
            scores['conciseness'] = 4.0
        else:
            scores['conciseness'] = 3.0
        
        # 可读性 (0-5)
        # 简单判断：是否有结构化输出
        if isinstance(output, dict):
            scores['readability'] = 4.5
        else:
            scores['readability'] = 3.0
        
        scores['total'] = sum(scores.values()) / len(scores)
        return scores
    
    def _generate_report(self) -> dict:
        """生成评估报告"""
        total_score = sum(r['score']['total'] for r in self.results) / len(self.results)
        avg_duration = sum(r['duration'] for r in self.results) / len(self.results)
        
        report = {
            'agent': self.agent_name,
            'date': datetime.now().isoformat(),
            'test_cases': len(self.test_cases),
            'avg_score': round(total_score, 2),
            'avg_duration': round(avg_duration, 2),
            'results': self.results
        }
        
        # 保存报告
        report_path = Path('.harness/eval') / f'report_{self.agent_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print("\n" + "=" * 50)
        print("评估报告")
        print("=" * 50)
        print(f"Agent: {self.agent_name}")
        print(f"测试用例: {len(self.test_cases)}")
        print(f"平均得分: {total_score:.2f}/5")
        print(f"平均耗时: {avg_duration:.1f}s")
        print(f"\n报告已保存: {report_path}")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='Agent 评估脚本')
    parser.add_argument('--agent', required=True, help='Agent 名称')
    parser.add_argument('--test-cases', required=True, help='测试用例文件路径')
    
    args = parser.parse_args()
    
    evaluator = AgentEvaluator(args.agent, args.test_cases)
    evaluator.run()


if __name__ == '__main__':
    main()
