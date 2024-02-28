import configparser
import requests

class storageAccess:
    def __init__(self, xAuthToken, uploadPath, fileName, contentType):
        self.xAuthToken = xAuthToken
        self.uploadPath = uploadPath
        self.fileName = fileName
        self.contentType = contentType

    def thumbnailUpload(self):

        config = configparser.ConfigParser()
        config.read('./config/config.ini', encoding='utf-8')
        
        thumbnailPath = config['path']['previewOrThumbnailUploadTargetUrl']

        url = thumbnailPath.format (
            region_name=config['kakao_icloud']['regionName'],
            projectID=['kakao_icloud']['projectID'],
            bucket_name=['kakao_icloud']['bucketName'],
            path=self.uploadPath,
            file=self.fileName
        )

        header = {
            "X-Auth-Token": self.xAuthToken,
            "Content-Type": self.contentType
        }
        
        response = requests.post(url, headers=header)

        print(response.status_code)
        print(response.text)

    def streamingChunkUpload(self):
        pass