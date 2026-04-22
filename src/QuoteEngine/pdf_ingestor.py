import subprocess

from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class PdfIngestor(IngestorInterface):
    allowed_file_exts = ["pdf"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:

        quotes = []

        text = subprocess.run(
            ["pdftotext", path, "-"], capture_output=True, text=True
        )
        for line in text.stdout.splitlines():
            if line and line != "":
                splitted = line.split(" - ")
                quotes.append(
                    QuoteModel(splitted[0].strip(), splitted[1].strip())
                )

        return quotes
