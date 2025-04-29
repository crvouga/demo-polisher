import subprocess
import os
import logging
from typing import List, Optional
from src.audio_source_separator.inter import AudioSourceSeparator


class SpleeterSeparator(AudioSourceSeparator):
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.default_stems = ["vocals", "drums", "bass", "other"]
        self.logger = logger or logging.getLogger(__name__)

    def separate(
        self,
        input_file: str,
        output_dir: str,
        output_filename: Optional[str] = None,
        stem_names: Optional[List[str]] = None,
    ):
        if output_filename is None:
            output_filename = os.path.splitext(os.path.basename(input_file))[0]

        if stem_names is None:
            stem_names = self.default_stems

        # Determine the Spleeter model based on number of stems
        num_stems = len(stem_names)
        if num_stems == 2:
            model = "2stems"
        elif num_stems == 4:
            model = "4stems"
        elif num_stems == 5:
            model = "5stems"
        else:
            model = "4stems"  # Default to 4 stems if not standard configuration

        self.logger.info(f"Separating {input_file} using Spleeter with {model} model")

        os.makedirs(output_dir, exist_ok=True)

        subprocess.run(
            ["spleeter", "separate", "-p", model, "-o", output_dir, input_file],
            check=True,
        )

        # Spleeter creates a subdirectory with the input filename
        # We may need to rename files to match expected format
        input_basename = os.path.splitext(os.path.basename(input_file))[0]
        spleeter_output_dir = os.path.join(output_dir, input_basename)

        self.logger.info(f"Separation complete. Files saved to {spleeter_output_dir}")
