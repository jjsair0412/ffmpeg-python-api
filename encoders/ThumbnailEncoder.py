from werkzeug.datastructures import FileStorage
from .file_type import FileType

import os
import ffmpeg
import base64 as bs

class thumbnailEncoder:
    
    def __init__(self, targetFile, fileType):
        self.targetFile = targetFile
        self.fileType = fileType

    # python에서 json은 dict type 이다.
    def createThumbnail(self) -> dict:
        if isinstance(self.targetFile, FileStorage):
            tmp_path = os.path.join('./tmp',self.targetFile.filename)
            self.targetFile.save(tmp_path)


            match self.fileType :   
                case FileType.IMAGE: # image
                    output_path = self.imageThumbnailMaker(tmp_path)
                    os.remove(tmp_path)
                    return self.loadImages(output_path)

                
                case FileType.VIDEO: # video
                    video_duration = self.get_video_duration(tmp_path)
                    output_paths = self.videoThumbnailMaker(video_duration, tmp_path)
                    os.remove(tmp_path)
                    return self.loadImages(output_paths)
                
                case _ :
                    print('file type is not match')
                    os.remove(tmp_path)
                    return 500
                    
        else:
            print("callCreate Thumbnail: Value not found or self.targetFile is not a dict")        
            return 500
    
    @staticmethod
    def videoThumbnailMaker(videoDuration, file_path) -> list:

        fractions = {0.2, 0.4, 0.6, 0.8}
        thumbnail_paths=[]

        for fraction in fractions:

            thumbnail_name = "output_thumbnail_"  + str(fraction) + ".jpeg"  # 예시 파일명, 실제 적용 필요
            output_path = os.path.join('./tmp', thumbnail_name)

            if videoDuration < 3:
                midTime = videoDuration * 1000 / 2
                ffmpeg.input(file_path, ss=midTime)\
                    .output(output_path, vframes=1, vf='scale=1280:720')\
                    .run()
            
            else :
                    # start_offsets = []
                    start_offset = float(videoDuration * fraction * 1000 - 500)
                    # start_offsets.append(start_offset)

                    ffmpeg.input(file_path, ss=(start_offset / 1000))\
                        .output(output_path, vframes=1, vf='scale=1280:720', acodec='copy')\
                        .run()
            
            thumbnail_paths.append(output_path)

        return thumbnail_paths


    @staticmethod
    def imageThumbnailMaker(file_path) -> str:

        thumbnail_name = "output_thumbnail.png"

        output_path = os.path.join('./tmp',thumbnail_name)

        ffmpeg.input(file_path)\
            .output(output_path, vframes=1, vf='scale=1280:720')\
            .run()

        return output_path


    @staticmethod
    def get_video_duration(file) -> float:
        probe = ffmpeg.probe(file)
        duration = float(probe['streams'][0]['duration'])
        return duration
                

    @staticmethod
    def loadImages(imagesList) -> list:
        base_images = {}
        count = 0
        for path in imagesList:
            with open(path, 'rb') as file:
                file_byte = file.read()
                base_images[count] = bs.b64encode(file_byte).decode('utf-8')
            
            os.remove(path)
            count+=1

        return base_images