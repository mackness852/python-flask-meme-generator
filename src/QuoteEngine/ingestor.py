from csv_ingestor import CsvIngestor
from docx_ingestor import DocxIngestor
from pdf_ingestor import PdfIngestor
from quote_model import QuoteModel
from txt_ingestor import TxtIngestor


class Ingestor:
    allowed_file_exts = ["csv", "docx", "pdf", "txt"]
    ingestors = [CsvIngestor, DocxIngestor, TxtIngestor, PdfIngestor]

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:

        quotes = []

        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                quotes = ingestor.parse(path)
                break

        return quotes
