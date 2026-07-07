from flask import Flask, send_from_directory
from app import create_app

app = create_app()

# Change Jinja's default tags so they don't clash with Vue

app.jinja_env.variable_start_string = '{$'
app.jinja_env.variable_end_string = '$}'

@app.route("/")
def home():
    return send_from_directory('../../Frontend',"index.html")

app.run(debug=True)