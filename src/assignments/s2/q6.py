"""Design a custom card that goes beyond static HTML and integrates some data
visualization.

Implement a flow that generates a random dataset and use the @card decorator to
show charts or tables related to the data.
"""  # noqa: D205

import random

import matplotlib.pyplot as plt
import pandas as pd
from metaflow import FlowSpec, card, step, current
from metaflow.cards import Image, Table, Markdown
from io import BytesIO


class DataVisualizationFlow(FlowSpec):
    """A flow that generates random data and visualizes it using custom cards."""

    @card
    @step
    def start(self):
        """Generate a random dataset."""
        self.data = [random.randint(1, 100) for _ in range(10)]
        self.next(self.visualize)

    @card(type="blank")
    @step
    def visualize(self):
        """Visualize the dataset with a histogram and a table."""
         # ---- Create histogram directly in memory ----
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(self.data, bins=10, color="#3A7CA5", alpha=0.8, edgecolor="white")
        ax.set_title("Random Data Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.grid(visible=True, linestyle="--", alpha=0.5)()

        # ---- Prepare table data ----
        df = pd.DataFrame({"Index": range(len(self.data)), "Value": self.data})

        # ---- Attach visualizations to card ----
        current.card.append(Markdown("# See Visualizations Below\n ## Histogram of Random Data"))
        current.card.append(Image.from_matplotlib(fig, label ="Histogram of Random Data"))
        current.card.append(Markdown("## Data Table"))
        current.card.append(Table.from_dataframe(df))


        self.next(self.end)

    @card
    @step
    def end(self):
        """End of the flow."""
        print("Flow completed successfully.")

if __name__ == "__main__":
    DataVisualizationFlow()
