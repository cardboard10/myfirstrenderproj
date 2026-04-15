from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    return f"SUCCESS: Python is alive {name}!"

if __name__ == "__main__":
    app.run()
