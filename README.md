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
      - /mnt/hdd1/movies:/movies/hdd1
      - /mnt/hdd2/movies:/movies/hdd2
```