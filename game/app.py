"""from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    return f"SUCCESS: Python is alive {name}!"

if __name__ == "__main__":
    app.run()
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Get the name from the box (if they typed one)
    name = request.args.get('name', '')
    
    # 2. Create the message
    if name:
        greeting = f"<h1>SUCCESS: Python is alive {name}!</h1>"
    else:
        greeting = "<h1>Welcome! What is your name?</h1>"

    # 3. This is the HTML that makes the box and button
    # It sends the 'input' back to this same page as '?name=...'
    html_form = """
        <form action="/" method="get">
            <input type="text" name="name" placeholder="Type name here...">
            <input type="submit" value="Send to Python">
        </form>
    """
    
    return greeting + html_form

if __name__ == "__main__":
    app.run()
