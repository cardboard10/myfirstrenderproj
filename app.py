from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello! This is Landon's Python Server.</h1><p>No HTML files here, just pure Python logic.</p>"

if __name__ == "__main__":
    app.run()
