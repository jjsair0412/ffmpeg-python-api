import shutil
import glob
import ffmpeg
import os
from werkzeug.datastructures import FileStorage
from encoders.storageAccessManager.awsStorageAccess import awsStorageAccess
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader


class newCreateStreaming:
    def __init__(self, uploadPath, contentName, origin_file_name, save_file_name, save_waterMark_path):
        self.uploadPath = uploadPath
        self.contentName = contentName
        self.origin_file_name = origin_file_name
        self.save_file_name = save_file_name
        self.save_waterMark_path = save_waterMark_path

    
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
        tmp_path = os.path.join('/tmp/'+save_file_name, origin_file_name)


        # s3에서 파일 다운로드
        file_downloader = Downloader(
            file_path=save_file_name,
            file_name=origin_file_name,
            sample_file_path='/tmp/'+save_file_name,
            bucket_name=os.environ.get('contents_bucket_name')
            )
        file_downloader.multipartFileDownloader()

        self.videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, '/tmp/'+uploadPath, contentName, self.save_waterMark_path)

        os.remove(tmp_path)
        os.remove(self.save_waterMark_path)
        shutil.rmtree("/tmp/"+uploadPath)
        return 'ok'
            

    @staticmethod
    def videoStreaming(tmp_path, m3u8FilePath, ts_segment_pattern, uploadPath, contentName, save_waterMark_path):

        # ffmpeg.input(tmp_path)\
        #     .output(
        #         m3u8FilePath,
        #         # vf='scale=1280:720',
        #         format='hls', 
        #         vcodec='libx264', 
        #         crf=40,
        #         hls_time=3, 
        #         hls_list_size=0, 
        #         hls_segment_filename=ts_segment_pattern, 
        #         **{'profile:v': 'high444'})\
        #     .global_args(
        #         '-i',save_waterMark_path, 
        #         '-filter_complex', '[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p'
        #         )\[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=(W-w)/2:H-h:format=auto,format=yuv420p
        #     .run()
        # [0:v][1:v]scale2ref=w=iw:h=ow/mdar[base][wm];[base][wm]overlay=(W-w)/2:(H-h)-10,pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2

        ffmpeg.input(tmp_path)\
            .output(
                m3u8FilePath,
                format='hls', 
                vcodec='libx264', 
                crf=30,
                hls_time=3, 
                hls_list_size=0, 
                hls_segment_filename=ts_segment_pattern, 
                **{'profile:v': 'high444'})\
            .global_args(
                '-i',save_waterMark_path, 
                '-filter_complex','overlay=W-w-5:H-h-5'
                )\
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


        
    
