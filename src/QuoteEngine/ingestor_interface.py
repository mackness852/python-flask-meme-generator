from abc import ABC, abstractmethod

from quote_model import QuoteModel


class IngestorInterface(ABC):
    allowed_file_exts = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
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
