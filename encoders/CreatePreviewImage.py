import ffmpeg
import os
from werkzeug.datastructures import FileStorage
import shutil
from encoders.storageAccessManager.storageAccess import storageAccess
from encoders.storageAccessManager.awsStorageAccess import awsStorageAccess



class createPreviewImage:
    def __init__(self, file, previewPath, originName):
        self.file = file
        self.previewPath = previewPath
        self.originName = originName

    def createImageChunk(self) -> str:
        if isinstance(self.file, FileStorage):
            file = self.file
            previewPath = self.previewPath
            originName = self.originName

            if os.path.isdir("/tmp/"+previewPath) == False:
                os.makedirs("/tmp/"+previewPath)

            tmp_path = os.path.join('/tmp/'+previewPath, originName)
            file.save(tmp_path)
            
            output_save_path = '/tmp/'+previewPath+'/' + originName+".png"
            self.imageStreaming(tmp_path, output_save_path)

            shutil.rmtree('/tmp/'+previewPath)
            return 'ok'
            
        else:
            return 'Value not found or self.targetFile is not a dict',500

    @staticmethod
    def imageStreaming(tmp_path, output_save_path):
        
        ffmpeg.input(tmp_path)\
            .output(output_save_path, 
                    vframes=1, 
                    vf='scale=1280:720'
                    )\
            .run()

        os.remove(tmp_path)

        print('output_save_path : ' + output_save_path)
        with open(output_save_path, 'rb') as image:
            target_image = {'file': (output_save_path[5:],image)}
            storageManager = awsStorageAccess(target_image, output_save_path[5:])
            storageManager.streamingUpload()
            