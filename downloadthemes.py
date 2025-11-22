import requests
import json
import os
import sys, getopt
import yt_dlp

try:
    print("arg1= ", sys.argv[1])
    maindir = sys.argv[1]
except IndexError as e:
    print("Adja meg a filmek helyét!")
    raise e

if "TOKEN" not in os.environ:
    try:
        api_key = sys.argv[2]
    except IndexError as e:
        print("Adjon meg egy TMDB api kulcsot!")
        raise e
else:
    print(os.environ["TOKEN"])
    api_key = os.environ["TOKEN"]

TMDB_API_KEY = api_key

def check_folders(maindir):
    hdds = os.listdir(maindir)
    return hdds


def get_titles(location):
    dirs = os.listdir(location)
    print(dirs)
    return dirs

def get_tmdb_id(title):
    """Lekéri a film TMDb ID-ját a cím alapján."""
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    response = requests.get(url, params=params)
    data = response.json()

    if not data["results"]:
        print("Nincs találat a TMDb-ben erre a címre.")
        return None

    movie_id = data["results"][0]["id"]
    movie_name = data["results"][0]["title"]
    print(f"🎬 {movie_name} (TMDb ID: {movie_id})")
    return movie_id


def get_themerrdb_theme(tmdb_id):
    """Lekéri a ThemerrDB-ből a témazenét YouTube-linkkel."""
    url = f"https://raw.githubusercontent.com/LizardByte/ThemerrDB/refs/heads/database/movies/themoviedb/{tmdb_id}.json"
    response = requests.get(url)

    if response.status_code != 200:
        print("Nem található témaadat a ThemerrDB-ben.")
        return None
    
    else:
        context = json.loads(response.text)
        youtube_link = context["youtube_theme_url"]
        print(f"Témazene link: {youtube_link}")
        return youtube_link

def downloadtheme(theme_url, location, name):
    print(f"Témazene letöltése: {theme_url}")
    cmd = f"yt-dlp -x --audio-format mp3 -o {location}/'{name}'/theme.mp3 {theme_url}"
    print(cmd)
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': f'{location}/{name}/theme.%(ext)s',
        'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            error_code = ydl.download(theme_url)
        except:
            print("nem sikerült letölteni :(")

def get_clean_name(dirname):
    title_split = dirname.split()
    del title_split[-1]
    print(title_split)
    title_clean = ' '.join(title_split)
    print(title_clean)
    return title_clean
    
def main():
    hdds = check_folders(maindir)
    for h in hdds:
        location = f"{maindir}/{h}"
        dir = get_titles(location)
        print(dir)
        for t in dir:
            print(t)
            if not "theme.mp3" in os.listdir(f"{location}/{t}"):
                print("Témazene Keresése...")
                title_clean = get_clean_name(t)
                tmdb_id = get_tmdb_id(title_clean)
                if tmdb_id:
                    theme_url = get_themerrdb_theme(tmdb_id)
                    if theme_url:
                        downloadtheme(theme_url, location, t)
                    else:
                        print("Nem volt találat az adatbázisban!")
                        notfound=[]
                        notfound.append(t)
                        print(notfound)
                        #inputlink = input(f"Adjon meg egy youtube linket a {title_clean} zenéjéhez:")
                        #if inputlink:
                            #downloadtheme(inputlink, location, t)
                        #else:
                            #print(f"A {title_clean} zenéje nem lesz letöltve")
                else:
                    print("Nem volt találat az adatbázisban!")
            else:
                print(f"A témazene már elérhető a {t}-hez")
    
if __name__ == "__main__":
    main()
