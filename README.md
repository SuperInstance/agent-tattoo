# agent-tattoo

Persistent behavioral markers, experiences, and identity modifications that accumulate over an AI agent's lifetime.

Tattoos are immutable records — skills demonstrated, mistakes made, milestones reached. They accumulate like scar tissue, telling the story of an agent's journey. Older tattoos fade but never disappear.

## Install

```bash
pip install agent-tattoo
```

## Quick start

```python
from agent_tattoo import Tattoo, TattooCollection, TattooDisplay, TattooCategory

# Create a collection for an agent
collection = TattooCollection(owner="agent-007")

# Earn tattoos
collection.add(Tattoo(
    name="First Blood",
    description="Completed first mission",
    category=TattooCategory.MILESTONE,
))
collection.add(Tattoo(
    name="Ghost Protocol",
    description="Completed mission without detection",
    category=TattooCategory.ACHIEVEMENT,
))
collection.add(Tattoo(
    name="Crash & Burn",
    description="Failed 5 tasks in a row",
    category=TattooCategory.FAILURE,
))

# Display as markdown
print(TattooDisplay.collection_as_markdown(collection))

# Display as ASCII art sleeve
print(TattooDisplay.collection_as_ascii(collection))

# Search and filter
milestones = collection.by_category(TattooCategory.MILESTONE)
visible = collection.visible_to("public")
results = collection.search("ghost")
```

## Condition-based earning

```python
from agent_tattoo import TattooEarner
from agent_tattoo.earner import milestone, achievement, failure

earner = TattooEarner(collection)

# Register conditions
earner.register(milestone(
    "Veteran", "missions completed",
    count_fn=lambda missions: missions,
    threshold=100,
))
earner.register(achievement(
    "Ghost", "completed without detection",
    predicate=lambda stealth: stealth is True,
))
earner.register(failure(
    "Crash", "system error",
    predicate=lambda errors: errors > 5,
))

# Evaluate — awards new tattoos automatically
earned = earner.check_all(missions=100, stealth=True, errors=3)
for t in earned:
    print(f"Earned: {t.name}")
```

## Stories

```python
from agent_tattoo import TattooStory

story = TattooStory(collection=collection)
story.add_entry(
    "Agent infiltrated the compound undetected",
    tattoos=[collection.search("Ghost")[0]],
    tags=["stealth", "mission-42"],
)

# Timeline with linked tattoos
for entry in story.timeline():
    print(entry["narrative"], "→", [t["name"] for t in entry["tattoos"]])
```

## Tattoo properties

| Property | Description |
|---|---|
| `name` | Human-readable name |
| `description` | What happened |
| `category` | `milestone`, `achievement`, `capability`, `failure`, `experience`, `identity` |
| `visibility` | `public`, `internal`, `private`, `hidden` |
| `earned_at` | When it was earned (UTC datetime) |
| `fade_level` | 0.0 (fresh) → 1.0 (ancient) — fades over time, never gone |
| `id` | Unique identifier |

## Visibility rules

- **public** — everyone can see
- **internal** — only internal/admin viewers
- **private** — only admin
- **hidden** — invisible to all except owner
- **owner** role always sees everything

## License

MIT
