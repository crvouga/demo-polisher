import logging
from typing import Dict, Type, Literal, Union
from src.audio_source_separator.inter import AudioSourceSeparator
from src.audio_source_separator.impl_spleeter import SpleeterSeparator
from src.audio_source_separator.impl_demucs import DemucsSeparator


class AudioSourceSeparatorFactory:
    _separators: Dict[str, Type[AudioSourceSeparator]] = {
        "spleeter": SpleeterSeparator,
        "demucs": DemucsSeparator,
    }

    @classmethod
    def create(
        cls,
        impl: Union[Literal["spleeter"], Literal["demucs"]],
        logger: logging.Logger,
    ) -> AudioSourceSeparator:
        """
        Create an instance of the specified audio source separator.

        Args:
            separator_type (Literal["spleeter", "demucs"]): The type of separator to create ('spleeter' or 'demucs')

        Returns:
            AudioSourceSeparator: An instance of the requested separator

        Raises:
            ValueError: If the separator type is not supported
        """
        if impl not in cls._separators:
            raise ValueError(
                f"Unsupported separator type: {impl}. "
                f"Supported types are: {', '.join(cls._separators.keys())}"
            )

        return cls._separators[impl](logger)
