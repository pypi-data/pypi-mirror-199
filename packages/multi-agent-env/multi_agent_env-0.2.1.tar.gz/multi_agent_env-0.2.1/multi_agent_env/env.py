from abc import ABC, abstractmethod
from typing import Tuple

from utils import State, Action, Reward


class Env(ABC):
    """An environment.

    An environment takes agent actions and calculates
    state transitions and rewards.

    Attributes:
        state: The current state of the environment.
        done: Whether the environment is done or not.

    Methods:
        start: Start the environment.
        step: Take an action and calculate the next state and reward.
        reset: Reset the environment to its initial state.
        get_state: Get the current state of the environment.
        is_done: Check if the environment is done.
    """
    def __init__(self) -> None:
        """Initialize the environment."""
        self._state = None
        self._done = None

    @abstractmethod
    def start(self) -> State:
        """Start the environment.

        Returns:
            State: The initial state of the environment.
        """
        pass

    @abstractmethod
    def step(self, action: Action) -> Tuple[State, Reward]:
        """Take an action and return the next state and reward.

        Calculate the state transition and reward for the given action.

        Args:
            action (Action): The action to take.

        Returns:
            Tuple[State, Reward]: The next state and reward.
        """
        pass

    @abstractmethod
    def reset(self) -> State:
        """Reset the environment to its initial state.

        Returns:
            State: The initial state of the environment.
        """
        pass

    @abstractmethod
    def get_state(self) -> State:
        """Get the current state of the environment.

        Returns:
            State: The current state of the environment.
        """
        pass

    @property
    def state(self) -> State:
        """Get the current state of the environment.

        Returns:
            State: The current state of the environment.
        """
        self._state = self.get_state()
        return self._state

    @abstractmethod
    def is_done(self) -> bool:
        """Check if the environment is done.

        Returns:
            bool: Whether the environment is done or not.
        """
        pass

    @property
    def done(self) -> bool:
        """Check if the environment is done.

        Returns:
            bool: Whether the environment is done or not.
        """
        self.done = self.is_done()
        return self.done
