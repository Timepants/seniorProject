import os,sys, time
from stat import S_ISREG, ST_CTIME, ST_MODE
from datetime import datetime
from zipLog import zipper, clearPrevious, hasManualData, hasPackagedData, getZipFileName
import slowpiInstructor 
import colorpiInstructor
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
        self.useColor = False

    def getOutputData(self, outputQueue):
        while not outputQueue.empty():
            temp = outputQueue.get()
            self.data = {
                "showLogger":self.showLogger()
                ,"throttle":temp["throttle"]
                ,"accel": [temp["accel_x_scaled"]
                        , temp["accel_y_scaled"]
                        , temp["accel_z_scaled"]]
                ,"magnitude":temp["magnitude"]
                ,"steering":temp["steering_angle"]
                ,"proximity":temp["proximity"]
                ,"stopAccel":temp["stop_accel"] if not self.isManual else False
                ,"stopProximity":temp["stop_proximity"] if not self.isManual else False
            } 
            
            if (temp["stop_accel"] or temp["stop_proximity"]):
                if not self.isManual:
                    self.started = False
                    self.stopAI()
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


        for cdate, path in sorted(data, reverse=True):
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
        if (self.useColor):
            colorpiInstructor.stop()
        else:
            slowpiInstructor.stop()

    def index(self, request):
        if request.method == 'POST':
            color = request.form.get('colorPicker', None)
            if color is not None and not self.started:
                colorpiInstructor.run_color_AI(outputQueue)
                self.started = True
                self.isManual = False
                self.useColor = True

            model = request.form.get('model', None)
            if model is not None and not self.started:
                slowpiInstructor.run_nn_AI("carModels/"+model, outputQueue)
                self.started = True
                self.isManual = False
                self.model = model
                self.useColor = False

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
                self.stopAI()
                stopMan()

            pause = request.form.get('pause', None)
            if pause is not None:
                self.paused = True
                self.stopAI()
                stopMan()

            play = request.form.get('play', None)
            if play is not None:
                self.paused = False
                if self.isManual:
                    runInstructor(outputQueue)
                else:
                    if (self.useColor):
                        colorpiInstructor.run_color_AI(outputQueue)
                    else:
                        slowpiInstructor.run_nn_AI("carModels/"+self.model, outputQueue)
        return render_template('bootstrap.html'
                    , models = self.getModels()
                    , isRunning = self.started
                    , isPaused = self.paused
                    , isManual = self.isManual
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

def gen():
    with PiCamera() as camera:
        camera.rotation = 180
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
        if (not hasPackagedData() or hasManualData()):
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
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
