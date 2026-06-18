from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

import streamlit as st

from vla_embodied_agent_simulator import GridWorldEnv, plan_from_instruction

st.set_page_config(page_title="VLA Embodied Agent Simulator", page_icon="AI", layout="wide")
st.title("VLA-Inspired Embodied Agent Simulator")
st.caption("Simulation only: maps language and grid-world state into safe action sequences.")

instruction = st.text_input("Instruction", "Pick up the red object and move it to the blue zone.")
env = GridWorldEnv()
plan = plan_from_instruction(instruction, env)
trace = []
done = False
for action in plan:
    state, reward, done, info = env.step(action)
    trace.append({"action": action, "reward": reward, "done": done, "info": info, "state": state})
    if done:
        break

st.subheader("Plan")
st.write(plan)
st.subheader("Rendered environment")
st.code(env.render_text())
st.subheader("Episode trace")
st.json(trace)
