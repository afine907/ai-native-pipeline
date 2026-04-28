#!/usr/bin/env python3
"""
交互式 Agent 评估工具

用法:
    # 步骤 1: 生成测试任务
    python scripts/evaluate_interactive.py --generate-tasks
    
    # 步骤 2: 运行 Agent 并保存输出
    python scripts/evaluate_interactive.py --run-agent impact-analyzer --task 1
    
    # 步骤 3: 评估所有输出
    python scripts/evaluate_interactive.py --evaluate impact-analyzer
    
    # 步骤 4: 生成报告
    python scripts/evaluate_interactive.py --report impact-analyzer
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


EVAL_DIR = Path(".harness/eval")
TASKS_FILE = EVAL_DIR / "tasks.json"
OUTPUTS_DIR = EVAL_DIR / "outputs"
REPORTS_DIR = EVAL_DIR / "reports"


def ensure_dirs():
    """确保目录存在"""
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_tasks():
    """生成测试任务"""
    tasks = [
        {
            "id": 1,
            "description": "在用户模块增加手机号登录功能",
            "type": "incremental",
            "difficulty": "medium"
        },
        {
            "id": 2,
            "description": "将登录模块从 session 改为 JWT",
            "type": "incremental",
            "difficulty": "hard"
        },
        {
            "id": 3,
            "description": "添加商品列表分页功能",
            "type": "incremental",
            "difficulty": "easy"
        },
        {
            "id": 4,
            "description": "全新模块：消息通知中心",
            "type": "new_module",
            "difficulty": "medium"
        },
        {
            "id": 5,
            "description": "优化数据库查询性能",
            "type": "optimization",
            "difficulty": "hard"
        }
    ]
    
    ensure_dirs()
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成 {len(tasks)} 个测试任务")
    print(f"   保存位置: {TASKS_FILE}")
    return tasks


def run_agent_interactive(agent_name: str, task_id: int):
    """交互式运行 Agent"""
    ensure_dirs()
    
    # 读取任务
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        return
    
    print("\n" + "=" * 60)
    print(f"任务 {task_id}: {task['description']}")
    print("=" * 60)
    
    print(f"\n请在 Claude Code 中运行以下命令：")
    print(f"\n  /{agent_name} {task['description']}\n")
    
    print("Agent 输出完成后，请粘贴输出内容（输入空行结束）：\n")
    
    # 收集用户输入
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    output_text = "\n".join(lines)
    
    if not output_text.strip():
        print("❌ 输出为空，已取消")
        return
    
    # 保存输出
    output_file = OUTPUTS_DIR / agent_name / f"task_{task_id}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Agent: {agent_name}\n")
        f.write(f"# Task: {task['description']}\n")
        f.write(f"# Time: {datetime.now().isoformat()}\n\n")
        f.write(output_text)
    
    print(f"\n✅ 已保存输出: {output_file}")


def evaluate_outputs(agent_name: str):
    """评估 Agent 输出"""
    ensure_dirs()
    
    output_dir = OUTPUTS_DIR / agent_name
    if not output_dir.exists():
        print(f"❌ 没有找到 {agent_name} 的输出")
        return
    
    output_files = list(output_dir.glob("task_*.md"))
    if not output_files:
        print(f"❌ 没有找到 {agent_name} 的输出文件")
        return
    
    print(f"\n评估 {agent_name} 的输出...")
    print(f"找到 {len(output_files)} 个输出文件\n")
    
    results = []
    
    for output_file in sorted(output_files):
        task_id = int(output_file.stem.split("_")[1])
        
        # 读取任务描述
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        # 读取输出
        with open(output_file, 'r', encoding='utf-8') as f:
            output = f.read()
        
        print(f"\n{'=' * 60}")
        print(f"任务 {task_id}: {task['description'] if task else 'Unknown'}")
        print(f"{'=' * 60}")
        
        # 显示输出摘要
        lines = output.split('\n')
        print(f"输出行数: {len(lines)}")
        print(f"输出预览: {lines[4][:100] if len(lines) > 4 else 'N/A'}...")
        
        # 交互式评分
        print("\n请评分 (1-5):")
        
        scores = {}
        for dimension in ['完整性', '准确性', '简洁性', '可读性']:
            while True:
                try:
                    score = float(input(f"  {dimension}: "))
                    if 1 <= score <= 5:
                        scores[dimension] = score
                        break
                    else:
                        print("  请输入 1-5 之间的分数")
                except ValueError:
                    print("  请输入有效数字")
        
        avg_score = sum(scores.values()) / len(scores)
        
        # 备注
        comment = input("\n备注（可选）: ")
        
        results.append({
            'task_id': task_id,
            'description': task['description'] if task else 'Unknown',
            'output_file': str(output_file),
            'scores': scores,
            'avg_score': round(avg_score, 2),
            'comment': comment
        })
        
        print(f"\n平均分: {avg_score:.2f}/5")
    
    # 保存结果
    result_file = REPORTS_DIR / f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'agent': agent_name,
            'date': datetime.now().isoformat(),
            'results': results,
            'summary': {
                'avg_score': round(sum(r['avg_score'] for r in results) / len(results), 2),
                'total_tasks': len(results)
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 评估结果已保存: {result_file}")


def generate_report(agent_name: str):
    """生成评估报告"""
    ensure_dirs()
    
    report_files = sorted(REPORTS_DIR.glob(f"{agent_name}_*.json"), reverse=True)
    if not report_files:
        print(f"❌ 没有找到 {agent_name} 的评估报告")
        return
    
    # 读取最新报告
    with open(report_files[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n" + "=" * 60)
    print(f"Agent 评估报告: {agent_name}")
    print("=" * 60)
    print(f"评估日期: {data['date']}")
    print(f"任务数量: {data['summary']['total_tasks']}")
    print(f"平均分数: {data['summary']['avg_score']}/5")
    
    print("\n详细结果:")
    print("-" * 60)
    
    for result in data['results']:
        print(f"\n任务 {result['task_id']}: {result['description']}")
        print(f"  完整性: {result['scores']['完整性']}/5")
        print(f"  准确性: {result['scores']['准确性']}/5")
        print(f"  简洁性: {result['scores']['简洁性']}/5")
        print(f"  可读性: {result['scores']['可读性']}/5")
        print(f"  平均分: {result['avg_score']}/5")
        if result['comment']:
            print(f"  备注: {result['comment']}")
    
    # 生成 Markdown 报告
    md_report = REPORTS_DIR / f"{agent_name}_report.md"
    with open(md_report, 'w', encoding='utf-8') as f:
        f.write(f"# Agent 评估报告: {agent_name}\n\n")
        f.write(f"**日期**: {data['date']}\n\n")
        f.write(f"**平均分数**: {data['summary']['avg_score']}/5\n\n")
        f.write("## 详细结果\n\n")
        f.write("| 任务 | 完整性 | 准确性 | 简洁性 | 可读性 | 平均分 |\n")
        f.write("|------|--------|--------|--------|--------|--------|\n")
        for result in data['results']:
            f.write(f"| {result['task_id']} | {result['scores']['完整性']} | {result['scores']['准确性']} | {result['scores']['简洁性']} | {result['scores']['可读性']} | {result['avg_score']} |\n")
    
    print(f"\n📄 Markdown 报告: {md_report}")


def compare_versions(agent_name: str):
    """对比不同版本的评估结果"""
    ensure_dirs()
    
    report_files = sorted(REPORTS_DIR.glob(f"{agent_name}_*.json"))
    if len(report_files) < 2:
        print(f"❌ 至少需要 2 个评估报告才能对比")
        return
    
    print("\n版本对比:")
    print("=" * 60)
    
    reports = []
    for rf in report_files[-2:]:  # 取最近两个
        with open(rf, 'r', encoding='utf-8') as f:
            reports.append(json.load(f))
    
    v1, v2 = reports[0], reports[1]
    
    print(f"版本 1: {v1['date'][:10]} - 平均分 {v1['summary']['avg_score']}/5")
    print(f"版本 2: {v2['date'][:10]} - 平均分 {v2['summary']['avg_score']}/5")
    
    diff = v2['summary']['avg_score'] - v1['summary']['avg_score']
    if diff > 0:
        print(f"\n✅ 改进: +{diff:.2f}")
    elif diff < 0:
        print(f"\n❌ 退步: {diff:.2f}")
    else:
        print(f"\n➡️ 无变化")


def main():
    parser = argparse.ArgumentParser(description='交互式 Agent 评估工具')
    parser.add_argument('--generate-tasks', action='store_true', help='生成测试任务')
    parser.add_argument('--run-agent', metavar='AGENT', help='运行指定 Agent')
    parser.add_argument('--task', type=int, help='指定任务 ID')
    parser.add_argument('--evaluate', metavar='AGENT', help='评估 Agent 输出')
    parser.add_argument('--report', metavar='AGENT', help='生成报告')
    parser.add_argument('--compare', metavar='AGENT', help='对比版本')
    
    args = parser.parse_args()
    
    if args.generate_tasks:
        generate_tasks()
    elif args.run_agent and args.task:
        run_agent_interactive(args.run_agent, args.task)
    elif args.evaluate:
        evaluate_outputs(args.evaluate)
    elif args.report:
        generate_report(args.report)
    elif args.compare:
        compare_versions(args.compare)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
