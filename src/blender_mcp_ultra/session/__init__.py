"""Session management — goal-first routing, stateful sessions, tool visibility."""

import time
import logging
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger("blender_mcp_ultra.session")


class SessionPhase(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    BUILDING = "building"
    INSPECTING = "inspecting"
    FINISHING = "finishing"


@dataclass
class SessionGoal:
    """Tracks the current session goal and progress."""
    goal: str = ""
    phase: SessionPhase = SessionPhase.IDLE
    steps_completed: list[str] = field(default_factory=list)
    steps_remaining: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    error_count: int = 0
    screenshot_count: int = 0

    def touch(self):
        self.last_activity = time.time()

    @property
    def is_stale(self) -> bool:
        return (time.time() - self.last_activity) > 600  # 10 minutes

    def advance_phase(self):
        order = [SessionPhase.PLANNING, SessionPhase.BUILDING, SessionPhase.INSPECTING, SessionPhase.FINISHING]
        idx = order.index(self.phase) if self.phase in order else 0
        if idx < len(order) - 1:
            self.phase = order[idx + 1]

    def complete_step(self, step: str):
        if step in self.steps_remaining:
            self.steps_remaining.remove(step)
        self.steps_completed.append(step)
        self.touch()

    def to_dict(self) -> dict:
        return {
            "goal": self.goal,
            "phase": self.phase.value,
            "steps_completed": self.steps_completed,
            "steps_remaining": self.steps_remaining,
            "age_seconds": int(time.time() - self.created_at),
            "error_count": self.error_count,
            "screenshot_count": self.screenshot_count,
        }


class SessionManager:
    """Manages stateful sessions for goal-first workflows."""

    def __init__(self):
        self._sessions: dict[str, SessionGoal] = {}

    def get_or_create(self, session_id: str = "default") -> SessionGoal:
        if session_id not in self._sessions or self._sessions[session_id].is_stale:
            self._sessions[session_id] = SessionGoal()
        return self._sessions[session_id]

    def set_goal(self, goal: str, session_id: str = "default") -> dict:
        session = self.get_or_create(session_id)
        session.goal = goal
        session.phase = SessionPhase.PLANNING
        session.steps_completed = []
        session.steps_remaining = ["plan", "build", "inspect", "finish"]
        session.created_at = time.time()
        session.touch()

        logger.info("Session goal set: %s", goal)
        return {
            "status": "goal_set",
            "goal": goal,
            "phase": session.phase.value,
            "next_steps": session.steps_remaining,
            "message": (
                f"Goal registered: {goal}. "
                "I'll plan the approach, build the scene, verify quality, and finalize. "
                "Use get_viewport_screenshot and analyze_mesh_quality at milestones."
            ),
        }

    def get_status(self, session_id: str = "default") -> dict:
        session = self.get_or_create(session_id)
        return session.to_dict()

    def advance(self, session_id: str = "default") -> dict:
        session = self.get_or_create(session_id)
        session.advance_phase()
        session.touch()
        return {
            "phase": session.phase.value,
            "steps_completed": session.steps_completed,
            "steps_remaining": session.steps_remaining,
        }

    def record_error(self, session_id: str = "default"):
        session = self.get_or_create(session_id)
        session.error_count += 1
        session.touch()

    def record_screenshot(self, session_id: str = "default"):
        session = self.get_or_create(session_id)
        session.screenshot_count += 1
        session.touch()


_session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    return _session_manager
