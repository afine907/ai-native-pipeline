# AgentOps 设计

## 什么是 AgentOps？

AgentOps = AI Agent 的 DevOps

核心能力：
- **监控** - Agent 执行状态、性能指标
- **日志** - 完整的执行日志
- **告警** - 异常自动告警
- **回滚** - 快速回滚到稳定版本
- **A/B 测试** - 对比不同版本效果

---

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    AgentOps 平台                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   监控面板   │  │   日志系统   │  │   告警系统   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  版本管理    │  │  A/B 测试    │  │  回滚机制    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent 运行时                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  impact-analyzer → prd-agent → spec-agent → ...        │
│        │               │              │                 │
│        └───────────────┴──────────────┘                 │
│                        │                                 │
│                        ▼                                 │
│              ┌──────────────────┐                       │
│              │  AgentOps SDK   │                       │
│              └──────────────────┘                       │
│                        │                                 │
│                        ▼                                 │
│              上报日志、指标、事件                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 核心组件

### 1. 日志系统

记录 Agent 执行的完整日志：

```python
# .harness/logs/{session_id}/

# 执行日志
2026-04-28T09:00:00Z [INFO] impact-analyzer started
2026-04-28T09:00:05Z [INFO] impact-analyzer found 3 core files
2026-04-28T09:00:10Z [INFO] impact-analyzer completed in 10s
2026-04-28T09:00:10Z [INFO] prd-agent started
2026-04-28T09:00:20Z [INFO] prd-agent completed in 10s
...

# 性能日志
2026-04-28T09:00:10Z [METRIC] impact-analyzer: tokens=2500, time=10s
2026-04-28T09:00:20Z [METRIC] prd-agent: tokens=1800, time=10s
...

# 错误日志
2026-04-28T09:00:30Z [ERROR] verification failed: 2 tests failed
```

### 2. 监控面板

实时监控 Agent 状态：

```
┌─────────────────────────────────────────────────────────┐
│                   Agent 监控面板                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  今日执行                                                │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ 42  │ │ 38  │ │ 40  │ │ 42  │ │ 45  │              │
│  │ 总数│ │ 成功│ │ 失败│ │ 耗时│ │Token│              │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │
│                                                          │
│  成功率: 90% ████████████████████░░                     │
│  平均耗时: 45s                                          │
│  Token 消耗: 12K/任务                                   │
│                                                          │
│  最近执行                                                │
│  ┌────────────────────────────────────────────────────┐│
│  │ 09:25 手机号登录功能 ✅ 45s 8.5K tokens            ││
│  │ 09:20 JWT 迁移 ❌ 60s 12K tokens (验证失败)        ││
│  │ 09:15 商品列表 ✅ 38s 6.2K tokens                  ││
│  └────────────────────────────────────────────────────┘│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 3. 告警系统

异常自动告警：

```yaml
# .harness/alerts/config.yaml

alerts:
  - name: high_failure_rate
    condition: failure_rate > 0.2
    duration: 5m
    action: notify
    
  - name: slow_execution
    condition: avg_duration > 120s
    duration: 10m
    action: notify
    
  - name: high_token_usage
    condition: avg_tokens > 20000
    duration: 5m
    action: notify

notify:
  channels:
    - type: feishu
      webhook: https://open.feishu.cn/...
    - type: email
      to: team@example.com
```

### 4. 版本管理

管理 Agent 版本：

```bash
# 查看版本
.harness/versions/
├── impact-analyzer/
│   ├── v1.0.md
│   ├── v1.1.md
│   └── v2.0.md (current)
├── prd-agent/
│   ├── v1.0.md
│   └── v2.0.md (current)
...

# 版本元数据
.harness/versions/impact-analyzer/v2.0.json
{
  "version": "2.0",
  "created_at": "2026-04-28",
  "changes": ["精简输出", "移除追溯标注"],
  "metrics": {
    "accuracy": 0.85,
    "quality_score": 3.8,
    "avg_duration": 38
  }
}
```

### 5. A/B 测试

对比不同版本效果：

```yaml
# .harness/experiments/ab-test.yaml

experiment:
  name: "impact-analyzer v2 vs v3"
  
  variants:
    - name: control
      agent_version: v2.0
      traffic: 50%
    - name: treatment
      agent_version: v3.0
      traffic: 50%
      
  metrics:
    - accuracy
    - quality_score
    - duration
    
  duration: 7d
  
  success_criteria:
    accuracy_improvement: "> 5%"
```

### 6. 回滚机制

快速回滚到稳定版本：

```bash
# 回滚命令
.harness/rollback impact-analyzer v1.1

# 回滚流程
1. 保存当前版本到 .harness/backups/
2. 恢复 v1.1 版本的 Agent 文件
3. 更新版本标记
4. 发送通知
```

---

## AgentOps SDK

在 Agent 中集成 AgentOps：

```python
# 示例：impact-analyzer 集成

from agentops import AgentOps

ops = AgentOps(agent_name="impact-analyzer", version="2.0")

@ops.trace
def analyze_impact(task_description):
    ops.log("开始分析", level="INFO")
    
    try:
        # Agent 逻辑
        result = do_analysis(task_description)
        
        ops.metric("files_found", len(result["files"]))
        ops.log("分析完成", level="INFO")
        
        return result
        
    except Exception as e:
        ops.error(f"分析失败: {e}")
        raise
```

---

## 流水线验证

在流水线中集成验证：

```yaml
# .harness/pipeline/validation.yaml

stages:
  - name: pre_check
    checks:
      - agent_version_exists
      - test_cases_ready
      
  - name: run_agent
    agent: impact-analyzer
    timeout: 60s
    
  - name: validate_output
    checks:
      - output_not_empty
      - core_files_identified
      - boundary_defined
      
  - name: post_check
    checks:
      - execution_time_ok
      - token_usage_ok
```

### 验证规则

```yaml
# .harness/validation/rules.yaml

rules:
  - name: output_not_empty
    check: len(output) > 0
    error: "输出不能为空"
    
  - name: core_files_identified
    check: len(output.core_files) > 0
    error: "必须识别出至少一个核心文件"
    
  - name: boundary_defined
    check: len(output.boundary) >= 0
    warning: "建议定义 boundary"
    
  - name: execution_time_ok
    check: duration < 60
    error: "执行时间超过 60s"
    
  - name: token_usage_ok
    check: tokens < 10000
    warning: "Token 消耗较高"
```

---

## 快速开始

### 1. 初始化 AgentOps

```bash
# 创建 AgentOps 目录
mkdir -p .harness/{logs,versions,experiments,backups}

# 初始化 SDK
pip install agentops-sdk  # 假设有这个库
agentops init
```

### 2. 配置监控

```yaml
# .harness/config.yaml

agentops:
  enabled: true
  log_level: INFO
  
  monitoring:
    enabled: true
    dashboard: true
    
  alerts:
    enabled: true
    channels:
      - feishu
      
  version_control:
    enabled: true
    auto_backup: true
```

### 3. 运行 Agent

```bash
# 运行时会自动上报日志、指标
/pipeline 在用户模块增加手机号登录
```

### 4. 查看监控

```bash
# 打开监控面板
agentops dashboard

# 查看日志
cat .harness/logs/session-*/agent.log

# 查看指标
agentops metrics --last 24h
```

---

## 最佳实践

### 1. 日志分级

```
DEBUG - 调试信息（开发时使用）
INFO  - 正常执行信息
WARN  - 警告信息（不影响执行）
ERROR - 错误信息（执行失败）
```

### 2. 指标上报

每个 Agent 至少上报：
- 执行时间
- Token 消耗
- 输出大小
- 成功/失败

### 3. 版本发布流程

```
1. 开发新版本
2. 运行评估测试
3. 通过质量门禁
4. 发布到生产
5. 监控指标
6. 如有问题，快速回滚
```

### 4. A/B 测试原则

- 只测试一个变量
- 流量分配合理（50/50 或 80/20）
- 运行足够长时间（至少 7 天）
- 关注多个指标（不只是准确率）
