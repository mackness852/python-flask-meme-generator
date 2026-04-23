# python-flask-meme-generator

This project exposes a flask app and a CLI process.

It generates memes based on the user input for both.

## Flask app: 
To get it up and running: python3 app.py

- random meme: http://127.0.0.1:5000/
- create a meme: http://127.0.0.1:5000/create

note - the server deletes generated images 3s after responding with html, so the user can see the image but it doesn't clog up the ./static folder

## CLI process: 
Example usage: python3 meme.py --body "the quote body" --author "author's name"

saves memes to the ./tmp folder