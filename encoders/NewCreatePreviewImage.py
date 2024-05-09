import ffmpeg
import os
import shutil
from encoders.storageAccessManager.awsStorageAccess import awsStorageAccess
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader
import subprocess
from dotenv import load_dotenv


class newCreatePreviewImage:
    def __init__(self, previewPath,  origin_file_name, save_file_name, save_waterMark_path):
        self.previewPath = previewPath
        self.origin_file_name = origin_file_name
        self.save_file_name = save_file_name
        self.save_waterMark_path = save_waterMark_path

    def createImageChunk(self) -> str:
        previewPath = self.previewPath
        origin_file_name = self.origin_file_name
        save_file_name = self.save_file_name

        if os.path.isdir("/tmp/"+previewPath) == False:
            os.makedirs("/tmp/"+previewPath)

        # 미리보기 이미지 생성용 임시파일 저장 경로
        tmp_path = os.path.join('/tmp/'+previewPath, origin_file_name)
        # 미리보기 이미지 파일 이름 생성
        output_save_path = '/tmp/'+previewPath+'/' + origin_file_name+'.png'
        # s3에서 파일 다운로드
        file_downloader = Downloader(
            file_path=save_file_name,
            sample_file_path='/tmp/'+previewPath,
            file_name=origin_file_name,
            bucket_name=os.environ.get('contents_bucket_name')
            )
        file_downloader.multipartFileDownloader()

        self.imageStreaming(tmp_path, output_save_path, self.save_waterMark_path)

        os.remove(self.save_waterMark_path)
        os.remove(output_save_path)
        os.remove(tmp_path)
        return 'ok'
            
    @staticmethod
    def imageStreaming(tmp_path, output_save_path, save_waterMark_path):
        

        load_dotenv(dotenv_path='./config/.env')
        ffprobe_path = os.environ.get('ffprobe_path')
        
        cmd = [
            ffprobe_path,
            '-v', 'error',
            '-show_entries','stream=width,height',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            tmp_path
        ] 

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()  # 바이트 객체를 문자열로 변환
        width, height = output.strip().split('\n')

        ffmpeg.input(tmp_path)\
            .output(output_save_path, vframes=1, **{'qscale:v': 15})\
            .global_args(
                '-i',save_waterMark_path, 
                '-filter_complex', f'[1:v]scale=w=trunc({width}/2):h=-1 [wm]; [0:v][wm]overlay=W-w-50:H-h-50'
                )\
            .run()
        
        with open(output_save_path, 'rb') as image:
            target_image = {'file': (output_save_path[5:],image)}
            storageManager = awsStorageAccess(target_image, output_save_path[5:])
            storageManager.streamingUpload()
            