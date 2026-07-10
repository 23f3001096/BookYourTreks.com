from flask import Flask, send_from_directory
from app import create_app

app = create_app()


@app.route("/")
def home():
    return send_from_directory('../../Frontend',"index.html")

app.run(debug=True)