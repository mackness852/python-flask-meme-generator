from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class TxtIngestor(IngestorInterface):
    """The .txt file ingestor"""

    allowed_file_exts = ["txt"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parses a txt file path into a list of QuoteModel

        Args:
            path (str): filepath

        Returns:
            list[QuoteModel]: List of parsed QuoteModels
        """

        quotes = []

        with open(path) as infile:
            for line in infile:
                splitted = line.split(" - ")
                quotes.append(
                    QuoteModel(splitted[0].strip(), splitted[1].strip())
                )

        return quotes
