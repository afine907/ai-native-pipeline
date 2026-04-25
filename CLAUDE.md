# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin for AI Native development workflow automation. It contains 5 independent Agents and 1 Pipeline Skill that together automate the full development lifecycle from requirements to testing.

## Project Structure

```
ai-native-pipeline/
├── .claude-plugin/
│   └── plugin.json              # Plugin configuration
├── agents/
│   ├── prd-agent.md             # Requirements analysis agent
│   ├── task-agent.md            # Task breakdown agent
│   ├── coding-agent.md          # Code generation agent
│   ├── review-agent.md          # Code review agent
│   └── test-agent.md            # Test generation agent
└── skills/
    └── pipeline/
        └── SKILL.md             # Main pipeline orchestration skill
```

## Commands

This is a Claude Code plugin - no build/test commands required. To use:

```bash
# Full pipeline (runs all 5 agents in sequence)
/pipeline [requirement description]

# Individual agents
/prd-agent [requirement]
/task-agent [PRD content]
/coding-agent [task description]
/review-agent [code path or content]
/test-agent [code path]
```

## Architecture

### Agents (5 independent)
- **prd-agent**: Converts user requirements into structured PRD documents (user stories, feature list, acceptance criteria)
- **task-agent**: Breaks down PRD into executable technical tasks with dependencies and priorities
- **coding-agent**: Generates high-quality code based on tasks, follows project conventions
- **review-agent**: Reviews generated code for correctness, security, performance, best practices
- **test-agent**: Generates unit tests and E2E tests for the code

### Pipeline Skill
The `pipeline` skill orchestrates all 5 agents in sequence:
```
User Requirement → PRD Agent → Task Agent → Coding Agent → Review Agent → Test Agent → Complete
```

Each agent is defined with frontmatter specifying:
- `name`: Agent identifier
- `description`: What the agent does
- `model`: Claude model to use (sonnet)
- `effort`: Estimated complexity (medium)
- `maxTurns`: Maximum conversation turns

## Key Principles

- Agents use prompt engineering only, no external dependencies
- Each agent focuses on a single responsibility in the development workflow
- The pipeline enables end-to-end automation, but agents can be used independently
- Code generation follows existing project conventions and best practices (SOLID, DRY)