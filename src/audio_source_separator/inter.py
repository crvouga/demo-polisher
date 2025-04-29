from abc import ABC, abstractmethod
from typing import List, Optional


class AudioSourceSeparator(ABC):

    @abstractmethod
    def separate(
        self,
        input_file: str,
        output_dir: str,
        output_filename: str = None,
        stem_names: Optional[List[str]] = None,
    ):
        """
        Separate an audio file into individual stems.

        Args:
            input_file (str): Path to the input audio file.
            output_dir (str): Path to the output directory where separated stems will be saved.
            output_filename (str, optional): Base name for output files. If None, uses input file name.
            stem_names (List[str], optional): List of specific stem names to separate. If None, uses default stems.

        Returns:
            None
        """
        pass
