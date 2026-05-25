import requests
import json
import os
import sys, getopt
import yt_dlp

try:
    print("arg1= ", sys.argv[1])
    maindir = sys.argv[1]
    print("arg2= ", sys.argv[2])
    seriesdir = sys.argv[2]
    print("arg3= ", sys.argv[3])
    configdir = sys.argv[3]
except IndexError as e:
    print("Please give the movies/series folder as an argument")
    raise e

if "TOKEN" not in os.environ:
    try:
        api_key = sys.argv[4]
    except IndexError as e:
        print("Api key not found")
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

def get_tmdb_id(title, type):
    """Gets the tmdb id of the movie/serie"""
    url = f"https://api.themoviedb.org/3/search/{type}"
    params = {"api_key": TMDB_API_KEY, "query": title}
    response = requests.get(url, params=params)
    data = response.json()

    if not data["results"]:
        print("Not found in tmdb.")
        return None

    movie_id = data["results"][0]["id"]
    #movie_name = data["results"][0]["title"]
    print(f"{title} (TMDb ID: {movie_id})")
    return movie_id


def get_themerrdb_theme(tmdb_id, type):
    """Gets the youtube link from themerrdb"""
    url = f"https://raw.githubusercontent.com/LizardByte/ThemerrDB/refs/heads/database/{type}/themoviedb/{tmdb_id}.json"
    response = requests.get(url)

    if response.status_code != 200:
        print("No data found in themerrdb")
        return None
    
    else:
        context = json.loads(response.text)
        youtube_link = context["youtube_theme_url"]
        print(f"Témazene link: {youtube_link}")
        return youtube_link

def downloadtheme(theme_url, location, name):
    print(f"Downloading from: {theme_url}")
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
            print("Cant download theme music :(")
            return "fail"

def get_clean_name(dirname):
    title_split = dirname.split()
    del title_split[-1]
    print(title_split)
    title_clean = ' '.join(title_split)
    print(title_clean)
    return title_clean

def writeconfig(title):
    try:
        with open(f'{configdir}/notfound.txt', 'a') as f:
            f.write(f"{title}\n")
            return "sucess"
    except Exception as e:
        print(f"Error while writing file: {e}")
        return "fail"
    
def checkconfig(title):
    try:
        with open(f'{configdir}/notfound.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if title in line:
                    print(line)
                    print("Title is already in notfound.txt")
                    return True
                else:
                    pass
                if line == lines[-1]:
                    return False
    except FileNotFoundError:
        print("Creating notfound.txt")
        with open(f'{configdir}/notfound.txt', 'w') as f:
            pass
    
def processlink(title):
    try:
        with open(f'{configdir}/notfound.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if title in line:
                    link = line.replace(f"{title}", "")
                    print(link)
                    if link != "":
                        return link
                    else:
                        return None
                
    except Exception as e:
        print(f"Error while reading file: {e}")
        return None

def processnotfounds(t, location):
    is_in_config = checkconfig(f"{t}:")
    if is_in_config:
        link = processlink(f"{t}: ")
        if link:
            downloadtheme(link, location, t)
    else:
        configsucess = writeconfig(f"{t}:")
        if configsucess == "sucess":
            print("Title added to notfound.txt")
        else:
            print("Error while writing to notfound.txt")

def process_series():
    hdds = check_folders(seriesdir)
    for h in hdds:
        location = f"{seriesdir}/{h}"
        dir = get_titles(location)
        print(dir)
        for t in dir:
            print(t)
            if not "theme.mp3" in os.listdir(f"{location}/{t}"):
                print("Searchimg for theme music...")
                title_clean = t
                tmdb_id = get_tmdb_id(title_clean, "tv")
                if tmdb_id:
                    theme_url = get_themerrdb_theme(tmdb_id, "tv_shows")
                    if theme_url:
                        is_sucessfull = downloadtheme(theme_url, location, t)
                        if is_sucessfull == "fail":
                            print("Hiba történt a letöltés során.")
                            processnotfounds(t, location)
                    else:
                        processnotfounds(t, location)
                        
                else:
                    print("Not found in database")
            else:
                print(f"Theme music is available for {t}")

def process_movies():
    hdds = check_folders(maindir)
    for h in hdds:
        location = f"{maindir}/{h}"
        dir = get_titles(location)
        print(dir)
        for t in dir:
            print(t)
            if not "theme.mp3" in os.listdir(f"{location}/{t}"):
                print("Searching for theme music...")
                title_clean = get_clean_name(t)
                tmdb_id = get_tmdb_id(title_clean, "movie")
                if tmdb_id:
                    theme_url = get_themerrdb_theme(tmdb_id, "movies")
                    if theme_url:
                        is_sucessfull = downloadtheme(theme_url, location, t)
                        if is_sucessfull == "fail":
                            print("Error while downloading
...")
                            processnotfounds(t, location)
                    else:
                        processnotfounds(t, location)
                        
                else:
                    print("Not found in database...")
            else:
                print(f"Theme music is available for {t}")
    
def main():
    process_movies()
    process_series()

if __name__ == "__main__":
    main()
