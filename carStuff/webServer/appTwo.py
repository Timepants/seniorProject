import sys

# sys.path.append('../src/unused')

# from ..src.unused.phpTest import butts
from piInstructor import run_steering_server, stop

from flask import Flask, jsonify, render_template, request

from picamera import PiCamera

from multiprocessing import Queue
class AppServer():
    def __init__(self):
        self.a = 0
        self.b = 0
        self.value = 0

    def add_numbers(self, outputQueue):
        # a = request.args.get('a', 0, type=int)
        # b = request.args.get('b', 0, type=int)
        self.a += 1
        self.b += 1



        while not outputQueue.empty():
            self.value = outputQueue.get()[2]

        return jsonify(result=float(self.value))
        # return jsonify(result=self.a + self.b)

appServer = AppServer()

app = Flask(__name__)

outputQueue = Queue()



@app.route('/_add_numbers')
def add_numbers():
    return appServer.add_numbers(outputQueue)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def startServer():
    
    run_steering_server("carModels/maroon.h5", outputQueue)
    return index()

@app.route('/stop')
def stopServer():
    # camera.close()
    stop()
    return index()

if __name__ == '__main__':
    # if __package__ is None:
    #     print ("no package")
    #     import sys
    #     from os import path
    #     sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    #     from src.piInstructor import run_steering_server, stop
    # else:
    #     from ..src.piInstructor import run_steering_server, stop

    app.run(debug=True, host='0.0.0.0')
