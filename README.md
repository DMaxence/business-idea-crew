# BusinessIdeas Crew

BusinessIdeas is a multi‑agent system built with [crewAI](https://crewai.com) that helps you generate, validate, and plan online business ideas. It orchestrates specialized agents to:

1) Propose a structured business idea, 2) Validate market viability with data, 3) Produce a concise project plan with milestones, resources, and assignments.

## How it works

- Agents (see `src/business_ideas/config/agents.yaml`):
  - Business Innovation Strategist (`business_ideator`)
  - Market Research & Validation Specialist (`market_analyst`) — provider "gemini" (`gemini-1.5-flash-8b`)
  - Project Planning & Development Coordinator (`project_coordinator`)
  - Product Requirements Documentation Specialist (`prd_specialist`)
  - Growth Marketing Strategist (`marketing_strategist`)

- Tasks and flow (see `src/business_ideas/config/tasks.yaml`):
  - `generate_business_idea_task` → structured idea proposal
  - `analyze_market_viability_task` → market validation with data
  - `create_project_plan_task` → plan with milestones and team tasks

- Process: sequential execution (see `src/business_ideas/crew.py`).
- Tools: `SerperDevTool` for web search.
- Optional input: `user_prompt` to steer the topic; defaults to current opportunities.

## Installation

Prereqs: Python >=3.10 <=3.13 and [UV](https://docs.astral.sh/uv/).

```bash
pip install uv
cd business_ideas
uv sync
```

## Configuration

Create a `.env` in the project root with your keys:

```bash
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
SERPER_API_KEY=...
```

- `OPENAI_API_KEY`: used by default agents.
- `GEMINI_API_KEY`: required for `market_analyst` (Gemini provider).
- `SERPER_API_KEY`: required by `SerperDevTool` for search.

## Run

### Option A: crewAI CLI

From the project root:

```bash
crewai run
```

Provide inputs interactively or pass them explicitly:

```bash
crewai run --inputs '{"user_prompt": "AI tools for teachers"}'
```

### Option B: via UV entrypoints

The project exposes script entrypoints (see `pyproject.toml`). Run the default flow:

```bash
uv run business_ideas
```

Other utilities:

```bash
# Train for N iterations and save to a file
uv run train 3 training.json

# Replay from a specific task id
uv run replay <task_id>

# Test for N iterations with a specific model
uv run test 2 gpt-4o-mini
```

## Output

The agents return structured sections matching the schemas in `tasks.yaml`:

- Business idea proposal
- Market viability analysis
- Project plan

To save results:

```bash
crewai run --inputs '{"user_prompt": "AI tools for teachers"}' > report.md
```

## Customize

- Edit agents: `src/business_ideas/config/agents.yaml`
- Edit tasks: `src/business_ideas/config/tasks.yaml`
- Orchestrate: `src/business_ideas/crew.py`
- Add tools: implement under `src/business_ideas/tools/` and wire them in `crew.py`

## Support

- Docs: https://docs.crewai.com
- Repo: https://github.com/joaomdmoura/crewai
- Discord: https://discord.com/invite/X4JWnZnxPb
