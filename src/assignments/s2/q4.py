import numpy as np
from metaflow import FlowSpec, Parameter, step

class Session2(FlowSpec):
    """A flow that takes a list as a parameter, squares each element,
    and prints the sum and the original list.
    """  # noqa: D205

    number_list = Parameter("numbers", help = "List of numbers", default = [1,2,3,4,5])

    @step
    def start(self):
        """Print the list."""
        print("Original list:", self.number_list)
        self.next(self.square_and_sum, foreach="number_list")

    @step
    def square_and_sum(self):
        """Square each number and compute the sum."""
        number = self.input or 0
        self.squared = number ** 2
        print(f"Squared {number} to get {self.squared}")
        self.next(self.join)

    @step
    def join(self, inputs):
        """Join the results and print the total sum of squares."""
        self.squared_values = [i.squared for i in inputs]
        self.total_sum = np.sum(np.array(self.squared_values))
        self.next(self.end)

    @step
    def end(self):
        """Print the total sum of squares."""
        print("Total sum of squares:", self.total_sum)

if __name__ == "__main__":
    Session2()


