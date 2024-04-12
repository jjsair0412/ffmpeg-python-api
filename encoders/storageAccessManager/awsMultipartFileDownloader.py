import boto3
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Downloader:

    def __init__(self, file_path, file_name, sample_file_path) -> None:
        self.file_path = file_path
        self.file_name = file_name
        self.sample_file_path = sample_file_path

    
    def multipartFileDownloader(self):
        try:

            load_dotenv(dotenv_path='./config/.env')

            file_path = self.file_path
            file_name = self.file_name
            # 파일이 저장될 디렉토리 경로 추출
            dir_path = self.sample_file_path

            
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            
            # 사전인증 S3 POST URL 생성하기
            client = boto3.client(
                's3',
                aws_access_key_id=os.environ.get('access_key'),
                aws_secret_access_key=os.environ.get('secret_key'),
                region_name=os.environ.get('region_name')
            )
           

            client.download_file(
                os.environ.get('bucket_name'),
                file_path,  # 파일의 키를 지정합니다.
                dir_path +'/'+ file_name  # 로컬에 저장될 파일 경로 및 이름을 지정합니다.
            )

        except Exception as e :
            raise Exception(e)
        
        