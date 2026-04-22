class QuoteModel:
    """The model that holds a quote's body and author."""

    def __init__(self, body: str, author: str):
        """Create a QuoteModel object.

        Args:
            body (str): body of quote
            author (str): author of quote
        """
        self.body = body
        self.author = author

    def __str__(self):
        return f"Body:{self.body} - Author:{self.author}."

    def __repr__(self):
        return f"Body:{self.body} - Author:{self.author}"
