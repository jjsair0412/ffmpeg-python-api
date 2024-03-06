# ffmpeg encoder api
python with ffmpeg encoder

## api reference
- python version : Python 3.11.4

## Requirements Options
### 1. ffmpeg install
- **출처:** 
    - https://yy8305.tistory.com/48 [인생을 바꾸는 기록:티스토리]
ubuntu 22:04 에서 수행

```bash
$ sudo apt-get update -qq && sudo apt-get -y install \
    autoconf \
    automake \
    build-essential \
    cmake \
    git-core \
    libass-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    pkg-config \
    texinfo \
    wget \
    yasm \
    zlib1g-dev

$ mkdir -p ~/ffmpeg_sources ~/bin

$ sudo apt-get install nasm

$ sudo apt-get install libx264-dev

$ sudo apt-get install libx265-dev libnuma-dev

$ sudo apt-get install libvpx-dev

$ sudo apt-get install libfdk-aac-dev

$ sudo apt-get install libmp3lame-dev

$ sudo apt-get install libopus-dev

$ cd ~/ffmpeg_sources && \
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
tar xjvf ffmpeg-snapshot.tar.bz2 && \
cd ffmpeg && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree && \
PATH="$HOME/bin:$PATH" make && \
make install && \
hash -r

$ echo "MANPATH_MAP $HOME/bin $HOME/ffmpeg_build/share/man" >> ~/.manpath

# ~/bin 에 있는거 /usr/local/bin 으로 복사
$ cp ~/bin/* /usr/local/bin/
```

### 2. import packages
- download target module : 
  - ffmpeg-python
  - flask
```bash
pip3 install -r requirements.txt
```

### 3. config.ini 파일 생성
```bash
cat <<EOF> ./config/config.ini
[kakao_icloud]
projectId = {project_id}
bucketName = {bucket_name}
regionName = {region_name}


[path]
chunkUploadTargetUrl = {chunk_upload_path}
previewOrThumbnailUploadTargetUrl = {preview_upload_path}

[ffmpeg]
ffprobe_path = {ffprobe_path}
EOF
```


## Function List
### 1. health check

#### Request Syntax
```bash
curl http://127.0.0.1:5000/health
```
#### Response Syntax
```bash
ok
```

#### Request Syntax
```bash
curl http://127.0.0.1:5000/ready
```
#### Response Syntax
```bash
ok
```

### 2. thumbnail 생성
#### Request Syntax

### 3. file metadata 추출
#### Request Syntax

### 4. streaming chunk 추출
#### Request Syntax

### 5. preview Image 추출
#### Request Syntax

## Docker Run
### Docker build command
```bash
docker build -t ffmpeg-api:{tag} . \
  --build-arg "projectId={projectId}" \
  --build-arg "bucketName={bucketName}" \
  --build-arg "regionName={regionName}" \
  --build-arg "chunkUploadTargetUrl={chunkUploadTargetUrl}" \
  --build-arg "ffprobe_path=/usr/local/bin/ffprobe"
```
