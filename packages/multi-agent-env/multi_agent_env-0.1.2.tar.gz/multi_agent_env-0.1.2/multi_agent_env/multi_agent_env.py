from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Callable


@dataclass
class State:
    """A state in a game environment."""
    pass


@dataclass
class Reward:
    """A reward in a game environment."""
    pass


@dataclass
class Action:
    """An action in a game environment."""
    pass


class Game(ABC):
    """A game environment.

    A game takes agent actions and calculates state transitions and rewards.

    Attributes:
        state: The current state of the game.
        done: Whether the game is done or not.

    Methods:
        start: Start the game.
        step: Take an action and calculate the next state and reward.
        reset: Reset the game to its initial state.
        get_state: Get the current state of the game.
        is_done: Check if the game is done.
    """
    def __init__(self) -> None:
        """Initialize the game."""
        self._state = None
        self._done = None

    @abstractmethod
    def start(self) -> State:
        """Start the game.

        Returns:
            State: The initial state of the game.
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
        """Reset the game to its initial state.

        Returns:
            State: The initial state of the game.
        """
        pass

    @abstractmethod
    def get_state(self) -> State:
        """Get the current state of the game.

        Returns:
            State: The current state of the game.
        """
        pass

    @property
    def state(self) -> State:
        """Get the current state of the game.

        Returns:
            State: The current state of the game.
        """
        self._state = self.get_state()
        return self._state

    @abstractmethod
    def is_done(self) -> bool:
        """Check if the game is done.

        Returns:
            bool: Whether the game is done or not.
        """
        pass

    @property
    def done(self) -> bool:
        """Check if the game is done.

        Returns:
            bool: Whether the game is done or not.
        """
        self.done = self.is_done()
        return self.done

    def main_loop(self, agent: 'Agent',
                  timeout: int = None,
                  on_step: Callable[['Game'], None] = None) -> None:
        """Run the main loop of the game.

        This is not recommended as the game loop should be handled by the
        agent.

        Args:
            agent (Agent): The agent to run the game with.
            timeout (int): The maximum number of steps to take.
            on_step (Callable[[Game], None]): A function called on the game
              after each step.
        """
        state = self.start()
        while timeout is None or timeout > 0:
            agent.step(state)

            if on_step is not None:
                on_step(self)

            if timeout is not None:
                timeout -= 1

            if self.done:
                break


class GameRenderer(ABC):
    """A game renderer.

    A game renderer renders the game environment from a State object."""
    def __init__(self, game: Game) -> None:
        """Initialize the game renderer."""
        self.game = game

    @abstractmethod
    def render(self, state: State) -> None:
        """Render the game state.

        Args:
            state (State): The state to render.
        """
        pass


class Agent(ABC):
    """An agent in a game environment.

    An agent takes actions in a game environment and learns from the rewards.

    Attributes:
        game: The game environment the agent is in.

    Methods:
        policy: Calculate the next action to take.
        train: Train the agent on the reward.
        step: Take an action and train the agent.
        main_loop: Run the agent in the game environment.
    """
    def __init__(self, game: Game) -> None:
        """Initialize the agent.

        Args:
            game (Game): The game environment the agent is in.
        """
        self.game = game

    @abstractmethod
    def policy(self, states: State) -> Action:
        """Calculate the next action to take.

        Args:
            states (State): The current state of the game.

        Returns:
            Action: The next action to take.
        """
        pass

    @abstractmethod
    def train(self, reward: Reward) -> None:
        """Train the agent on the reward.

        Args:
            reward (Reward): The reward from the game.
        """
        pass

    def step(self, state: State) -> State:
        """Take an action and train the agent.

        Args:
            state (State): The current state of the game.
        """
        action = self.policy(state)
        observation, reward = self.game.step(action)
        self.train(reward)
        return observation

    def main_loop(self) -> None:
        """Run the agent in the game environment."""
        state = self.game.start()
        while True:
            state = self.step(state)
            if self.game.is_done():
                break
