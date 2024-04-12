import shutil
import glob
import ffmpeg
import os
from werkzeug.datastructures import FileStorage
from encoders.storageAccessManager.awsStorageAccess import awsStorageAccess
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader


class newCreateStreaming:
    def __init__(self, uploadPath, contentName, origin_file_name, save_file_name):
        self.uploadPath = uploadPath
        self.contentName = contentName
        self.origin_file_name = origin_file_name
        self.save_file_name = save_file_name

    
    def createVideoChunk(self) -> str:
        uploadPath = self.uploadPath
        contentName = self.contentName
        origin_file_name = self.origin_file_name
        save_file_name = self.save_file_name


        if os.path.isdir("/tmp/"+uploadPath) == False:
            os.makedirs("/tmp/"+uploadPath)
        
        # 스트리밍 청크 생성용 임시저장파일 저장경로
        save_path =  '/tmp/' + uploadPath + "/" + contentName
        # m3u8 파일 이름 생성
        m3u8FilePath = save_path + '.m3u8'
        # ts 파일 이름 생성
        ts_segment_pattern = save_path + '_%03d_.ts'
        # 실제 임시저장된 파일의 경로와 이름이 저장된 변수
        tmp_path = os.path.join('/tmp/'+uploadPath, origin_file_name)


        # s3에서 파일 다운로드
        file_downloader = Downloader(
            file_path=save_file_name,
            file_name=origin_file_name,
            sample_file_path=tmp_path
            )
        file_downloader.multipartFileDownloader()

        self.videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, '/tmp/'+uploadPath, contentName)

        os.remove(tmp_path)
        shutil.rmtree("/tmp/"+uploadPath)
        return 'ok'
            

    @staticmethod
    def videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, uploadPath, contentName):

        ffmpeg.input(tmp_path)\
            .output(
                m3u8FilePath,
                # vf='scale=1280:720',
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
                target_ts_file = {'file': (ts_path[5:], tsFile)}
                storageManager = awsStorageAccess(target_ts_file, ts_path[5:])
                storageManager.streamingUpload()
                
                
        m3u8FilePath = glob.glob(uploadPath + '/' + contentName + '.m3u8')
        for playlistPath in m3u8FilePath:
            with open(playlistPath, 'rb') as playlistFile:
                target_playlist_file = {'file': (playlistPath[5:], playlistFile)}
                storageManager = awsStorageAccess(target_playlist_file, playlistPath[5:])
                storageManager.streamingUpload()


        
    