#!/usr/bin/env python3
"""
Vacuum Cleaner Agent (Simple Reflex Agent)
==========================================
Classic two-room vacuum world for AI lab coursework.

Environment:
  - Two rooms: A (left) and B (right)
  - Each room may be Clean or Dirty
  - Agent can Sense location + dirt, Suck, or Move Left/Right

Agent type: Simple reflex agent
  - If current location is Dirty -> Suck
  - Else if in A -> Move Right
  - Else if in B -> Move Left

Performance measure:
  +10 for each successful Suck (dirt cleaned)
  -1 for each action (energy cost)

Default demo runs automatically with no interactive input.
Optional: pass --interactive to choose initial dirt status.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal

Location = Literal["A", "B"]
Status = Literal["Clean", "Dirty"]
Action = Literal["Suck", "Left", "Right", "NoOp"]


@dataclass
class Environment:
    """Two-room vacuum world state."""

    dirt: Dict[Location, Status]
    agent_location: Location = "A"
    step: int = 0
    performance: int = 0
    history: List[str] = field(default_factory=list)

    def percept(self) -> tuple[Location, Status]:
        """What the agent currently perceives."""
        loc = self.agent_location
        return loc, self.dirt[loc]

    def is_all_clean(self) -> bool:
        return all(s == "Clean" for s in self.dirt.values())

    def print_state(self, title: str = "Environment") -> None:
        a = self.dirt["A"]
        b = self.dirt["B"]
        agent_a = " [AGENT]" if self.agent_location == "A" else ""
        agent_b = " [AGENT]" if self.agent_location == "B" else ""
        print(f"\n  --- {title} (step {self.step}) ---")
        print(f"  +----------+----------+")
        print(f"  | Room A   | Room B   |")
        print(f"  | {a:<8} | {b:<8} |")
        print(f"  |{agent_a:<10}|{agent_b:<10}|")
        print(f"  +----------+----------+")
        print(f"  Performance score: {self.performance}")


def simple_reflex_agent(location: Location, status: Status) -> Action:
    """
    Simple reflex rules (condition-action):
      if status == Dirty  -> Suck
      else if location A  -> Right
      else if location B  -> Left
    """
    if status == "Dirty":
        return "Suck"
    if location == "A":
        return "Right"
    if location == "B":
        return "Left"
    return "NoOp"


def execute(env: Environment, action: Action) -> None:
    """Apply action to the environment and update performance."""
    env.step += 1
    # Every action costs 1 energy unit
    env.performance -= 1

    if action == "Suck":
        loc = env.agent_location
        if env.dirt[loc] == "Dirty":
            env.dirt[loc] = "Clean"
            env.performance += 10  # reward for cleaning
            note = f"Sucked dirt in Room {loc} (+10)"
        else:
            note = f"Sucked in Room {loc} (already clean)"
    elif action == "Right":
        env.agent_location = "B"
        note = "Moved Right (A -> B)"
    elif action == "Left":
        env.agent_location = "A"
        note = "Moved Left (B -> A)"
    else:
        note = "NoOp"

    env.history.append(f"Step {env.step}: {action} - {note}")


def run_simulation(
    initial_dirt: Dict[Location, Status],
    start: Location = "A",
    max_steps: int = 10,
) -> Environment:
    """Run the vacuum agent until both rooms are clean or max_steps."""
    env = Environment(dirt=dict(initial_dirt), agent_location=start)

    print("=" * 50)
    print("=== Vacuum Cleaner Agent Demo ===")
    print("=" * 50)
    print("Agent type : Simple Reflex Agent")
    print("World      : Two rooms (A and B)")
    print("Rules      : Dirty->Suck | A->Right | B->Left")
    print(f"Max steps  : {max_steps}")

    env.print_state("Initial State")

    while env.step < max_steps:
        location, status = env.percept()
        print(f"\n  Percept : location={location}, status={status}")
        action = simple_reflex_agent(location, status)
        print(f"  Action  : {action}")
        execute(env, action)
        env.print_state("After Action")

        if env.is_all_clean():
            # One extra check: if both clean, agent may still move; stop when clean
            # and we have cleaned at least once or rooms started clean.
            print("\n  >> Both rooms are CLEAN. Stopping simulation.")
            break

    print("\n" + "=" * 50)
    print("Simulation Summary")
    print("=" * 50)
    print(f"  Total steps        : {env.step}")
    print(f"  Final performance  : {env.performance}")
    print(f"  Final dirt status  : A={env.dirt['A']}, B={env.dirt['B']}")
    print("\n  Action history:")
    for line in env.history:
        print(f"    {line}")
    print("=" * 50)
    return env


def parse_optional_interactive() -> Dict[Location, Status] | None:
    """Optional interactive setup; returns None to use the default demo."""
    import sys

    if "--interactive" not in sys.argv:
        return None

    print("Interactive setup (enter Clean or Dirty):")
    a = input("  Room A status [Dirty]: ").strip().capitalize() or "Dirty"
    b = input("  Room B status [Dirty]: ").strip().capitalize() or "Dirty"
    if a not in ("Clean", "Dirty"):
        a = "Dirty"
    if b not in ("Clean", "Dirty"):
        b = "Dirty"
    return {"A": a, "B": b}  # type: ignore[return-value]


def main() -> None:
    custom = parse_optional_interactive()
    if custom is None:
        # Default demo: both rooms dirty, agent starts in A - classic lab scenario
        initial = {"A": "Dirty", "B": "Dirty"}
        print("(Default demo - both rooms Dirty, agent starts in A)")
        print("(Re-run with --interactive to choose initial dirt.)\n")
    else:
        initial = custom

    run_simulation(initial, start="A", max_steps=10)


if __name__ == "__main__":
    main()
