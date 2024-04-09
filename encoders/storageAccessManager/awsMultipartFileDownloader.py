import boto3
from boto3.s3.transfer import TransferConfig
import os

class Downloader:

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        
    
    def multipartFileDownloader(self):
        try:
            file_path = self.file_path

            if os.path.isdir(file_path) == False:
                os.makedirs(file_path)

            # 사전인증 S3 POST URL 생성하기
            client = boto3.client(
                's3',
                aws_access_key_id=os.environ.get('access_key'),
                aws_secret_access_key=os.environ.get('secret_key'),
                region_name=os.environ.get('region_name')
            )

            config = TransferConfig(
                multipart_threshold=1024 * 25,
                max_concurrency=10,
                multipart_chunksize=1024 * 25,
                use_threads=True
            )
            

            client.download_file(
                os.environ.get('bucket_name'),
                file_path,  # 파일의 키를 지정합니다.
                'tmp/'+file_path,  # 로컬에 저장될 파일 경로 및 이름을 지정합니다.
                config  
            )

        except Exception as e :
            raise Exception(e)
        
        