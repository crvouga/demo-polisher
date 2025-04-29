import subprocess
import os
from typing import List, Optional
from src.audio_source_separator.inter import AudioSourceSeparator


class DemucsSeparator(AudioSourceSeparator):
    def __init__(self):
        self.default_stems = ["vocals", "drums", "bass", "other"]

    def separate(
        self,
        input_file: str,
        output_dir: str,
        output_filename: str = None,
        stem_names: Optional[List[str]] = None,
    ):
        if output_filename is None:
            output_filename = os.path.splitext(os.path.basename(input_file))[0]

        if stem_names is None:
            stem_names = self.default_stems

        # Demucs supports 4 stems by default
        subprocess.run(
            [
                "demucs",
                "--out",
                output_dir,
                "--filename",
                f"{output_filename}_{{stem}}.wav",
                input_file,
            ]
        )
