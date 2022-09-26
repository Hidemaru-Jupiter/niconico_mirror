# https://github.com/Negima1072/zenn-docs/blob/main/articles/nvcomment-api.md
# https://dplayer.diygod.dev/guide.html#special-thanks
import requests, random, string, json
import niconico_comment_getter_legacy
def niconicoComment(currentDir, movieId):
    headers = {
      "X-Frontend-Id": "6",
      "X-Frontend-Version": "0"
    }

    actionTrackId = \
      "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) \
      + "_" \
      + str(random.randrange(10**(12),10**13))

    commentList = []
    try:
        url = "https://www.nicovideo.jp/api/watch/v3_guest/{}?actionTrackId={}" \
          .format(movieId, actionTrackId)

        res = requests.post(url, headers=headers).json()

        nvComment = res["data"]["comment"]["nvComment"]

        headers = {
          "X-Frontend-Id": "6",
          "X-Frontend-Version": "0",
          "Content-Type": "application/json"
        }

        params = {
          "params": nvComment["params"],
          "additionals": {},
          "threadKey": nvComment["threadKey"]
        }

        url = nvComment["server"] + "/v1/threads"

        res = requests.post(url, json.dumps(params), headers=headers).json()
        
        
        commentId = 0
        for threads in res["data"]["threads"]:
            for comments in threads["comments"]:
                commentList.append([int(commentId), int(comments["vposMs"]),
                                    comments["body"].replace("\n", "  ").replace("\t", "  ")])
                commentId+=1
    except:
        print(f"[{movieId}]use niconico_comment_getter_legacy")
        commentList = niconico_comment_getter_legacy.get(movieId)
    with open(f"{currentDir}{movieId}/comment.txt", "w") as f:
        for comment in sorted(commentList, key=lambda x:x[1]):
            f.write(str(comment[0])+"\t"+str(comment[1])+"\t"+str(comment[2])+"\n")
    return sorted(commentList, key=lambda x:x[1])