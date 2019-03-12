from flask import Flask, render_template, Response, request
from io import BytesIO

my_stream = BytesIO()


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form['firstname'])
        name = request.form.get('butt', None)
        if name is None:
            print("no butt")
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)