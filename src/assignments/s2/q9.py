"""Write a flow that takes a text prompt and uses an LLM to generate a short response.

Store the response as an artifact and create a custom card that visualizes
the prompt/response pair nicely in a styled format.
"""

import os

import anthropic
from dotenv import load_dotenv
from metaflow import FlowSpec, Parameter, card, current, step
from metaflow.cards import Markdown

load_dotenv()

LLM_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def call_anthropic(prompt: str) -> str:
    """Call Anthropic API."""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except ImportError:
        print("Anthropic library not installed. Install with: pip install anthropic")
        return None
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return None


class LLMResponseFlow(FlowSpec):
    """A flow that generates a response from an LLM based on a text prompt."""

    prompt = Parameter(
        "prompt",
        help="The text prompt to send to the LLM",
        default="What is the capital of France?",
    )

    @step
    def start(self):
        """Generate a response from the LLM."""
        self.response = call_anthropic(self.prompt)
        self.next(self.end)

    @card(type="blank")
    @step
    def end(self):
        """End of the flow and create a card with the prompt/response."""
        card_content = f"""
        # LLM Response

        **Prompt:**
        {self.prompt}

        **Response:**
        {self.response}
        """
        current.card.append(Markdown(card_content))
        print("Flow completed successfully.")

if __name__ == "__main__":
    LLMResponseFlow()
