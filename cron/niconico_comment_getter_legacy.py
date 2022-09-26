from bs4 import BeautifulSoup
import requests
import json
def get(movieId):
    source = requests.get(f"https://nicovideo.jp/watch/{movieId}")
    soup = BeautifulSoup(source.text, "html.parser")
    elem = soup.select_one("#js-initial-watch-data")
    js = json.loads(elem.get("data-api-data"))
    threads = js["comment"]["threads"]

    commentList = []
    for thread in threads:
        params = {
            "thread": thread["id"],
            "version": "20090904",
            "scores": "1",
            "fork": thread["fork"],
            "language": "0",
            "res_from": "-1000"
        }
        url = thread["server"] + "/api.json/thread"

        res = requests.get(url, params=params)
        resjs = json.loads(res.text)

        commentId = 0
        for el in resjs:
            if "chat" in el:
                commentList.append([
                        commentId,
                        int(el["chat"]["vpos"]),
                        el["chat"]["content"].replace("\n", "  ").replace("\t", "  ")
                ])
                commentId += 1
    return commentList