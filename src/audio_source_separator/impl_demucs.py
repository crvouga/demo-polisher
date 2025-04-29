import logging
import subprocess
import os
from typing import List
from src.audio_source_separator.inter import AudioSourceSeparator


class DemucsSeparator(AudioSourceSeparator):
    def __init__(self, logger: logging.Logger):
        self.default_stems = ["drums", "other"]
        self.logger = logger

    def separate(self, input_file: str, output_dir: str):
        # Ensure input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get the absolute paths to ensure proper handling
        abs_input = os.path.abspath(input_file)
        abs_output = os.path.abspath(output_dir)

        self.logger.info(f"Separating {abs_input} using Demucs")

        try:
            subprocess.run(
                [
                    "demucs",
                    "--two-stems=drums",
                    "--out",
                    abs_output,
                    "--filename",
                    "{stem}.wav",
                    abs_input,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.logger.info(f"Separation complete. Files saved to {abs_output}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Demucs separation failed: {e.stderr}")
            raise
