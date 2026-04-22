from docx import Document
from ingestor_interface import IngestorInterface
from quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    allowed_file_exts = ["docx"]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:

        quotes = []

        doc = Document(path)

        for line in doc.paragraphs:
            if line.text and line.text != "":
                splitted = line.text.split(" - ")
                quotes.append(QuoteModel(splitted[0], splitted[1]))

        return quotes
