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
        output_filename = os.path.splitext(os.path.basename(input_file))[0]
        self.logger.info(f"Separating {input_file} using Demucs")

        os.makedirs(output_dir, exist_ok=True)

        subprocess.run(
            [
                "demucs",
                "--two-stems=drums",
                "--out",
                output_dir,
                "--filename",
                f"{output_filename}_{{stem}}.wav",
                input_file,
            ],
            check=True,
        )

        self.logger.info(f"Separation complete. Files saved to {output_dir}")
