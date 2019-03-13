import sys

import os,sys

from piInstructorInterface import run_steering_server, stop

from flask import Flask, jsonify, render_template, request, Response

from multiprocessing import Queue

from io import BytesIO

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
            self.value = outputQueue.get()["throttle"]
            print(self.value)

        return jsonify(result=float(self.value))
        # return jsonify(result=self.a + self.b)

    def getModels(self):
        files = os.listdir("carModels/")

        return files

appServer = AppServer()

app = Flask(__name__)

outputQueue = Queue()

my_stream = BytesIO()

@app.route('/_add_numbers')
def add_numbers():
    return appServer.add_numbers(outputQueue)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model = request.form.get('model', None)
        if model is not None:
            run_steering_server("carModels/"+model, outputQueue)
        stopper = request.form.get('stop', None)
        if stopper is not None:
            stop()
    return render_template('index.html', models = appServer.getModels())

@app.route('/start<model>')
def startServer(model):
    

    return index()

@app.route('/stop')
def stopServer():
    stop()
    return index()

@app.route('/boot')
def boot():
    return render_template('bootstrap.html')

@app.route('/video')
def video():
    return render_template('videoTest.html')

def gen():
    print("gen")
    # with PiCamera() as camera:
    #     while True:
    #         my_stream.seek(0)
    #         camera.capture(my_stream, 'jpeg', use_video_port=True)
    #         yield (b'--frame\r\n'
    #             b'Content-Type: image/jpeg\r\n\r\n' + my_stream.getvalue() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
