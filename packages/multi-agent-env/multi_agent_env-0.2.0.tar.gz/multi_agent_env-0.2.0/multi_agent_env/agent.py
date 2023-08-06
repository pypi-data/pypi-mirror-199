from abc import ABC, abstractmethod

from utils import State, Action, Reward
from env import Env


class Agent(ABC):
    """An agent in a env environment.

    An agent takes actions in an environment and learns from the rewards.

    Attributes:
        Env: The env environment the agent is in.

    Methods:
        policy: Calculate the next action to take.
        train: Train the agent on the reward.
        step: Take an action and train the agent.
        main_loop: Run the agent in the env environment.
    """
    def __init__(self, env: Env) -> None:
        """Initialize the agent.

        Args:
            env (Env): The environment the agent is in.
        """
        self.env = env

    @abstractmethod
    def policy(self, states: State) -> Action:
        """Calculate the next action to take.

        Args:
            states (State): The current state of the environment.

        Returns:
            Action: The next action to take.
        """
        pass

    @abstractmethod
    def train(self, reward: Reward) -> None:
        """Train the agent on the reward.

        Args:
            reward (Reward): The reward from the environment.
        """
        pass

    def step(self, state: State) -> State:
        """Take an action and train the agent.

        Args:
            state (State): The current state of the env.
        """
        action = self.policy(state)
        observation, reward = self.env.step(action)
        self.train(reward)
        return observation

    def main_loop(self) -> None:
        """Run the agent in the environment."""
        state = self.env.start()
        while True:
            state = self.step(state)
            if self.env.is_done():
                break
