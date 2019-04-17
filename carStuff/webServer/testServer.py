import os,sys, time
from stat import S_ISREG, ST_CTIME, ST_MODE
from piInstructorInterface import runInstructor, stop
from datetime import datetime
from zipLog import zipper, clearPrevious, hasManualData, hasPackagedData, getZipFileName
# from piInstructor import run_steering_server, stop

from flask import Flask, jsonify, render_template, request, Response, send_file, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from multiprocessing import Queue

# from manualInstructor import CarControllerManual as manual

from io import BytesIO

class AppServer():
    def __init__(self):
        self.started = False
        self.paused = False
        self.model = "none"
        self.data = self.data = {
                "throttle":0
                ,"accel": [0
                        , 1
                        , 2]
            } 

    def getOutputData(self, outputQueue):
        while not outputQueue.empty():
            temp = outputQueue.get()
            self.data = {
                "showLogger":self.showLogger()
                ,"throttle":temp["throttle"]
                ,"accel": [temp["accel_x_scaled"]
                        , temp["accel_y_scaled"]
                        , temp["accel_z_scaled"]]
                ,"magnitude":temp["accel_z_scaled"]
                ,"steering":temp["steering_angle"]
                ,"proximity":temp["proximity"]
                ,"stopAccel":False
                ,"stopProximity":False
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
            ts = int(cdate)
            files.append({
                "date":datetime.utcfromtimestamp(ts).strftime("%m/%m/%y, %I:%M")
                ,"file_name":os.path.basename(path)
                ,"name":os.path.splitext(os.path.basename(path))[0]
            })

        
        return files

    def showLogger(self):
        if outputQueue.empty():
            return 0
        return 1

    def stopAI(self):
        stop()

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def index(self, request):
        if request.method == 'POST':

            model = request.form.get('model', None)
            if model is not None and not self.started:
                self.model = model
                runInstructor("carModels/"+self.model, outputQueue)
                self.started = True

            delete = request.form.get('delete', None)
            if delete is not None and not self.started:
                os.remove("carModels/"+delete)

            manual = request.form.get('manual', None)
            if manual is not None and not self.started:
                runInstructor("carModels",  outputQueue)
                self.started = True

            stopper = request.form.get('stop', None)
            if stopper is not None:
                self.started = False
                self.paused = False
                stop()

            pause = request.form.get('pause', None)
            if pause is not None:
                self.paused = True
                stop()

            play = request.form.get('play', None)
            if play is not None:
                self.paused = False
                runInstructor("carModels/"+self.model, outputQueue)

        return render_template('bootstrap.html'
                    , models = self.getModels()
                    , isRunning = self.started
                    , isPaused = self.paused
                    , hasManualData = (hasManualData() or hasPackagedData()))
appServer = AppServer()

UPLOAD_FOLDER = 'carModels/'
ALLOWED_EXTENSIONS = set(['h5'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/return-training-files/')
def return_training_files():
    # try:
    if (not hasPackagedData() or hasManualData()):
        clearPrevious()
        fileName = zipper()
    else:
        fileName = getZipFileName()
    return send_file(fileName, as_attachment=True, attachment_filename="training_img.zip")
    # except Exception as e:
	#     return str(e)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and appServer.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
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
