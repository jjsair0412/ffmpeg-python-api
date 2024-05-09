from flask import Flask, request
from encoders.NewCreateStreamingChunk import newCreateStreaming
from encoders.NewCreatePreviewImage import newCreatePreviewImage
from encoders.file_type import FileType
from encoders.ThumbnailEncoder import ThumbnailEncoder
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader
import os


# Flask 앱 정의
app = Flask(__name__)

# health check api
@app.route('/health',methods=['GET'])
def health_check():
    return "ok"

@app.route('/ready',methods=['GET'])
def ready_check():
    return "ok"


@app.route('/thumbnail', methods=['POST'])
def new_create_thumbnail():
    
    request_data = request.json
    file_name = request_data['fileName']
    file_path = request_data['filePath']
    file_type = request_data['fileType']


    if file_type == FileType.IMAGE.name:
        create_thumbnail = ThumbnailEncoder(file_name, file_path, FileType.IMAGE)
        return_value = create_thumbnail.createThumbnail();
        return return_value
    elif file_type == FileType.VIDEO.name:
        create_thumbnail = ThumbnailEncoder(file_name, file_path, FileType.VIDEO)
        return_value = create_thumbnail.createThumbnail()
        return return_value
    else:
        return "create_thumbnail is fail" , 500


@app.route('/streaming', methods=['POST'])
def create_streaming_chunk():
    
    save_file_name = request.form['saveFileName']
    origin_file_name = request.form['originFileName']
    uploadPath = request.form['uploadPath']
    contentName = request.form['contentName']

    save_waterMark_path = downloadWaterMark()

    create_streaming = newCreateStreaming(uploadPath, contentName, origin_file_name, save_file_name, save_waterMark_path)

    return create_streaming.createVideoChunk()



@app.route('/previewImage', methods=['POST'])
def create_preview_image():
    
    save_file_name = request.form['saveFileName']
    origin_file_name = request.form['originFileName']
    previewPath = request.form['previewPath']

    save_waterMark_path = downloadWaterMark()

    create_preview_image = newCreatePreviewImage(previewPath, origin_file_name, save_file_name, save_waterMark_path)

    return create_preview_image.createImageChunk()


@staticmethod
def downloadWaterMark() -> str:
    file_downloader = Downloader(
        file_path=os.environ.get('waterMark_path'),
        file_name=os.environ.get('waterMark_name'),
        sample_file_path=os.environ.get('waterMark_save_path'),
        bucket_name=os.environ.get('etc_bucket_name')
        )
    file_downloader.multipartFileDownloader()

    save_waterMark_path = os.path.join(
            os.environ.get('waterMark_save_path'),
            os.environ.get('waterMark_name')
    )

    return save_waterMark_path
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)