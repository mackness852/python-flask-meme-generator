import pandas as pd
from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class CsvIngestor(IngestorInterface):
    allowed_file_exts = ["csv"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:

        quotes = []

        with open(path) as infile:
            data = pd.read_csv(infile)

            for _, row in data.iterrows():
                quotes.append(
                    QuoteModel(row["body"].strip(), row["author"].strip())
                )

        return quotes
