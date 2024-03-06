from dotenv import load_dotenv
import requests
import os

class storageAccess:
    def __init__(self, xAuthToken, uploadPathFileName, contentType, targetFile):
        self.xAuthToken = xAuthToken
        self.uploadPathFileName = uploadPathFileName
        self.contentType = contentType
        self.targetFile = targetFile

    def streamingUpload(self):
        load_dotenv(dotenv_path='./config/.env')
        
        targetFile = self.targetFile

        streamingPath = os.environ.get('chunkUploadTargetUrl')

        url = streamingPath.format (
            projectID=os.environ.get('projectId'),
            bucket_name=os.environ.get('bucketName'),
            uploadPathFileName=self.uploadPathFileName
        )

        header = {
            "X-Auth-Token": self.xAuthToken,
            "Content-Type": self.contentType
        }

        response = requests.put(url, headers=header, data=targetFile)

        print(response.status_code)
        print(response.text)
