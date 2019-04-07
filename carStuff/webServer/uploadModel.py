import os, shutil
import zipfile
import time
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zipper():
    filePath = 'packaged_training/training_data'+ time.strftime("%-m-%-d-%Y-%-H:%M:%S") +'.zip'
    zipf = zipfile.ZipFile(filePath, 'w', zipfile.ZIP_DEFLATED)
    zipdir('training_img/', zipf)
    zipf.close()
    return filePath

def clearPrevious():
    folder = 'packaged_training/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    clearPrevious()
    zipper()