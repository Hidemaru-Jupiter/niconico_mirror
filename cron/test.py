import requests
from bs4 import BeautifulSoup
import re
import datetime
import niconico_comment_getter
import os
import subprocess
import thumbnail

def command(dump, cmd):
    print(f"[cmd]{cmd}\n")
    ret = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    with open(dump, "w") as f:
        f.write(f"[cmd]{cmd}\n")
        f.write("=============================\n")
        f.write("return code\n")
        f.write("=============================\n")
        f.write(str(ret.returncode)+"\n")
        f.write("=============================\n")
        f.write("stdout\n")
        f.write("=============================\n")
        f.write(str(ret.stdout)+"\n")
        f.write("=============================\n")
        f.write("stderr\n")
        f.write("=============================\n")
        f.write(str(ret.stderr)+"\n")
    return ret.returncode

titleDict = {}
currentDir = "/media/hiita/2C8CE78D8CE74FBE/www/html/"
response = requests.get("https://www.nicovideo.jp/ranking/genre/all?term=hour&rss=2.0")
soup = BeautifulSoup(response.text, 'lxml')
movieIdList = []
for item in soup.find_all("item")[:3]:
    title = re.sub(r"第[0-9]+位：",
                      "", item.find("title").text)
    url = re.search(r"https://www.nicovideo.jp/watch/(sm|so)[0-9]+"
                    ,item.text).group()
    movieId = url.split("/")[-1]
    movieIdList.append(movieId)
    titleDict[movieId] = title
    
    if not os.path.exists(f"{currentDir}{movieId}"):
        os.mkdir(f"{currentDir}{movieId}")
    if not os.path.exists(f"{currentDir}{movieId}/original.mp4"):
        status = command(f"{currentDir}{movieId}/yt-dlp.log",
                    f"yt-dlp --write-url --write-thumbnail --convert-thumbnails jpg "
                    f"--merge-output-format mp4 "
                    f"-o 'thumbnail:{currentDir}{movieId}/thumbnail' "
                    f"-o '{currentDir}{movieId}/original.mp4' {url}")
    else:
        print(f"[{movieId}] skip yt-dlp")
    if not os.path.exists(f"{currentDir}{movieId}/comment.txt"):
        print(f"[function]niconico_comment_getter.niconicoComment({currentDir}, {movieId})\n")
        niconico_comment_getter.niconicoComment(currentDir, movieId)
    else:
        print(f"[{movieId}] skip commentGet")
    with open(f"{currentDir}{movieId}/create.txt", "w") as f:
        f.write(str(int(datetime.datetime.now().timestamp())))
    if not os.path.exists(f"{currentDir}{movieId}/hconcat100_thumbnail.jpg"):
        print(f"[function]thumbnail.make({currentDir}, {movieId})\n")
        thumbnail.make(f'{currentDir}{movieId}/original.mp4', f'{currentDir}{movieId}/hconcat100_thumbnail.jpg')
print('end')
