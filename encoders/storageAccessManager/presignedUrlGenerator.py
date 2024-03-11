import logging
import boto3
from botocore.exceptions import ClientError
import os


class createUrl:

    def __init__(self, object_name, fields=None, conditions= None,  expiration=3600) -> None:
        self.object_name = object_name
        self.fields = fields
        self.conditions = conditions
        self.expiration = expiration

    def create_presigned_post(self):

        """ 파일을 업로드하기 위한 사전인증 URL S3 POST 요청 생성하기
        
        :param bucket_name: 문자열
        :param object_name: 문자열
        :param fields: 미리채워진 양식필드 딕셔너리
        :param conditions: 정책에 포함할 조건 목록
        :param expiration: 사전인증 URL이 유효한 시간(초)
        :return: 아래의 키를 가진 딕셔너리
            url: POST 요청 URL
            fields: POST와 함께 제출될 양식 항목과 값의 딕셔너리
        :return : 오류시 None
        """
        
        # 사전인증 S3 POST URL 생성하기
        s3_client =  boto3.client(
                's3',
                aws_access_key_id = os.environ.get('access_key'),
                aws_secret_access_key = os.environ.get('secret_key'),
                region_name = os.environ.get('region_name')
        )


        try:
            bucket_name = os.environ.get('bucket_name')
            response = s3_client.generate_presigned_post(
                bucket_name,
                self.object_name,
                Fields=self.fields,
                Conditions=self.conditions,
                ExpiresIn=self.expiration
            )
            
        except ClientError as e:
            print('prisignedUrl 생성 시 에러 발생 :' , e)
            logging.error(e)
            return None
    
            
        # 사전인증 URL과 요구되는 항목을 포함한 응답
        return response