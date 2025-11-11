"""Create a flow that compares the use of the @environment decorator with accessing
environment variables using the python-dotenv library to load environment variables
from a .env file.

This flow demonstrates two different approaches to environment variable management
in Metaflow workflows.
"""  # noqa: D205

import os

from dotenv import load_dotenv
from metaflow import FlowSpec, environment, step


class Environment(FlowSpec):
    """A flow that compares environment decorator with accessing environment variables
    using the python-dotenv library.

    This flow shows the differences between Metaflow's @environment decorator
    and manual environment variable loading with python-dotenv.
    """  # noqa: D205

    @step
    def start(self):
        """Initialize the flow and set up test environment variables."""
        print("Starting environment variable comparison flow")

        # Set some test environment variables for demonstration
        os.environ["TEST_VAR"] = "from_os_environ"
        os.environ["SHARED_VAR"] = "available_to_both"

        self.next(self.dotenv_approach, self.metaflow_approach)

    @step
    def dotenv_approach(self):
        """Demonstrate using python-dotenv to load environment variables."""
        print("\n=== Python-dotenv Approach ===")

        # Load environment variables from .env file
        load_dotenv()

        # Access variables
        test_var = os.getenv("TEST_VAR", "not_found")
        shared_var = os.getenv("SHARED_VAR", "not_found")
        dotenv_var = os.getenv("DOTENV_SPECIFIC", "not_found")

        print(f"TEST_VAR: {test_var}")
        print(f"SHARED_VAR: {shared_var}")
        print(f"DOTENV_SPECIFIC: {dotenv_var}")

        self.dotenv_results = {
            "approach": "python-dotenv",
            "test_var": test_var,
            "shared_var": shared_var,
            "dotenv_var": dotenv_var
        }

        self.next(self.compare_results)

    @environment(
        vars={
            "TEST_VAR": "from_metaflow_decorator",
            "METAFLOW_SPECIFIC": "metaflow_only"
        }
    )
    @step
    def metaflow_approach(self):
        """Demonstrate using Metaflow's @environment decorator."""
        print("\n=== Metaflow @environment Approach ===")

        # Access variables set by the decorator and existing ones
        test_var = os.getenv("TEST_VAR", "not_found")
        shared_var = os.getenv("SHARED_VAR", "not_found")
        metaflow_var = os.getenv("METAFLOW_SPECIFIC", "not_found")

        print(f"TEST_VAR: {test_var}")
        print(f"SHARED_VAR: {shared_var}")
        print(f"METAFLOW_SPECIFIC: {metaflow_var}")

        self.metaflow_results = {
            "approach": "metaflow @environment",
            "test_var": test_var,
            "shared_var": shared_var,
            "metaflow_var": metaflow_var
        }

        self.next(self.compare_results)

    @step
    def compare_results(self, inputs):
        """Compare the results from both approaches."""
        print("\n=== Comparison Results ===")

        # Merge results from both branches
        self.dotenv_results = inputs.dotenv_approach.dotenv_results
        self.metaflow_results = inputs.metaflow_approach.metaflow_results

        print(f"Dotenv results: {self.dotenv_results}")
        print(f"Metaflow results: {self.metaflow_results}")

        print("\n=== Key Differences ===")
        print("1. @environment decorator sets variables at step level")
        print("2. python-dotenv loads variables from .env file globally")
        print("3. @environment can override existing environment variables")
        print("4. python-dotenv preserves existing environment variables")

        self.next(self.end)

    @step
    def end(self):
        """End the flow with summary."""
        print("\n=== Summary ===")
        print("Both approaches have their use cases:")
        print("- Use @environment for step-specific variable requirements")
        print("- Use python-dotenv for configuration management across the application")
        print("Flow completed successfully!")

if __name__ == "__main__":
    Environment()
