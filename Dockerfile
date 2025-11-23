FROM python:3.13.9-alpine
RUN mkdir /app
ADD downloadthemes.py /app
RUN pip install requests yt_dlp
RUN apk --no-cache add ffmpeg
RUN mkdir /movies
RUN mkdir /config
WORKDIR /movies
CMD python /app/downloadthemes.py /movies
