import subprocess

from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class PdfIngestor(IngestorInterface):
    """The .pdf file ingestor."""

    allowed_file_exts = ["pdf"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parses a pdf file path into a list of QuoteModel. Note, we
        are not parsing a PDF and writing to a temporary .txt file, we
        are simply capturing the contents into std.out and calling
        splitlines to get each line of text.

        Args:
            path (str): filepath

        Returns:
            list[QuoteModel]: List of parsed QuoteModels
        """
        quotes = []

        try:
            text = subprocess.run(
                ["pdftotext", path, "-"], capture_output=True, text=True
            )  # No temp file required, instead we capture stdout as text
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
        except Exception as e:
            print(f"Cannot parse pdf file {path}: {e}")

        for line in text.stdout.splitlines():
            if line and line != "":
                splitted = line.split(" - ")
                quotes.append(
                    QuoteModel(splitted[0].strip(), splitted[1].strip())
                )

        return quotes
