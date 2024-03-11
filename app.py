from flask import Flask, request
from encoders.CreateMetadata import metadata
from encoders.ThumbnailEncoder import thumbnailEncoder
from encoders.CreateStreamingChunk import createStreaming
from encoders.file_type import FileType
from encoders.CreatePreviewImage import createPreviewImage

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
def create_thumbnail():
    if 'file' not in request.files:
        return 'no file part', 400
    file = request.files['file']
    type = request.form['fileType']
    saveThumbnailName = request.form['saveThumbnailName']
    outPutFilePath = request.form['outPutFilePath']

    if type == FileType.IMAGE.name:
        create_thumbnail = thumbnailEncoder(file, FileType.IMAGE, saveThumbnailName, outPutFilePath)
        return create_thumbnail.createThumbnail()
    elif type == FileType.VIDEO.name:
        create_thumbnail = thumbnailEncoder(file, FileType.VIDEO, saveThumbnailName, outPutFilePath)
        return create_thumbnail.createThumbnail()
    else:
        return "create_thumbnail is fail" , 500
    

@app.route('/metadata', methods=['POST'])
def create_file_metadata():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    create_file_metadata = metadata(file)

    return create_file_metadata.createMetadata()


@app.route('/streaming', methods=['POST'])
def create_streaming_chunk():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    uploadPath = request.form['uploadPath']
    contentName = request.form['contentName']

    create_streaming = createStreaming(file, uploadPath, contentName)

    return create_streaming.createVideoChunk()



@app.route('/previewImage', methods=['POST'])
def create_preview_image():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    previewPath = request.form['previewPath']
    originName = request.form['originName']

    create_preview_image = createPreviewImage(file, previewPath, originName)

    return create_preview_image.createImageChunk()



if __name__ == '__main__':
    app.run(port=5000, debug=True)