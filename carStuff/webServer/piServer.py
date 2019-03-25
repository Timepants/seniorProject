import sys

import os,sys

# from piInstructorInterface import run_steering_server, stop

from piInstructor import run_steering_server, stop

from flask import Flask, jsonify, render_template, request, Response

from multiprocessing import Queue

from manualInstructor import runInstructor, stopMan

from io import BytesIO

from picamera import PiCamera

class AppServer():
    def __init__(self):
        self.a = 0
        self.b = 0
        self.data = self.data = {
                "throttle":0
                ,"accel": [0
                        , 1
                        , 2]
            }
        self.started = False

    def getOutputData(self, outputQueue):
        # a = request.args.get('a', 0, type=int)
        # b = request.args.get('b', 0, type=int)
        self.a += 1
        self.b += 1

        while not outputQueue.empty():
            self.data = {
                "showLogger":self.showLogger()
                ,"throttle":outputQueue.get()["throttle"]
                ,"accel": [outputQueue.get()["accel_x_scaled"]
                        , outputQueue.get()["accel_y_scaled"]
                        , outputQueue.get()["accel_z_scaled"]]
                ,"steering":outputQueue.get()["steering_angle"]
                ,"proximity":outputQueue.get()["proximity"]
            } 
            print(self.data)


        return jsonify(self.data)
        # return jsonify(result=self.a + self.b)

    def getModels(self):
        files = os.listdir("carModels/")

        return files

    def showLogger(self):
        if outputQueue.empty():
            return 0
        return 1

    def stopAI(self):
        stop()

    def index(self, request):
        if request.method == 'POST':
            model = request.form.get('model', None)
            if model is not None and not self.started:
                run_steering_server("carModels/"+model, outputQueue)
                self.started = True
            manual = request.form.get('manual', None)
            if manual is not None and not self.started:
                runInstructor(outputQueue)
                self.started = True
            stopper = request.form.get('stop', None)
            if stopper is not None:
                self.started = False
                stop()
                stopMan()
        return render_template('bootstrap.html', models = self.getModels(), isRunning = self.started)

appServer = AppServer()

app = Flask(__name__)

outputQueue = Queue()

my_stream = BytesIO()

@app.route('/_getOutputData')
def getOutputData():
    return appServer.getOutputData(outputQueue)

@app.route('/', methods=['GET', 'POST'])
def index():
    return appServer.index(request)

@app.route('/start')
def startServer(model):
    

    return boot()

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
    with PiCamera() as camera:
        while True:
            my_stream.seek(0)
            camera.capture(my_stream, 'jpeg', use_video_port=True)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + my_stream.getvalue() + b'\r\n')

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
