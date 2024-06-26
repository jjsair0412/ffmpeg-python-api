from dotenv import load_dotenv
import os
import subprocess
from .dto.MetaDataDto import MetadataDto
import json

class metadata:

    def __init__(self, tmp_path):
        self.tmp_path = tmp_path

    def createMetadata(self) -> str:
        load_dotenv(dotenv_path='./config/.env')
        ffprobe_path = os.environ.get('ffprobe_path')
        tmp_path = self.tmp_path
        metaDto = self.getMetaData(ffprobe_path, tmp_path)
        return metaDto


    @staticmethod
    def getMetaData(ffprobe_path, tmp_path) -> dict:
        cmd = [
            ffprobe_path,
            '-v', 'quiet',
            '-print_format','json',
            '-show_format',
            '-show_streams',
            tmp_path
        ]  
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        metadata = json.loads(result.stdout)
        # 추출된 메타데이터에서 필요한 정보 파싱
        format_info = metadata.get('format', {})
        video_stream = next((stream for stream in metadata.get('streams', []) if stream.get('codec_type') == 'video'), None)
        audio_stream = next((stream for stream in metadata.get('streams', []) if stream.get('codec_type') == 'audio'), None)

        data =  MetadataDto(
            format_long_name=format_info.get('format_long_name'),
            duration_in_seconds=float(format_info.get('duration', 0)),
            size=int(format_info.get('size', 0)),
            bit_rate=int(format_info.get('bit_rate', 0)),
            codec_name=video_stream.get('codec_name') if video_stream else None,
            width=int(video_stream.get('width', 0)) if video_stream else None,
            height=int(video_stream.get('height', 0)) if video_stream else None,
            channels=int(audio_stream.get('channels', 0)) if audio_stream else None,
            r_frame_rate=video_stream.get('r_frame_rate') if video_stream else None
        )
        
        return data.to_dict()
        



        
        
    