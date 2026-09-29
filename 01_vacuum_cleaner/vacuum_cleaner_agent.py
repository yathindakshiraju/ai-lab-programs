# Name: yathindakshiraju
# Email: yathindakshiraju.cs24@bmsce.ac.in
# Subject: AI Laboratory
# Program 1: Vacuum Cleaner Agent (Simple Reflex)

# Two rooms A and B. Agent sucks if dirty, otherwise moves to the other room.
# Score: +10 when dirt is cleaned, -1 for each action.


def agent(location, status):
    if status == "Dirty":
        return "Suck"
    if location == "A":
        return "Right"
    return "Left"


def print_rooms(rooms, location, step, score):
    print(f"\nStep {step}")
    print(f"  Room A: {rooms['A']}" + ("  <-- agent" if location == "A" else ""))
    print(f"  Room B: {rooms['B']}" + ("  <-- agent" if location == "B" else ""))
    print(f"  Score: {score}")


def run(rooms, start="A", max_steps=10):
    location = start
    score = 0
    history = []

    print("Vacuum Cleaner Agent")
    print("Simple reflex agent - two rooms A and B")
    print_rooms(rooms, location, 0, score)

    for step in range(1, max_steps + 1):
        status = rooms[location]
        action = agent(location, status)
        print(f"\nPercept: location={location}, status={status}")
        print(f"Action: {action}")

        score -= 1

        if action == "Suck":
            if rooms[location] == "Dirty":
                rooms[location] = "Clean"
                score += 10
                history.append(f"Step {step}: Suck in {location} (+10)")
            else:
                history.append(f"Step {step}: Suck in {location} (already clean)")
        elif action == "Right":
            location = "B"
            history.append(f"Step {step}: Move Right")
        elif action == "Left":
            location = "A"
            history.append(f"Step {step}: Move Left")

        print_rooms(rooms, location, step, score)

        if rooms["A"] == "Clean" and rooms["B"] == "Clean":
            print("\nBoth rooms clean. Done.")
            break

    print("\nSummary")
    print(f"  Steps: {step}")
    print(f"  Final score: {score}")
    print(f"  A={rooms['A']}, B={rooms['B']}")
    print("  History:")
    for h in history:
        print(f"    {h}")


if __name__ == "__main__":
    # both rooms dirty, agent starts in A
    initial = {"A": "Dirty", "B": "Dirty"}
    run(initial)
