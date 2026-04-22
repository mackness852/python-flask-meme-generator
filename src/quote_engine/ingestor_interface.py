from abc import ABC, abstractmethod

from .quote_model import QuoteModel


class IngestorInterface(ABC):
    """Ingestor interface for concrete implementations. Provides a
    class method to check if file type supported.
    """

    allowed_file_exts = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if concrete implementations can parse that file by
        stripping the file ext and checking.

        Args:
            path (str): filepath

        Returns:
            bool: True if it can parse a given path
        """
        file = path.split(".")[-1]

        for ext in cls.allowed_file_exts:
            if ext == file:
                return True
        else:
            return False

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        pass
