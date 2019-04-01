import os,sys, time
from stat import S_ISREG, ST_CTIME, ST_MODE
# from piInstructorInterface import run_steering_server, stop
from datetime import datetime
from zipLog import zipper, clearPrevious, hasManualData, hasPackagedData, getZipFileName
from piInstructor import run_steering_server, stop

from flask import Flask, jsonify, render_template, request, Response, send_file, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from multiprocessing import Queue

from manualInstructor import runInstructor, stopMan

from io import BytesIO

from picamera import PiCamera

class AppServer():
    def __init__(self):
        self.data = self.data = {
                "throttle":0
                ,"accel": [0
                        , 1
                        , 2]
            }
        self.started = False
        self.paused = False
        self.isManual = False
        self.model = "none"

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


        # regular files, insert creation date
        data = ((stat[ST_CTIME], path)
                for stat, path in data if S_ISREG(stat[ST_MODE]))


        for cdate, path in sorted(data):
            ts = int(cdate)
            files.append({
                "date":datetime.utcfromtimestamp(ts).strftime("%-m/%-d/%y, %-I:%M")
                ,"file_name":os.path.basename(path)
                ,"name":os.path.splitext(os.path.basename(path))[0]
            })

        
        return files

    def showLogger(self):
        if outputQueue.empty():
            return 0
        return 1

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def stopAI(self):
        stop()

    def index(self, request):
        if request.method == 'POST':

            model = request.form.get('model', None)
            if model is not None and not self.started:
                run_steering_server("carModels/"+model, outputQueue)
                self.started = True
                self.isManual = False
                self.model = model

            delete = request.form.get('delete', None)
            if delete is not None and not self.started:
                os.remove("carModels/"+delete)

            manual = request.form.get('manual', None)
            if manual is not None and not self.started:
                runInstructor(outputQueue)
                self.started = True
                self.isManual = True

            stopper = request.form.get('stop', None)
            if stopper is not None:
                self.started = False
                stop()
                stopMan()

            pause = request.form.get('pause', None)
            if pause is not None:
                self.paused = True
                stop()
                stopMan()

            play = request.form.get('play', None)
            if play is not None:
                self.paused = False
                if self.isManual:
                    runInstructor(outputQueue)
                else:
                    run_steering_server("carModels/"+self.model, outputQueue)
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

@app.route('/return-training-files/')
def return_training_files():
    try:
        if (not hasPackagedData() and not hasManualData()):
            clearPrevious()
            fileName = zipper()
        else:
            fileName = getZipFileName()
        return send_file(fileName, as_attachment=True, attachment_filename="training_img.zip")
    except Exception as e:
	    return str(e)

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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

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
