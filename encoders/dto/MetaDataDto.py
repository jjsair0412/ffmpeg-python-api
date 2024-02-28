class MetadataDto:
    def __init__(self, 
                 format_long_name, # 포멧의 긴 이름
                 duration_in_seconds, # 영상 길이 (초단위 출력)
                 size, # 영상 사이즈 (바이트단위)
                 bit_rate, # 비트레이트
                 codec_name, # 코덱 이름
                 width, # 해상도 가로 
                 height, # 해상도 세로
                 channels, # 오디오 채널 수
                 r_frame_rate # 프레임 레이트
                ):
        self.format_long_name = format_long_name
        self.duration_in_seconds = duration_in_seconds
        self.size = size
        self.bit_rate = bit_rate
        self.codec_name = codec_name
        self.width = width
        self.height = height
        self.channels = channels
        self.r_frame_rate = r_frame_rate

    # dictionary 변환
    def to_dict(self):
        return {
            "format_long_name": self.format_long_name,
            "duration_in_seconds": self.duration_in_seconds,
            "size": self.size,
            "bit_rate": self.bit_rate,
            "codec_name": self.codec_name,
            "width": self.width,
            "height": self.height,
            "channels": self.channels,
            "r_frame_rate": self.r_frame_rate,
        }

    @property
    def format_long_name(self):
        return self._format_long_name
    
    @format_long_name.setter
    def format_long_name(self, value):
        self._format_long_name = value
    
    @property
    def duration_in_seconds(self):
        return self._duration_in_seconds
    
    @duration_in_seconds.setter
    def duration_in_seconds(self, value):
        self._duration_in_seconds = value

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value

    @property
    def bit_rate(self):
        return self._bit_rate
    
    @bit_rate.setter
    def bit_rate(self, value):
        self._bit_rate = value

    
    @property
    def codec_name(self):
        return self._codec_name
    
    @codec_name.setter
    def codec_name(self, value):
        self._codec_name = value

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self,value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
    

    @property
    def channels(self):
        return self._channels
    
    @channels.setter
    def channels(self, value):
        self._channels = value

    @property
    def r_frame_rate(self):
        return self._r_frame_rate

    @r_frame_rate.setter
    def r_frame_rate(self , value):
        self._r_frame_rate = value
