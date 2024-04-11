from flask import Flask, request
from encoders.CreateMetadata import metadata
from encoders.CreateStreamingChunk import createStreaming
from encoders.NewCreateStreamingChunk import newCreateStreaming
from encoders.NewCreatePreviewImage import newCreatePreviewImage
from encoders.file_type import FileType
from encoders.CreatePreviewImage import createPreviewImage
from encoders.ThumbnailEncoder import ThumbnailEncoder


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


# @app.route('/metadata', methods=['POST'])
# def create_file_metadata():
#     if 'file' not in request.files:
#         return 'no file part', 400
    
#     file = request.files['file']
#     create_file_metadata = metadata(file)

#     return create_file_metadata.createMetadata()


@app.route('/streaming_old', methods=['POST'])
def create_streaming_chunk_old():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    uploadPath = request.form['uploadPath']
    contentName = request.form['contentName']

    create_streaming = createStreaming(file, uploadPath, contentName)

    return create_streaming.createVideoChunk()

@app.route('/previewImage_old', methods=['POST'])
def create_preview_image_old():
    if 'file' not in request.files:
        return 'no file part', 400
    
    file = request.files['file']
    previewPath = request.form['previewPath']
    originName = request.form['originName']

    create_preview_image = createPreviewImage(file, previewPath, originName)

    return create_preview_image.createImageChunk()

@app.route('/streaming', methods=['POST'])
def create_streaming_chunk():
    
    save_file_name = request.form['saveFileName']
    origin_file_name = request.form['originFileName']
    uploadPath = request.form['uploadPath']
    contentName = request.form['contentName']

    create_streaming = newCreateStreaming(uploadPath, contentName, origin_file_name, save_file_name)

    return create_streaming.createVideoChunk()



@app.route('/previewImage', methods=['POST'])
def create_preview_image():
    
    save_file_name = request.form['saveFileName']
    origin_file_name = request.form['originFileName']
    previewPath = request.form['previewPath']
    originName = request.form['originName']

    create_preview_image = newCreatePreviewImage(previewPath, originName, origin_file_name, save_file_name)

    return create_preview_image.createImageChunk()



if __name__ == '__main__':
    app.run(port=5000, debug=True)