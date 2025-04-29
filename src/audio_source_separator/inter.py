from abc import ABC, abstractmethod


class AudioSourceSeparator(ABC):

    @abstractmethod
    def separate(self, input_file: str, output_dir: str):
        """
        Separate an audio file into individual stems.

        Args:
            input_file (str): Path to the input audio file.
            output_dir (str): Path to the output directory where separated stems will be saved.

        Returns:
            None
        """
        pass
