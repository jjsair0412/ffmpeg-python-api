import ffmpeg
import os
from werkzeug.datastructures import FileStorage

class createStreaming:
    def __init__(self, file, tsSegmentPattern, outputFilePath):
        self.file = file
        self.tsSegmentPattern = tsSegmentPattern
        self.outputFilePath = outputFilePath

    
    def createVideoChunk(self) -> str:
        if isinstance(self.file, FileStorage):
            file = self.file
            ts_segment_pattern = self.tsSegmentPattern
            outputFilePath = self.outputFilePath
            tmp_path = os.path.join('./tmp', file.filename)

            file.save(tmp_path)
            
            self.videoStreaming(tmp_path, outputFilePath, ts_segment_pattern)

            os.remove(tmp_path)

            return 'ok'
            
        else:
            print("createMetadata: Value not found or self.targetFile is not a dict")
            return 'fail'

    @staticmethod
    def videoStreaming(tmp_path, outputFilePath, ts_segment_pattern):
        ffmpeg.input(tmp_path)\
            .output(
                outputFilePath,
                vf='scale=1280:720',
                format='hls', 
                vcodec='libx264', 
                hls_time=3, 
                hls_list_size=0, 
                hls_segment_filename=ts_segment_pattern, 
                **{'profile:v': 'high444'})\
            .run()
        
        
        
