import os,sys, time
from stat import S_ISREG, ST_CTIME, ST_MODE
from piInstructorInterface import runInstructor, stop

# from piInstructor import run_steering_server, stop

from flask import Flask, jsonify, render_template, request, Response

from multiprocessing import Queue

# from manualInstructor import CarControllerManual as manual

from io import BytesIO

class AppServer():
    def __init__(self):
        self.started = False
        self.data = self.data = {
                "throttle":0
                ,"accel": [0
                        , 1
                        , 2]
            } 

    def getOutputData(self, outputQueue):
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
        files = list()
        #Relative or absolute path to the directory
        dir_path = "carModels/"

        #all entries in the directory w/ stats
        data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
        data = ((os.stat(path), path) for path in data)

        # for datum in data:
        #     print(datum)

        # regular files, insert creation date
        data = ((stat[ST_CTIME], path)
                for stat, path in data if S_ISREG(stat[ST_MODE]))


        for cdate, path in sorted(data):
            print(time.ctime(cdate), os.path.basename(path))
            files.append({
                "date":time.ctime(cdate)
                ,"file_name":os.path.basename(path)
            })

        
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
                runInstructor("carModels/"+model, outputQueue)
                self.started = True
            manual = request.form.get('manual', None)
            if manual is not None and not self.started:
                runInstructor("carModels",  outputQueue)
                self.started = True
            stopper = request.form.get('stop', None)
            if stopper is not None:
                self.started = False
                stop()
        return render_template('bootstrap.html', models = self.getModels(), isRunning = self.started)
appServer = AppServer()

app = Flask(__name__)

outputQueue = Queue()

# man = manual()

@app.route('/_getOutputData')
def getOutputData():
    return appServer.getOutputData(outputQueue)

@app.route('/', methods=['GET', 'POST'])
def index():
    return appServer.index(request)

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

@app.route('/video_feed')
def video_feed():
    return "wow"

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
