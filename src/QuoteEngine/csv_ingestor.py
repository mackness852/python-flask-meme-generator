import pandas as pd
from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class CsvIngestor(IngestorInterface):
    """The .csv file ingestor"""

    allowed_file_exts = ["csv"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parses a csv file path into a list of QuoteModel

        Args:
            path (str): filepath

        Returns:
            list[QuoteModel]: List of parsed QuoteModels
        """

        quotes = []

        with open(path) as infile:
            data = pd.read_csv(infile)

            for _, row in data.iterrows():
                quotes.append(
                    QuoteModel(row["body"].strip(), row["author"].strip())
                )

        return quotes
