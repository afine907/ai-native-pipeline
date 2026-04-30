# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin for AI Native development workflow automation based on Harness Engineering methodology. It contains 5 Agents, 4 Skills, and 8 Rules that together automate the full development lifecycle from requirements to code.

## Project Structure

```
ai-native-pipeline/
├── .claude-plugin/
│   └── plugin.json              # Plugin configuration
├── agents/                      # 5 core Agents
│   ├── impact-analyzer.md       # Code impact analysis
│   ├── prd-agent.md             # Requirements analysis
│   ├── spec-agent.md            # Technical specification
│   ├── coding-agent.md          # Code generation (TDD)
│   └── verification-agent.md    # Acceptance verification
├── skills/                      # 4 Skills
│   ├── pipeline/                # Main pipeline orchestration
│   ├── task-breakdown/          # Complex task decomposition
│   ├── code-review/             # Code review
│   └── test-generator/          # Test generation
├── rules/                       # 8 coding rules & templates
│   ├── task-spec-template.md
│   ├── api-spec-rules.md
│   ├── acceptance-criteria-rules.md
│   ├── frontend-coding-standards.md
│   ├── backend-coding-standards.md
│   ├── tdd-pattern.md
│   ├── user-story-template.md
│   └── non-functional-requirements.md
├── scripts/                     # Evaluation scripts
│   ├── evaluate_agent.py        # Agent evaluation (mock mode)
│   ├── evaluate_real.py         # Real evaluation via LLM API
│   ├── evaluate_llm_judge.py    # LLM-as-Judge evaluation
│   ├── evaluate_interactive.py  # Interactive evaluation
│   └── run_agent_auto.py        # Auto agent runner
├── tests/                       # Test cases
│   └── eval/
│       └── test_cases_*.json    # Per-agent test cases
└── .github/workflows/           # CI/CD
    ├── ci.yml                   # Lint + test + plugin validation
    ├── evaluate.yml             # Agent evaluation
    ├── e2e-test.yml             # End-to-end pipeline test
    ├── release.yml              # Release build
    └── security.yml             # Security scan
```

## Commands

This is a Claude Code plugin - no build/test commands required. To use:

```bash
# Full pipeline (runs all 5 agents in sequence)
/pipeline [requirement description]

# Individual agents
/impact-analyzer [requirement]
/prd-agent [requirement]
/spec-agent [PRD content]
/coding-agent [task description]
/verification-agent

# Task breakdown
/task-breakdown
```

## Architecture

### Pipeline Flow

```
User Requirement
    → impact-analyzer (code impact analysis)
    → prd-agent (requirements + task spec)
    → [PAUSE] Planning Gate: user confirms scope
    → spec-agent (technical specification)
    → [auto] task-breakdown (if complex: API > 3 or cross-module)
    → coding-agent (TDD implementation)
    → [PAUSE] Planning Gate: user confirms code
    → verification-agent (acceptance verification)
    → Done
```

### Agents (5 independent)
- **impact-analyzer**: Analyzes code impact, generates Impact Map. Detects Core Files, Dependent Files, Boundary, and Risks.
- **prd-agent**: Converts user requirements into structured Task Spec (scope, priorities, acceptance criteria).
- **spec-agent**: Converts Task Spec into detailed Technical Spec (API design, data model, tech decisions).
- **coding-agent**: Implements code using TDD (Red → Green → Refactor). Follows project conventions.
- **verification-agent**: Verifies acceptance criteria by running tests, lint, type checks. Auto-derives checks from Spec.

### Skills (4)
- **pipeline**: Orchestrates all 5 agents in sequence with Planning Gates.
- **task-breakdown**: Auto-triggered when SPEC complexity is high. Generates parallel/serial execution plan.
- **code-review**: Standalone code review.
- **test-generator**: Standalone test generation.

### Agent Tools
Each agent declares `tools` in its frontmatter (e.g., `tools: Read, Bash, Grep`). These define which tools the agent is **allowed to use** during execution. Ensure declarations match actual agent needs:
- impact-analyzer: Read, Bash, Grep (read-only analysis)
- coding-agent: Read, Write, Edit, Bash (full code manipulation)
- verification-agent: Read, Bash (read-only verification)

### Key Principles
- Agents use prompt engineering only, no external dependencies
- Each agent focuses on a single responsibility
- Pipeline enables end-to-end automation, but agents can be used independently
- Planning Gates provide human oversight at critical checkpoints
- Code generation follows existing project conventions (SOLID, DRY)

## Evaluation

```bash
# Generate test tasks
python scripts/evaluate_interactive.py --generate-tasks

# Run real evaluation (requires API key)
python scripts/evaluate_real.py --agent impact-analyzer --api-key $KEY

# Run LLM-as-Judge evaluation
python scripts/evaluate_llm_judge.py --agent impact-analyzer --api-key $KEY

# Quality gate: avg score >= 3.5/5
```

## CI/CD

- **CI**: Push/PR to master → lint + test + plugin validation + agent evaluation
- **E2E Test**: Manual trigger / daily at 2am → full pipeline test
- **Agent Evaluation**: Manual trigger / PR with `needs-evaluation` label
- **Quality Gate**: Agent avg score must be >= 3.5/5 to pass
