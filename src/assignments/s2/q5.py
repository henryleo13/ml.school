"""Assignment 2 Question 5: Metaflow with retry decorator.

This module implements a Metaflow pipeline that demonstrates the use of a retry
decorator for handling flaky external services. The flow modifies an artifact
and prints its history, sum, and average.
"""
import random

import numpy as np
from metaflow import FlowSpec, step, user_step_decorator


class FlakyServiceError(Exception):
    """Custom exception for simulating flaky external service failures."""


def simulate_flaky_service():
    """Simulate a flaky external service that may fail."""
    threshold = 0.5  # 50% chance of failure
    if random.random() < threshold:
        msg = "Simulated failure"
        raise FlakyServiceError(msg)


@user_step_decorator
# Add a @retry decorator to a step in your flow that simulates a flaky external service
def retry(step_name, flow, inputs=None, attributes=None):  # noqa: ARG001
    """Retry a step on failure."""
    max_retries = 3
    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Attempt {attempt + 1} for step: {step_name}")
            # Simulate a flaky external service with 50% chance of failure
            simulate_flaky_service()
            yield  # Proceed with the step execution
            return
        except FlakyServiceError as e:
            print(f"Step {step_name} failed with error: {e}")
            attempt += 1
            if attempt == max_retries:
                print(f"Step {step_name} failed after {max_retries} attempts.")
                raise

class Session2(FlowSpec):
    """A flow that modifies an artifact then prints history, sum and average of artifact."""  # noqa: E501

    @step
    def start(self):
        """Initialize the artifact."""
        self.my_variable = 1
        self.var_list = []
        self.var_list.append(self.my_variable)
        self.next(self.mid1)

    @retry
    @step
    def mid1(self):
        """Increment the variable by 1."""
        self.my_variable += 1
        self.var_list.append(self.my_variable)
        self.next(self.mid2)
    @retry
    @step
    def mid2(self):
        """Decrement the variable by 2."""
        self.my_variable = self.my_variable - 2
        self.var_list.append(self.my_variable)
        self.next(self.end)

    @retry
    @step
    def end(self):
        """Print."""
        print(self.my_variable)
        print(self.var_list)
        print(np.sum(np.array(self.var_list)))
        print(np.mean(np.array(self.var_list)))

if __name__ == "__main__":
    Session2()
