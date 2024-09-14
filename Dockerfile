FROM public.ecr.aws/lambda/python:3.10
RUN pip install boto3 google-generativeai httplib2 moviepy oauth2client pexels-api-py pillow requests imageio imageio-ffmpeg google-api-python-client
COPY main.py ./
COPY publisher.py ./
COPY assets/* ./assets/*
COPY builder.py ./
COPY upload_video.py ./
COPY apikeys.py ./
COPY client_secrets.json ./
COPY main.py-oauth2.json ./
COPY Lato-Black.ttf ./

RUN yum update \
    && yum install -qq -y wget rpm tar ffmpeg, ImageMagick\
    && yum clean all
# ffmpeg libmagick++-dev
# RUN mkdir -p /tmp/distr && \
#     cd /tmp/distr && \
#     wget https://imagemagick.org/archive/linux/CentOS/x86_64/ImageMagick-7.1.1-38.x86_64.rpm && \
#     rpm -Uvh ImageMagick-7.1.1-38.x86_64.rpm && \
#     rpm -Uvh ImageMagick-libs-7.1.1-38.x86_64.rpm \
#     cd ImageMagick-7.1.1-38.x86_64 && \
#     tar xvzf ImageMagick.tar.gz &&\
#     export MAGICK_HOME="$HOME/ImageMagick-7.1.1" && \
#     export PATH="$MAGICK_HOME/bin:$PATH" && \
#     LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$MAGICK_HOME/lib" &&\
#     export LD_LIBRARY_PATH \
#     ./configure --enable-shared=yes --disable-static --without-perl && \
#     make && \
#     make install && \
#     ldconfig /usr/local/lib && \
#     cd /tmp && \
#     rm -rf distr

CMD ["main.lambda_handler"]