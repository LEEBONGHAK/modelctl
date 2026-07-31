import subprocess


class ClaudeLauncher:
    name = "claude"

    def run(
        self,
        model,
    ):

        subprocess.run(
            [
                "claude",
                "--model",
                model,
            ]
        )
