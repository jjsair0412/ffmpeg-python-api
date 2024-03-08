import shutil
import glob
import ffmpeg
import os
from werkzeug.datastructures import FileStorage
from encoders.storageAccessManager.storageAccess import storageAccess

class createStreaming:
    def __init__(self, file, xAuthToken, uploadPath, contentName):
        self.file = file
        self.xAuthToken = xAuthToken
        self.uploadPath = uploadPath
        self.contentName = contentName

    
    def createVideoChunk(self) -> str:
        if isinstance(self.file, FileStorage):
            file = self.file
            uploadPath = self.uploadPath
            contentName = self.contentName

            if os.path.isdir("/tmp/"+uploadPath) == False:
                os.makedirs("/tmp/"+uploadPath)
            
            save_path =  '/tmp/' + uploadPath + "/" + contentName

            m3u8FilePath = save_path + '.m3u8'
            ts_segment_pattern = save_path + '_%03d_.ts'
            xAuthToken = self.xAuthToken

            tmp_path = os.path.join('/tmp/'+uploadPath, file.filename)

            file.save(tmp_path)
            
            self.videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, '/tmp/'+uploadPath, xAuthToken, contentName)

            os.remove(tmp_path)
            shutil.rmtree("/tmp/"+uploadPath)
            return 'ok'
            
        else:
            return 'createMetadata: Value not found or self.targetFile is not a dict', 500

    @staticmethod
    def videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, uploadPath, xAuthToken, contentName):

        ffmpeg.input(tmp_path)\
            .output(
                m3u8FilePath,
                vf='scale=1280:720',
                format='hls', 
                vcodec='libx264', 
                hls_time=3, 
                hls_list_size=0, 
                hls_segment_filename=ts_segment_pattern, 
                **{'profile:v': 'high444'})\
            .run()
        
        ts_file_names = glob.glob(uploadPath + '/' + contentName + '*.ts')
        for ts_path in ts_file_names:
            with open(ts_path,'rb') as tsFile:
                storageManager = storageAccess(xAuthToken, ts_path[5:], 'application/octet-stream' , tsFile.read())
                storageManager.streamingUpload()
                
                
        m3u8FilePath = glob.glob(uploadPath + '/' + contentName + '.m3u8')
        for playlistPath in m3u8FilePath:
            with open(playlistPath, 'rb') as playlistFile:
                storageManager = storageAccess(xAuthToken, playlistPath[5:], 'application/octet-stream' , playlistFile.read())
                storageManager.streamingUpload()


        
    
