from abc import ABC, abstractmethod

from utils import State
from env import Env


class Renderer(ABC):
    """An environment renderer.

    A renderer renders the environment from a State object.

    Attributes:
        env (Env): The environment to render.

    Methods:
        render: Render the environment state.
    """
    def __init__(self, env: Env) -> None:
        """Initialize the environment renderer.

        Args:
            env (Env): The environment to render.
        """
        self.env = env

    @abstractmethod
    def render(self, state: State) -> None:
        """Render the environment state.

        Args:
            state (State): The state to render.
        """
        pass
