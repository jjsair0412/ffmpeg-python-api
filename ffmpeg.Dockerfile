FROM python:3.11-slim

RUN mkdir /app
COPY ./bin/ffmpeg-snapshot.tar.bz2 /app
WORKDIR /app

RUN sed -i 's/main/main non-free/g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update -y

RUN apt-get update -qq && apt-get -y install \
    autoconf \
    automake \
    build-essential \
    cmake \
    curl \
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

RUN mkdir -p ~/ffmpeg_sources ~/bin

RUN apt-get install nasm

RUN apt-get install libx264-dev -y

RUN apt-get install libx265-dev libnuma-dev -y

RUN apt-get install libvpx-dev -y

# 안드로이드 인코딩 코덱 (비자유 , 라이센스 확인 필요)
RUN apt-get install libfdk-aac-dev -y

RUN apt-get install libmp3lame-dev -y

RUN apt-get install libopus-dev -y

RUN mv /app/ffmpeg-snapshot.tar.bz2 ~/ffmpeg_sources/
RUN cd ~/ffmpeg_sources && \
#    curl -o ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
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

RUN echo "MANPATH_MAP $HOME/bin $HOME/ffmpeg_build/share/man" >> ~/.manpath


# ~/bin 에 있는거 /usr/local/bin 으로 복사
RUN cp ~/bin/* /usr/local/bin/
