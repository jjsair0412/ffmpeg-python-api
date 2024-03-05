import configparser
import requests

class storageAccess:
    def __init__(self, xAuthToken, uploadPathFileName, contentType, targetFile):
        self.xAuthToken = xAuthToken
        self.uploadPathFileName = uploadPathFileName
        self.contentType = contentType
        self.targetFile = targetFile

    def streamingUpload(self):

        config = configparser.ConfigParser()
        config.read('./config/config.ini', encoding='utf-8')
        
        targetFile = self.targetFile

        streamingPath = config['path']['chunkUploadTargetUrl']

        url = streamingPath.format (
            projectID=config['kakao_icloud']['projectId'],
            bucket_name=config['kakao_icloud']['bucketName'],
            uploadPathFileName=self.uploadPathFileName
        )

        header = {
            "X-Auth-Token": self.xAuthToken,
            "Content-Type": self.contentType
        }

        response = requests.put(url, headers=header, data=targetFile)

        print(response.status_code)
        print(response.text)
