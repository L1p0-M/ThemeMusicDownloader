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
      - /mnt/hdd3/series:/series/hdd3
      - /dockerconfig/thememusicdownloader/config:/config
```

Run the script once, and check the config folder for the *Notfound.txt* file!
You are gonna see a list with the names of the movies... You need to paste the youtube link manually after the ":", like this:

```
How to Train Your Dragon (2010): https://www.youtube.com/watch?v=IpPIK4T068s
One Battle After Another (2025): https://youtu.be/YzhjTeSz9y4?si=M23WZaepQCUt7TN5
```

Rerun the container,and its gonna download all specified music :)

To do:
update yt-dlp :/