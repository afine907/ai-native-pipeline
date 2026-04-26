# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin for AI Native development workflow automation. It contains 4 independent Agents and 1 Pipeline Skill that together automate the full development lifecycle from requirements to code.

## Project Structure

```
ai-native-pipeline/
├── .claude-plugin/
│   └── plugin.json              # Plugin configuration
├── agents/
│   ├── module-context.md        # Module context analysis
│   ├── prd-agent.md             # Requirements analysis agent
│   ├── spec-agent.md            # Technical specification agent
│   └── coding-agent.md          # Code generation agent
└── skills/
    └── pipeline/
        └── SKILL.md             # Main pipeline orchestration skill
```

## Commands

This is a Claude Code plugin - no build/test commands required. To use:

```bash
# Full pipeline (runs all 4 agents in sequence)
/pipeline [requirement description]

# Individual agents
/module-context
/prd-agent [requirement]
/spec-agent [PRD content]
/coding-agent [task description]
```

## Architecture

### Agents (4 independent)
- **module-context**: Analyzes existing module structure for incremental development
- **prd-agent**: Converts user requirements into structured PRD documents (user stories, feature list, acceptance criteria)
- **spec-agent**: Converts PRD into detailed technical specifications
- **coding-agent**: Generates high-quality code based on specs, follows project conventions

### Pipeline Skill
The `pipeline` skill orchestrates all 4 agents in sequence:
```
User Requirement → Module Context → PRD Agent → Spec Agent → Coding Agent → Complete
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