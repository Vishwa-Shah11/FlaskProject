from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    myvalue = 'vishwa'
    myresult = '7.1'
    mylist = [1, 2, 3, 4, 5]
    return render_template('index.html', mylist=mylist)

@app.route('/filter')
def filter():
    some_text = 'Creating Filters'
    return render_template('filter.html', some_text=some_text)

@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('filter'))

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return "You made a GET request\n"
    elif request.method == 'POST':
        return "You made a POST request\n"
    else:
        return "Hellowww"


@app.route('/greet/<name>')
def greet(name):
    return f"Congratulations {name}"

@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    return f'{num1} + {num2} = {num1 + num2}'

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return "Some parameters are missing"


@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]

@app.template_filter('repeat')
def repeat(s, times=2):
    return s * times


@app.template_filter('alternate_case')
def altername_case(s):
    return ''.join([c.upper() if i%2 == 0 else c.lower() for i, c in enumerate(s)])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)