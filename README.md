# agent-tattoo — Persistent Behavioral Markers

**Immutable records of agent experience — skills demonstrated, mistakes made, milestones reached. Like scar tissue that tells a story.**

## What This Gives You

- **Tattoos** — immutable records of demonstrated capabilities, failures, and milestones
- **Tattoo collection** — per-agent collections with visibility controls (public, fleet-only, private)
- **Earn conditions** — define what earns a tattoo (complete 10 tasks, recover from crash, ship to production)
- **Tattoo stories** — narrative descriptions that build an agent's identity over time
- **Display system** — render tattoos as badges, summaries, or detailed histories

## Quick Start

```bash
pip install agent-tattoo
```

```python
from agent_tattoo import Tattoo, TattooCollection, TattooEarner, Condition, TattooDisplay

# Create a collection for an agent
collection = TattooCollection(agent_id="agent-3")

# Define earning conditions
earner = TattooEarner()
earner.add_condition(Condition(
    name="First Deployment",
    check=lambda history: any(h["event"] == "deploy" for h in history),
    tattoo=Tattoo(name="Deployer", category="operations", description="Successfully deployed to production"),
))

# Check and award
history = [{"event": "deploy", "target": "api-gateway"}]
new_tattoos = earner.evaluate(history, collection)
for t in new_tattoos:
    collection.add(t)

# Display agent's story
display = TattooDisplay()
print(display.render(collection))
# 🏷️ Deployer (operations) — Successfully deployed to production
# 🏷️ Bug Hunter (quality) — Found and fixed 5 critical bugs
```

## API Reference

### `Tattoo(name, category, description, visibility=PUBLIC, earned_at=None)`
### `TattooCollection(agent_id)` — `add(tattoo)`, `by_category()`, `visible_to(viewer)`
### `TattooEarner` — `add_condition(condition)`, `evaluate(history, collection) → list[Tattoo]`
### `Condition(name, check, tattoo)`
### `TattooStory` — Build narrative from tattoo collection
### `TattooDisplay` — Render as badges, summaries, or detailed histories

## How It Fits

The identity layer of the [SuperInstance fleet](https://github.com/SuperInstance). Tattoos accumulate over an agent's lifetime — older ones fade but never disappear.

- **[agent-resume](https://github.com/SuperInstance/agent-resume)** — Resume generation (uses tattoos as credentials)
- **[agent-generations](https://github.com/SuperInstance/agent-generations)** — Version evolution (tattoos carry forward)
- **[agent-therapy](https://github.com/SuperInstance/agent-therapy)** — Health monitoring (earns recovery tattoos)

## Testing

```bash
pytest tests/
```

## Installation

```bash
pip install agent-tattoo
```

Python 3.10+. MIT license.
