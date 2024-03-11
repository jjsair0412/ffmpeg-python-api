from dotenv import load_dotenv
import requests
from encoders.storageAccessManager.presignedUrlGenerator import createUrl

class awsStorageAccess:
    def __init__(self,  target_file, obejct_name):
        self.target_file = target_file
        self.obejct_name = obejct_name

    def streamingUpload(self) -> str:
        load_dotenv(dotenv_path='./config/.env')
        target_file = self.target_file
        object_name = self.obejct_name

        url_generator = createUrl(
            object_name,
            # fields={'acl': 'public-read', 'Content-Type': "application/octet-stream"},
            # conditions=[{'acl': 'public-read'},{'Content-Type':"application/octet-stream"}],
            # fields={'acl': 'public-read'},
            # conditions=[{'acl': 'public-read'}],
            # fields={"Content-Type": "application/octet-stream"},
            # conditions=["starts-with", "$Content-Type", "application/"],                                        
            # expiration=3600
        )

        response = url_generator.create_presigned_post()

        if response is None:
            exit(1)

        response = requests.post(response['url'],data=response['fields'], files=target_file)
        return response.status_code
