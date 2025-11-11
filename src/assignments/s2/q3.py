from metaflow import FlowSpec, step


class Session2(FlowSpec):
    """A flow showing parallel steps modifying an artifact."""

    @step
    def start(self):
        """Initialize the variable."""
        self.my_variable = 0
        self.next(self.branch1, self.branch2)

    @step
    def branch1(self):
        """Increment the variable by 5."""
        self.my_variable += 5
        self.next(self.join)

    @step
    def branch2(self):
        """Multiply the variable by 10."""
        self.my_variable *= 10
        self.next(self.join)

    @step
    def join(self, inputs):
        """Join the branches and print the final value."""
        # Combine the results from both branches
        print(f"Value from branch1: {inputs.branch1.my_variable}")
        print(f"Value from branch2: {inputs.branch2.my_variable}")
        self.merge_artifacts(inputs, exclude = ["my_variable"])
        self.final_value = sum(i.my_variable for i in inputs)
        self.next(self.end)

    @step
    def end(self):
        """Print the final artifact value."""
        print("Final value after joining branches:", self.final_value)

if __name__ == "__main__":
    Session2()
