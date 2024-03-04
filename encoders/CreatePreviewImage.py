import ffmpeg
import os
from werkzeug.datastructures import FileStorage


class createPreviewImage:
    def __init__(self, file, preview_image_path):
        self.file = file
        self.preview_image_path = preview_image_path

    def createImageChunk(self) -> str:
        if isinstance(self.file, FileStorage):
            file = self.file
            preview_image_path = self.preview_image_path
            tmp_path = os.path.join('./tmp', file.filename)

            file.save(tmp_path)
            
            self.imageStreaming(tmp_path, preview_image_path)

            os.remove(tmp_path)

            return 'ok'
            
        else:
            print("Value not found or self.targetFile is not a dict")
            return 'fail'

    @staticmethod
    def imageStreaming(tmp_path, preview_image_path):
        
        ffmpeg.input(tmp_path)\
            .output(preview_image_path, 
                    vframes=1, 
                    vf='scale=1280:720'
                    )\
            .run()