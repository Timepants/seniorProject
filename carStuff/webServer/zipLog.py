import os, shutil
import zipfile
import time
img_folder = 'training_img/'
zip_folder = 'packaged_training/'
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zipper():
    filePath = zip_folder+'training_data'+ time.strftime("%-m-%-d-%Y-%-H:%M:%S") +'.zip'
    zipf = zipfile.ZipFile(filePath, 'w', zipfile.ZIP_DEFLATED)
    zipdir(img_folder, zipf)
    zipf.close()
    clearPreviousImages()
    return filePath

def clearPrevious():
    for the_file in os.listdir(zip_folder):
        file_path = os.path.join(zip_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def clearPreviousImages():
    for the_file in os.listdir(img_folder):
        file_path = os.path.join(img_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def getZipFileName():
    return zip_folder+os.listdir(zip_folder)[0]

def hasManualData():
    print(len(os.listdir(img_folder) ) > 0)
    return len(os.listdir(img_folder) ) > 0

def hasPackagedData():
    print(len(os.listdir(zip_folder) ) > 0)
    return len(os.listdir(zip_folder) ) > 0

if __name__ == '__main__':
    clearPrevious()
    zipper()