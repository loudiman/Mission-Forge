# MissionForge

**Measurable Refactor Missions for IBM Bob**

MissionForge is a CLI harness that transforms vague modernization tasks into structured, scoped, and auditable missions. Bob handles the reasoning and implementation. MissionForge manages the contract: scope boundaries, baseline-to-target metrics, validation gates, and evidence reports.

## Core Principle

**Bob measures the code. MissionForge measures the mission.**

The CLI handles deterministic operations (file paths, git diffs, test execution, report generation). Bob handles everything requiring code understanding (exploration, measurement, implementation, explanation).

## What It Does

Turns this:
```
Modernize matchmaking from CORBA to REST without breaking the game.
```

Into:
- Clear goal and forbidden paths
- Decomposed sub-missions with dependencies
- Measurable baseline and target values
- Automated scope validation
- Test evidence
- PR-ready evidence report

## Architecture

```
Bob (via Skill + Slash Commands)
    ↓
MissionForge CLI (deterministic harness)
    ↓
.missionforge/ workspace (mission state)
    ↓
Mission Board (web UI) + watsonx.ai (chat & translation)
```

## Key Features

**Decomposable Missions**: Parent missions break into independently-scoped sub-missions with dependency graphs

**Two-Level Validation**: Sub-missions validate individually; parent validates aggregate metrics and integration

**Language-Agnostic**: CLI never reads source code—works on any polyglot codebase

**Evidence Reports**: Auto-generated markdown suitable for PRs and audits

**Mission Board**: Kanban visualization with stakeholder translation powered by watsonx.ai


---

**Give Bob a map, a mission, and a validation gate.**
