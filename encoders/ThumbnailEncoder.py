from .file_type import FileType
from encoders.storageAccessManager.awsMultipartFileDownloader import Downloader
from encoders.CreateMetadata import metadata

import shutil
import os
import ffmpeg
import base64 as bs

class ThumbnailEncoder:
    
    def __init__(self, file_name, file_path, file_type, save_waterMark_path):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.save_waterMark_path = save_waterMark_path

    def createThumbnail(self) -> dict:

        file_name = self.file_name
        file_path = self.file_path
        
        # 썸네일 , 메타데이터 추출용 파일 설치경로 
        sample_file_path = os.path.join('tmp', file_path)
        # 실제파일명 포함 저장경로
        tmp_path = os.path.join(sample_file_path, file_name)

        # 파일 로컬에 저장 (경로는 tmp/download/manifest/년/월/일/유저_ID/UUID_포함_파일명)
        file_downloader = Downloader(
            file_path=file_path,
            file_name=file_name,
            sample_file_path=sample_file_path,
            bucket_name=os.environ.get('contents_bucket_name')
            )
        
        file_downloader.multipartFileDownloader()
        

        saveThumbnailName = file_name

        # 생성된 썸네일 저장 경로
        outPutFilePath = sample_file_path.replace('download','thumbnail')
        if not os.path.exists(outPutFilePath):
            os.makedirs(outPutFilePath)

        save_waterMark_path = self.save_waterMark_path

        thumbnailMetaDic = {}

        match self.file_type:   
            case FileType.IMAGE: # image
                base_image_dict = self.imageThumbnailMaker(tmp_path, save_waterMark_path, outPutFilePath, saveThumbnailName)
                thumbnailMetaDic['thumbnail'] = base_image_dict

            
            case FileType.VIDEO: # video
                video_duration = self.get_video_duration(tmp_path)
                output_paths = self.videoThumbnailMaker(tmp_path, save_waterMark_path, video_duration, outPutFilePath, saveThumbnailName)
                video_thumbnail_dict = self.loadImages(output_paths)
                thumbnailMetaDic['thumbnail'] = video_thumbnail_dict
            
            case _ :
                print('file type is not match')
                os.remove(tmp_path)
                shutil.rmtree(outPutFilePath)
                return 500
            
        get_meta_data = metadata(tmp_path=tmp_path)
        thumbnailMetaDic['metadata'] = get_meta_data.createMetadata()
        os.remove(tmp_path)
        os.remove(save_waterMark_path)
        shutil.rmtree(outPutFilePath)

        return thumbnailMetaDic
        
        
                
    
    @staticmethod
    def videoThumbnailMaker(file_path, waterMark_path, videoDuration, outPutFilePath, saveThumbnailName) -> list:

        fractions = {0.2, 0.4, 0.6, 0.8}
        thumbnail_paths=[]

        for fraction in fractions:

            thumbnail_name = str(fraction) + "_"+ saveThumbnailName+".jpeg"
            output_path = os.path.join(outPutFilePath, thumbnail_name)

            if videoDuration < 3:
                midTime = videoDuration * 1000 / 2
                # ffmpeg.input(file_path, ss=midTime)\
                #     .output(output_path, vframes=1, vf='scale=1280:720')\
                #     .run()
                # OLD (해상도 고정)
                
                # ffmpeg.input(file_path, ss=midTime)\
                #     .output(output_path, vframes=1, crf=51, **{'c:a': 'copy'})\
                #     .run()

                ffmpeg.input(file_path, ss=midTime)\
                    .output(output_path, vframes=1, **{'qscale:v': 31})\
                    .global_args(
                        '-i',waterMark_path, 
                        '-filter_complex', '[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p'
                        )\
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
                        .output(output_path, vframes=1, **{'qscale:v': 31})\
                        .global_args(
                            '-i',waterMark_path, 
                            '-filter_complex', '[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p'
                            )\
                        .run()

            
            thumbnail_paths.append(output_path)

        return thumbnail_paths


    @staticmethod
    def imageThumbnailMaker(file_path, waterMark_path, outPutFilePath, saveThumbnailName) -> str:

        # output_path = os.path.join('.' + outPutFilePath ,saveThumbnailName+".PNG")
        output_path = os.path.join(outPutFilePath ,saveThumbnailName+".jpeg")

        # ffmpeg.input(file_path)\
        #     .output(output_path, vframes=1, vf='scale=1280:720')\
        #     .run()
        

        # ffmpeg.input(file_path)\
        #     .output(output_path, vframes=1, crf=51, c='copy', **{'c:a': 'copy'})\
        #     .run()

        ffmpeg.input(file_path)\
            .output(output_path, vframes=1, **{'qscale:v': 31})\
            .global_args(
                '-i',waterMark_path, 
                '-filter_complex', '[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p'
                )\
            .run()

        with open(output_path, 'rb') as file:
            file_bytes = file.read()
            base_images = bs.b64encode(file_bytes).decode('utf-8')
        
        return {'0':base_images}


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