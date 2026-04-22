class QuoteModel:
    def __init__(self, body: str, author: str):
        self.body = body
        self.author = author

    def __str__(self):
        return f"Body:{self.body} - Author:{self.author}."

    def __repr__(self):
        return f"Body:{self.body} - Author:{self.author}"
