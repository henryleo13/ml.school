"""Create a flow that includes an external CSV file using the IncludeFile function.

In a processing step, parse the file and print the number of rows and columns.
Add error handling to check for issues such as an empty file or malformed content,
and print an appropriate error message if the file cannot be processed.
"""

import csv

from metaflow import FlowSpec, IncludeFile, step


class Files(FlowSpec):
    """A flow that includes an external CSV file."""

    file = IncludeFile(
        "file",
        is_text=True,
        help="Sample comma-separated file"
    )

    @step
    def start(self):
        """Parse CSV and print its shape."""
        try:
            rows = list(csv.reader(self.file.splitlines()))
            if not rows:
                msg = "File is empty."
                raise ValueError(msg)  # noqa: TRY301
            print(f"Rows: {len(rows)-1}, Columns: {len(rows[0])}")
        except Exception as e:
            print(f"Error processing file: {e}")
        self.next(self.end)

    @step
    def end(self):
        print("Done.")

if __name__ == "__main__":
    Files()
