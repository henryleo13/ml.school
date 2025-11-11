"""Metaflow pipeline for Session 2 assignment.

This module implements a Metaflow pipeline that demonstrates artifact modification
and tracking through multiple steps, calculating history, sum and average values.
"""

import numpy as np
from metaflow import FlowSpec, step


class Session2(FlowSpec):
    """A flow that modifies an artifact then prints history, sum and average of artifact."""

    @step
    def start(self):
        self.my_variable = 1
        self.var_list = []
        self.var_list.append(self.my_variable)
        self.next(self.mid1)

    @step
    def mid1(self):
        """Increment the variable by 1."""
        self.my_variable += 1
        self.var_list.append(self.my_variable)
        self.next(self.mid2)

    @step
    def mid2(self):
        """Decrement the variable by 2."""
        self.my_variable = self.my_variable - 2
        self.var_list.append(self.my_variable)
        self.next(self.end)

    @step
    def end(self):
        """Print."""
        print(self.my_variable)
        print(self.var_list)
        print(np.sum(np.array(self.var_list)))
        print(np.mean(np.array(self.var_list)))

if __name__ == "__main__":
    Session2()
