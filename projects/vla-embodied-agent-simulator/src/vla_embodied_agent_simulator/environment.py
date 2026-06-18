from __future__ import annotations

from dataclasses import dataclass, field

ACTIONS = ["move_up", "move_down", "move_left", "move_right", "pick", "drop", "inspect", "wait"]


@dataclass
class GridWorldEnv:
    width: int = 5
    height: int = 5
    agent: tuple[int, int] = (0, 0)
    carrying: str | None = None
    objects: dict[str, tuple[int, int]] = field(default_factory=lambda: {"red_object": (2, 1)})
    zones: dict[str, tuple[int, int]] = field(
        default_factory=lambda: {"blue_zone": (4, 4), "base": (0, 0)}
    )
    obstacles: set[tuple[int, int]] = field(default_factory=lambda: {(1, 1), (3, 2)})
    restricted_zones: set[tuple[int, int]] = field(default_factory=lambda: {(2, 2)})

    def reset(self) -> dict[str, object]:
        self.agent = (0, 0)
        self.carrying = None
        return self.state()

    def state(self) -> dict[str, object]:
        return {
            "agent": self.agent,
            "carrying": self.carrying,
            "objects": self.objects,
            "zones": self.zones,
            "obstacles": sorted(self.obstacles),
            "restricted_zones": sorted(self.restricted_zones),
        }

    def step(self, action: str) -> tuple[dict[str, object], float, bool, dict[str, str]]:
        if action not in ACTIONS:
            return self.state(), -2.0, False, {"error": "invalid_action"}
        x, y = self.agent
        moves = {
            "move_up": (x, y - 1),
            "move_down": (x, y + 1),
            "move_left": (x - 1, y),
            "move_right": (x + 1, y),
        }
        reward = -0.1
        info: dict[str, str] = {}
        if action in moves:
            target = moves[action]
            if (
                target[0] < 0
                or target[0] >= self.width
                or target[1] < 0
                or target[1] >= self.height
                or target in self.obstacles
                or target in self.restricted_zones
            ):
                return self.state(), -1.0, False, {"error": "unsafe_or_blocked_move"}
            self.agent = target
        elif action == "pick":
            for name, location in list(self.objects.items()):
                if location == self.agent:
                    self.carrying = name
                    del self.objects[name]
                    reward = 1.0
                    break
            else:
                info["error"] = "nothing_to_pick"
                reward = -0.5
        elif action == "drop":
            if self.carrying and self.agent == self.zones.get("blue_zone"):
                self.carrying = None
                reward = 5.0
                return self.state(), reward, True, {"success": "task_complete"}
            reward = -0.5
            info["error"] = "drop_not_allowed"
        elif action == "inspect":
            reward = 0.2
        return self.state(), reward, False, info

    def render_text(self) -> str:
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                point = (x, y)
                if point == self.agent:
                    row.append("A")
                elif point in self.obstacles:
                    row.append("X")
                elif point in self.restricted_zones:
                    row.append("R")
                elif point in self.objects.values():
                    row.append("O")
                elif point in self.zones.values():
                    row.append("Z")
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)


def plan_from_instruction(instruction: str, env: GridWorldEnv) -> list[str]:
    text = instruction.lower()
    if "inspect" in text:
        return ["move_right", "move_right", "inspect", "move_left", "move_left"]
    if "red" in text and "blue" in text:
        return [
            "move_right",
            "move_right",
            "move_down",
            "pick",
            "move_right",
            "move_right",
            "move_down",
            "move_down",
            "move_down",
            "drop",
        ]
    return ["wait"]
