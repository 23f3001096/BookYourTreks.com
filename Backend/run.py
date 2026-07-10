from flask import Flask, send_from_directory
from app import create_app

app = create_app()

@app.route("/")
@app.route("/<path:path>") 
def home(path=None):
    return send_from_directory('../../Frontend', "index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory('../../Frontend', filename)

if __name__ == '__main__':
    app.run(debug=True)