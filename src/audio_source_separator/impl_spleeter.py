import subprocess
import os
import logging
from typing import List, Optional
from src.audio_source_separator.inter import AudioSourceSeparator


class SpleeterSeparator(AudioSourceSeparator):
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.default_stems = ["vocals", "drums", "bass", "other"]
        self.logger = logger or logging.getLogger(__name__)

    def separate(self, input_file: str, output_dir: str):
        # Ensure input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get the absolute paths to ensure proper handling
        abs_input = os.path.abspath(input_file)
        abs_output = os.path.abspath(output_dir)

        self.logger.info(f"Separating {abs_input} using Spleeter")

        try:
            subprocess.run(
                ["spleeter", "separate", "-p", "4stems", "-o", abs_output, abs_input],
                check=True,
                capture_output=True,
                text=True,
            )
            self.logger.info(f"Separation complete. Files saved to {abs_output}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Spleeter separation failed: {e.stderr}")
            raise
