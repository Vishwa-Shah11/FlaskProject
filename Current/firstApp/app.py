from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hi Vishwa!</h1>"

@app.route('/hello')
def hello():
    return "Hellowww"


@app.route('/greet/<name>')
def greet(name):
    return f"Congratulations {name}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)