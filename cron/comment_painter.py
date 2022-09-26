import cv2
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy
from tqdm import tqdm
import comment_reader
import os

def commentPainter(currentDir, movieId):
    commentList = comment_reader.niconicoCommentReader(currentDir, movieId)
    # setting
    video_path = f'{currentDir}{movieId}/original.mp4'
    outName = f'{currentDir}{movieId}/paint.mp4'
    
    cap = cv2.VideoCapture(video_path)
    
    #動画サイズ取得
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    speed = width/7000
    
    # 画像サイズ，背景色，フォントの色を設定
    canvasSize    = (300, 150)
    backgroundRGB = (255, 0, 0)
    textRGB       = (255, 255, 255)
    stroke_RGB    = (0,0,0)
    stroke_size   = 1
    
    # 使うフォント，サイズ，描くテキストの設定
    ttfontname = "/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf"
    fontsize = int((width/640)*27)
    font = PIL.ImageFont.truetype(ttfontname, fontsize)
    
    #フレームレート取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    #フォーマット指定
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    writer = cv2.VideoWriter(outName, fmt, fps, (width, height))

    totalframecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    commentLine = {}
    commentLineLock = {k:False for k in range(10)}
    commentLineFree = []
    latest = 0
    for prog_i in range(totalframecount):
        if (prog_i%100==0):
            print(f"[{movieId}]", prog_i, "/", totalframecount)
        ret, frame = cap.read()
        if not ret:
            break
        # 文字を描く画像の作成
        img = PIL.Image.fromarray(frame)
        draw = PIL.ImageDraw.Draw(img)
        
        searchList = commentList.copy()
        for comment in searchList:
            commentId = comment[0]
            vposMs = comment[1]
            text = comment[2]
            # 用意した画像に文字列を描く
            diffMs = cap.get(cv2.CAP_PROP_POS_MSEC) - vposMs
            if (diffMs>0):
                _, _, textWidth, textHeight = draw.textbbox((0,0), text, font=font)
                if not commentId in commentLine.keys():
                    for i in range(10):
                        if not commentLineLock[i]:
                            commentLineLock[i] = True
                            commentLine[commentId] = i
                            latest = i
                            break
                    if not commentId in commentLine.keys():
                        latest += 0.5
                        if(latest > 9.5):
                            latest = 0
                        commentLine[commentId] = latest
                        
                textLeftTop = ((width-(diffMs-len(text)*100)*speed*(1+len(text)*0.1)),
                               commentLine[commentId]/10*height)
                            
                if(textLeftTop[0]+textWidth < width and
                           not commentId in commentLineFree):
                    commentLineLock[commentLine[commentId]] = False
                    commentLineFree.append(commentId)
                if(textLeftTop[0]+textWidth < 0):
                    commentList.remove(comment)                    
                draw.text(textLeftTop, text, fill=textRGB, font=font,
                          stroke_width=stroke_size, stroke_fill=stroke_RGB)
            else:
                break
        #動画書き込み
        writer.write(numpy.array(img))
    cap.release()
    #これを忘れるとプログラムが出力ファイルを開きっぱなしになる
    writer.release()
    cv2.destroyAllWindows()
    print(f"[{movieId}] paint Complete!")
    return 0

# currentDir = "/media/hiita/2C8CE78D8CE74FBE/www/html/"
# commentPainter(currentDir, "sm41117420")