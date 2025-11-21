# ThemeMusicDownloader

Example docker-compose.yaml:

```
services:
  thememusicdownloader:
    image: thememusicdownloader:latest
    container_name: ThemeMusicDownloader
    environment:
      - TOKEN=*tmdbtoken*
    volumes:
      - /home/user/movies:/movies
```