"""Create a flow that loads a JSON configuration file using the Config object.

Use Parameter objects as part of the flow to override some of the configuration values
at runtime. Demonstrate how the flow behaves differently based on the configuration
and parameter inputs.

Usage Examples:
1. Default configuration from JSON file:
    uv run src/assignments/s2/q10.py run
2. Override value1 and value2 parameters:
    uv run src/assignments/s2/q10.py run --value1 100 --value2 200
3. Override settingA and settingB parameters:
    uv run src/assignments/s2/q10.py run --setting-a "custom_mode" --setting-b "json_format"
4. Override all parameters:
    uv run src/assignments/s2/q10.py run --value1 50 --value2 75 --setting-a "advanced" --setting-b "csv_output"
5. Use a different configuration file:
    uv run src/assignments/s2/q10.py run --config path/to/other/config.json
"""  # noqa: E501

from metaflow import Config, FlowSpec, Parameter, step


class ConfigFlow(FlowSpec):
    """A flow that demonstrates Config and Parameter usage."""

    # Load configuration from JSON file
    config = Config("config", default="src/assignments/data/s2_config.json")

    # Parameters to override config values at runtime
    value1 = Parameter(
        "value1",
        help="Override value1 from config",
        type=int,
        default=None,
    )

    value2 = Parameter(
        "value2",
        help="Override value2 from config",
        type=int,
        default=None,
    )

    setting_a = Parameter(
        "setting-a",
        help="Override settingA from config",
        default=None,
    )

    setting_b = Parameter(
        "setting-b",
        help="Override settingB from config",
        default=None,
    )

    @step
    def start(self):
        """Load configuration and apply parameter overrides."""
        print("\n" + "=" * 60)
        print("CONFIGURATION LOADING")
        print("=" * 60)

        # Load config values
        config_data = self.config

        print(f"\n📁 Loaded configuration from: {self.config}")
        print(f"Config contents: {config_data}")

        # Apply parameter overrides or use config defaults
        self.final_value1 = (
            self.value1 if self.value1 is not None else config_data["value1"]
        )
        self.final_value2 = (
            self.value2 if self.value2 is not None else config_data["value2"]
        )
        self.final_setting_a = (
            self.setting_a
            if self.setting_a is not None
            else config_data["settingA"]
        )
        self.final_setting_b = (
            self.setting_b
            if self.setting_b is not None
            else config_data["settingB"]
        )

        print("\n" + "=" * 60)
        print("FINAL VALUES (after parameter overrides)")
        print("=" * 60)
        print(f"value1: {self.final_value1} {'(OVERRIDDEN)' if self.value1 is not None else '(from config)'}")
        print(f"value2: {self.final_value2} {'(OVERRIDDEN)' if self.value2 is not None else '(from config)'}")
        print(f"settingA: {self.final_setting_a} {'(OVERRIDDEN)' if self.setting_a is not None else '(from config)'}")
        print(f"settingB: {self.final_setting_b} {'(OVERRIDDEN)' if self.setting_b is not None else '(from config)'}")

        self.next(self.process)

    @step
    def process(self):
        """Process data based on configuration and parameters."""
        print("\n" + "=" * 60)
        print("PROCESSING")
        print("=" * 60)

        # Demonstrate different behavior based on configuration
        result = self.final_value1 + self.final_value2
        print(f"\n🔢 Mathematical operation: {self.final_value1} + {self.final_value2} = {result}")

        # Demonstrate behavior based on settings
        if self.final_setting_a == "defaultA":
            print(f"\n⚙️  Using default behavior for settingA: {self.final_setting_a}")
            self.behavior_a = "Standard processing mode"
        else:
            print(f"\n⚙️  Using custom behavior for settingA: {self.final_setting_a}")
            self.behavior_a = f"Custom processing with {self.final_setting_a}"

        if self.final_setting_b == "defaultB":
            print(f"⚙️  Using default behavior for settingB: {self.final_setting_b}")
            self.behavior_b = "Standard output format"
        else:
            print(f"⚙️  Using custom behavior for settingB: {self.final_setting_b}")
            self.behavior_b = f"Custom output with {self.final_setting_b}"

        # Store result
        self.result = result

        self.next(self.end)

    @step
    def end(self):
        """Display final results."""
        print("\n" + "=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        print(f"\n✅ Final Result: {self.result}")
        print(f"📋 Behavior A: {self.behavior_a}")
        print(f"📋 Behavior B: {self.behavior_b}")
        print("\n" + "=" * 60)
        print("FLOW COMPLETED SUCCESSFULLY")
        print("=" * 60)


if __name__ == "__main__":
    ConfigFlow()

