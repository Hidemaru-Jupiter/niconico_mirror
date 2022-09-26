def niconicoCommentReader(currentDir, movieId):
    raw_comment=""
    with open(f"{currentDir}{movieId}/comment.txt", "r") as f:
        raw_comment = f.read()
    commentList = []
    for comment in raw_comment.split("\n"):
        if not (comment == ""):
            commentId, vposMs, body = comment.split("\t")
            commentList.append([int(commentId), int(vposMs), body])
    return commentList
# commentList = niconicoCommentReader("yt-dlp_videos/","sm41116819")