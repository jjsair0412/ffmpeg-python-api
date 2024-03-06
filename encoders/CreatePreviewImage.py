import ffmpeg
import os
from werkzeug.datastructures import FileStorage
import shutil
from encoders.storageAccessManager.storageAccess import storageAccess


class createPreviewImage:
    def __init__(self, file, previewPath, originName, xAuthToken, contentType):
        self.file = file
        self.previewPath = previewPath
        self.originName = originName
        self.xAuthToken = xAuthToken
        self.contentType = contentType

    def createImageChunk(self) -> str:
        if isinstance(self.file, FileStorage):
            file = self.file
            previewPath = self.previewPath
            originName = self.originName
            xAuthToken = self.xAuthToken
            contentType = self.contentType

            if os.path.isdir("/app/tmp/"+previewPath) == False:
                os.makedirs("/app/tmp/"+previewPath)

            tmp_path = os.path.join('/app/tmp/'+previewPath, originName)
            file.save(tmp_path)
            
            output_save_path = '/app/tmp/'+previewPath+'/' + originName+".png"
            self.imageStreaming(tmp_path, output_save_path, xAuthToken, contentType)

            shutil.rmtree('/app/tmp/'+previewPath)
            return 'ok'
            
        else:
            return 'Value not found or self.targetFile is not a dict',500

    @staticmethod
    def imageStreaming(tmp_path, output_save_path, xAuthToken, contentType):
        
        ffmpeg.input(tmp_path)\
            .output(output_save_path, 
                    vframes=1, 
                    vf='scale=1280:720'
                    )\
            .run()

        os.remove(tmp_path)

        print('output_save_path : ' + output_save_path)
        with open(output_save_path, 'rb') as image:
            storageManager = storageAccess(xAuthToken, output_save_path[6:], contentType , image.read())
            storageManager.streamingUpload()
            

