from flask import Flask

app = Flask(__name__)

@app.route('/')
def top_page():
    return 'Alive'
