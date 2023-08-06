from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar, cast

from aiogram.fsm.state import State

from better_fsm.mixins import FSMContextMixin

if TYPE_CHECKING:
    from better_fsm.states.state import ExtendedState, NextStateT


StateT = TypeVar("StateT", bound=State)


@dataclass(slots=True, frozen=True)
class ExtendedStateManager(FSMContextMixin):
    async def set(self, new_state: StateT) -> StateT:
        await self.fsm.set_state(new_state)
        return new_state

    def get_next_state(
        self,
        current_state: ExtendedState[Any, NextStateT],
    ) -> NextStateT:
        all_group_states = cast(
            "tuple[NextStateT, ...]",
            current_state.group.__all_states__,
        )
        current_state_index = all_group_states.index(current_state)

        try:
            return all_group_states[current_state_index + 1]
        except IndexError as e:
            msg = f"`{current_state}` is the last state."
            raise ValueError(msg) from e


EXTENDED_STATE_MANAGER = ExtendedStateManager()
