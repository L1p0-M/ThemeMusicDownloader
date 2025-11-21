FROM python:3.13.9-slim-bookworm
RUN mkdir /app
ADD downloadthemes.py /app
RUN pip install requests yt_dlp
RUN apt-get update && apt-get upgrade -y && apt-get install -y ffmpeg 
RUN mkdir /movies
EXPOSE 8000
WORKDIR /movies
CMD python /app/downloadthemes.py /movies
