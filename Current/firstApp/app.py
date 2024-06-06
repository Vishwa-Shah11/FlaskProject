import os
import uuid
import pandas as pd
from flask import Flask, request, render_template, Response, send_from_directory, url_for, jsonify

app = Flask(__name__, template_folder='templates')

# @app.route('/')
# def index():
#     myvalue = 'vishwa'
#     myresult = '7.1'
#     mylist = [1, 2, 3, 4, 5]
#     return render_template('index.html', mylist=mylist)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'vishwa' and password == 'password':
            return 'POST request : Success'
        else:
            return 'POST request : Failure'


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
    return ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])


@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files.get('file')
    if file.content_type == 'text/plain':
        return file.read().decode()
    elif (file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          or file.content_type == 'application/vnd.ms-excel'):
        df = pd.read_excel(file)
        return df.to_html()


@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files.get('file')
    df = pd.read_excel(file)
    response = Response(
        df.to_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=result.csv'
        }
    )
    return response


@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
    file = request.files.get('file')
    df = pd.read_excel(file)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename))

    return render_template('download.html', filename=filename)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')


@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json.get('greeting')
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'Successfully written!'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
