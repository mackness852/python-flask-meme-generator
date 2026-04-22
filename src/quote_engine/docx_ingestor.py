from docx import Document
from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """The .docx file ingestor."""

    allowed_file_exts = ["docx"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parses a docx file path into a list of QuoteModel.

        Args:
            path (str): filepath

        Returns:
            list[QuoteModel]: List of parsed QuoteModels
        """
        quotes = []

        try:
            doc = Document(path)
        except Exception as e:
            print(f"Cannot open docx file {path}: {e}")

        for line in doc.paragraphs:
            if line.text and line.text != "":
                splitted = line.text.split(" - ")
                quotes.append(QuoteModel(splitted[0], splitted[1]))

        return quotes
