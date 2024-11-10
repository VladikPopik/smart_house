from enum import Enum

from statemachine import State, StateMachine
from statemachine.contrib.diagram import DotGraphMachine
from statemachine.states import States

img_path = "/data/statemanager.png"


class Status(int, Enum):
    planned = 0
    pending = 1
    completed = 2
    error = -1


class StateManager(StateMachine):
    """State machine that controls behaviour of micro-services."""

    state_ = States.from_enum(
        Status, initial=Status.planned, final=Status.error
    )

    move = state_.planned.to(state_.pending)
    complete = state_.pending.to(state_.completed)
    finish = state_.completed.to(state_.error)

    def on_enter_error(self) -> None:
        print(f"error occured")


sm = StateManager()
graph = DotGraphMachine(sm)
graph().write("statemanager.jpg", format="jpg")
