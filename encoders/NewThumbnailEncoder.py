from werkzeug.datastructures import FileStorage
from .file_type import FileType
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader

import shutil
import os
import ffmpeg
import base64 as bs

class newThumbnailEncoder:
    
    def __init__(self, file_name, file_path, file_type):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type

    def createThumbnail(self) -> dict:

        file_name = self.file_name
        file_path = self.file_path

        # 파일 로컬에 저장 (경로는 tmp/download/manifest/년/월/일/유저_ID/UUID_포함_파일명)
        file_downloader = Downloader(file_path=file_path)
        file_downloader.multipartFileDownloader()
        

        saveThumbnailName = file_name
        outPutFilePath = file_path.replace(
            old = 'download',
            new = 'thumbnail'
        )

        tmp_path = os.path.join(outPutFilePath, saveThumbnailName)


        match self.file_type :   
            case FileType.IMAGE: # image
                base_image_dic = self.imageThumbnailMaker(tmp_path, outPutFilePath, saveThumbnailName)
                os.remove(tmp_path)
                # shutil.rmtree("."+outPutFilePath)
                shutil.rmtree(outPutFilePath)
                return base_image_dic

            
            case FileType.VIDEO: # video
                video_duration = self.get_video_duration(tmp_path)
                output_paths = self.videoThumbnailMaker(tmp_path, video_duration, outPutFilePath, saveThumbnailName)
                video_thumbnail_dict = self.loadImages(output_paths)
                os.remove(tmp_path)
                # shutil.rmtree("."+outPutFilePath)
                shutil.rmtree(outPutFilePath)
                return video_thumbnail_dict
            
            case _ :
                print('file type is not match')
                os.remove(tmp_path)
                # shutil.rmtree("."+outPutFilePath)
                shutil.rmtree(outPutFilePath)
                return 500
                
    
    @staticmethod
    def videoThumbnailMaker(file_path, videoDuration, outPutFilePath, saveThumbnailName) -> list:

        fractions = {0.2, 0.4, 0.6, 0.8}
        thumbnail_paths=[]

        for fraction in fractions:

            thumbnail_name = str(fraction) + "_"+ saveThumbnailName+".jpeg"
            # output_path = os.path.join('.' + outPutFilePath, thumbnail_name)
            output_path = os.path.join(outPutFilePath, thumbnail_name)

            if videoDuration < 3:
                midTime = videoDuration * 1000 / 2
                # ffmpeg.input(file_path, ss=midTime)\
                #     .output(output_path, vframes=1, vf='scale=1280:720')\
                #     .run()
                # OLD (해상도 고정)
                
                ffmpeg.input(file_path, ss=midTime)\
                    .output(output_path, vframes=1,crf=63, **{'c:a': 'copy'})\
                    .run()
            
            else :
                    # start_offsets = []
                    start_offset = float(videoDuration * fraction * 1000 - 500)
                    # start_offsets.append(start_offset)

                    # ffmpeg.input(file_path, ss=(start_offset / 1000))\
                    #     .output(output_path, vframes=1, vf='scale=1280:720', acodec='copy')\
                    #     .run()
                    # OLD (해상도 고정)

                    ffmpeg.input(file_path, ss=(start_offset / 1000))\
                        .output(output_path, vframes=1 ,crf=63, **{'c:a': 'copy'})\
                        .run()

            
            thumbnail_paths.append(output_path)

        return thumbnail_paths


    @staticmethod
    def imageThumbnailMaker(file_path, outPutFilePath, saveThumbnailName) -> dict:

        # output_path = os.path.join('.' + outPutFilePath ,saveThumbnailName+".PNG")
        output_path = os.path.join(outPutFilePath ,saveThumbnailName+".jpeg")

        # ffmpeg.input(file_path)\
        #     .output(output_path, vframes=1, vf='scale=1280:720')\
        #     .run()
        


        ffmpeg.input(file_path)\
            .output(output_path, vframes=1, crf=51, c='copy', **{'c:a': 'copy'})\
            .run()

        with open(output_path, 'rb') as file:
            file_bytes = file.read()
            base_images = bs.b64encode(file_bytes).decode('utf-8')
        
        return base_images


    @staticmethod
    def get_video_duration(file) -> float:
        probe = ffmpeg.probe(file)
        duration = float(probe['streams'][0]['duration'])
        return duration
                

    @staticmethod
    def loadImages(imagesList) -> dict:
        base_images = {}
        count = 0

        for path in imagesList:
            with open(path, 'rb') as file:
                file_byte = file.read()
                base_images[count] = bs.b64encode(file_byte).decode('utf-8')
            
            count+=1

        return base_images