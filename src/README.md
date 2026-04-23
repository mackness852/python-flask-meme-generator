# python-flask-meme-generator

This project exposes a flask app and a CLI process.

It generates memes based on the user input for both.

## Flask app: 
To get it up and running, cd to the src/ directory and run: python3 app.py

- random meme: http://127.0.0.1:5000/
- create a meme: http://127.0.0.1:5000/create

note - the server deletes generated images 3s after responding with html, so the user can see the image but it doesn't clog up the ./static folder

## CLI process: 
Example usage,  cd to the src/ directory and run: python3 meme.py --body "the quote body" --author "author's name"

Saves memes to the ./tmp folder

## Description of sub-modules and their dependencies

### Module: `quote_engine`

**QuoteModel**
Data model for a quote.
- **Imports:** none
- **Attributes:** `body: str`, `author: str`
- **Methods:** `__str__`, `__repr__` — return formatted `"body - author"` strings

**IngestorInterface (ABC)**
Abstract base for all file parsers.
- **Imports:**
  - `abc.ABC`, `abc.abstractmethod` — enforce the interface contract; subclasses that don't implement `parse` raise `TypeError` at instantiation
  - `QuoteModel` — type used in the `parse` return signature
- **Attributes:** `allowed_file_exts: list` — override in subclasses
- **Methods:**
  - `can_ingest(cls, path: str) -> bool` — checks file extension against `allowed_file_exts`
  - `parse(cls, path: str) -> list[QuoteModel]` — abstract; implement in subclasses

**CsvIngestor(IngestorInterface)**
Parses `.csv` files with `body` and `author` columns.
- **Imports:**
  - `pandas` — reads the CSV into a DataFrame for column-based access
  - `IngestorInterface` — base class
  - `QuoteModel` — return type
- **Methods:** `parse(cls, path: str) -> list[QuoteModel]`

**DocxIngestor(IngestorInterface)**
Parses `.docx` files; expects lines formatted as `body - author`.
- **Imports:**
  - `docx.Document` (`python-docx`) — opens and iterates Word document paragraphs
  - `IngestorInterface` — base class
  - `QuoteModel` — return type
- **Methods:** `parse(cls, path: str) -> list[QuoteModel]`

**PdfIngestor(IngestorInterface)**
Parses `.pdf` files via the `pdftotext` system binary; expects lines formatted as `body - author`.
- **Imports:**
  - `subprocess` — shells out to `pdftotext` to extract raw text from the PDF
  - `IngestorInterface` — base class
  - `QuoteModel` — return type
- **Methods:** `parse(cls, path: str) -> list[QuoteModel]`

**TxtIngestor(IngestorInterface)**
Parses `.txt` files; expects lines formatted as `body - author`.
- **Imports:**
  - `IngestorInterface` — base class
  - `QuoteModel` — return type
- **Methods:** `parse(cls, path: str) -> list[QuoteModel]`

**Ingestor**
Facade that dispatches to the correct ingestor by file extension.
- **Imports:**
  - `CsvIngestor`, `DocxIngestor`, `PdfIngestor`, `TxtIngestor` — concrete parsers registered in `ingestors`
  - `QuoteModel` — return type
- **Attributes:** `allowed_file_exts: ["csv", "docx", "pdf", "txt"]`, `ingestors: list` — all concrete ingestors
- **Methods:** `parse(cls, path: str) -> list[QuoteModel]` — iterates ingestors, delegates to matching one

---

### Module: `meme_generation`

**MemeEngine**
Generates meme images by overlaying quote text on a source image.
- **Imports:**
  - `PIL.Image`, `PIL.ImageDraw`, `PIL.ImageFont` (`Pillow`) — image loading, resizing, and text rendering
  - `requests` — fetches images from HTTP/HTTPS URLs
  - `random` — generates a random filename for each saved meme
  - `urllib.parse.urlparse` — detects whether the input path is a URL
- **Attributes:** `dir_path: str` — output directory; `_font_path` — path to `LilitaOne-Regular.ttf`
- **Methods:**
  - `make_meme(img_path, text, author, width=500) -> str` — resizes image, draws text/author, saves PNG, returns filepath
  - `get_resized_image(img_path, width) -> PIL.Image` — loads from local path or HTTP URL, resizes proportionally
  - `is_url(path: str) -> bool` — returns `True` if path is an HTTP/HTTPS URL
  - `draw_text(img, text, author, width)` — draws white text and author onto image; font size = `width / 20`
