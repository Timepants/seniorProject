import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
# sys.path.append('../src/unused')

from phpTest import butts

from flask import Flask, jsonify, render_template, request

class AppServer():

    def __init__(self):
        self.a = 0
        self.b = 0

    def add_numbers(self):
        # a = request.args.get('a', 0, type=int)
        # b = request.args.get('b', 0, type=int)
        self.a += 1
        self.b += 1
        return jsonify(result=butts())
        # return jsonify(result=self.a + self.b)

appServer = AppServer()

app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    return appServer.add_numbers()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
