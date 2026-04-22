import os
import random
import threading

from flask import Flask, render_template, request

from meme_generation import MemeEngine
from quote_engine import Ingestor

app = Flask(__name__)

meme = MemeEngine("./static")


def setup():
    """Load all resources"""

    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]
    quotes = []

    for path in quote_files:
        for quote in Ingestor.parse(path):
            quotes.append(quote)

    images_path = "./_data/photos/dog/"

    imgs = [images_path + img for img in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme"""

    img = imgs[random.randint(0, len(imgs) - 1)]
    quote = quotes[random.randint(0, len(quotes) - 1)]
    path = meme.make_meme(img, quote.body, quote.author)

    delayed_delete(path)

    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information"""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme"""

    image_url = request.form.get("image_url")
    body = request.form.get("body")
    author = request.form.get("author")
    path = meme.make_meme(image_url, body, author)

    delayed_delete(path)

    return render_template("meme.html", path=path)


def delayed_delete(path, delay=3):
    """Not sure if there was a type in the task but it said to remove
    the image once served. I tried the flask.after_this_request
    decorator to describe the deletion logic below, but of course
    the page html was served first and image download second, so the
    image would already be deleted after serving the html. This
    introduces a new background thread that waits three seconds then
    deletes the file. I'm not sure if this is safe or industry
    standard, as I haven't touched python or flask much. But it seems to
    me safe enough. The daemon=False appears to control whether python
    can kill the parent flask process before the delete_the_image is
    finished, False = no it has to wait. So shutdown would be delayed
    by up to three seconds but that is ok. The wait is in the function
    that is used in the Thread, so it doesn't block flask requests
    during the wait.

    Args:
        path (str): path of file to delete
    """

    def delete_the_image():
        threading.Event().wait(delay)
        try:
            os.remove(path)
        except OSError as e:
            print(f"Cannot delete {path}: {e}")

    threading.Thread(target=delete_the_image, daemon=False).start()


if __name__ == "__main__":
    app.run()
