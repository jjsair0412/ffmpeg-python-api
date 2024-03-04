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

    if type == FileType.IMAGE.name:
        create_thumbnail = thumbnailEncoder(file,FileType.IMAGE)
        return create_thumbnail.createThumbnail()
    elif type == FileType.VIDEO.name:
        create_thumbnail = thumbnailEncoder(file,FileType.VIDEO)
        return create_thumbnail.createThumbnail()
    else:
        return "false" , 500
    

@app.route('/metadata', methods=['POST'])
def create_file_metadata():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    create_file_metadata = metadata(file,'/opt/homebrew/bin/ffprobe')

    return create_file_metadata.createMetadata()


@app.route('/streaming', methods=['POST'])
def create_streaming_chunk():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    tsSegmentPattern = request.form['tsSegmentPattern']
    outputFilePath = request.form['outputFilePath']
    xAuthToken = request.form['xAuthToken']

    create_streaming = createStreaming(file, tsSegmentPattern, outputFilePath)

    return create_streaming.createVideoChunk()


@app.route('/previewImage', methods=['POST'])
def create_preview_image():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    preview_image_path = request.form['preview_image_path']
    

    create_preview_image = createPreviewImage(file,preview_image_path)

    return create_preview_image.createImageChunk()



if __name__ == '__main__':
    app.run(port=5000, debug=True)