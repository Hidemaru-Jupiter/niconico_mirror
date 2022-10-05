import cv2

def make(video_path, outName):
    cap = cv2.VideoCapture(video_path)

    #動画サイズ取得
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    totalframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    mini_height = 90
    mini_width = int(mini_height*width/height)
    per_thumbnail = (totalframe-1)/100

    frameList = []
    for i in range(100):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(per_thumbnail*i))
        ret, frame = cap.read()
        mini_frame = cv2.resize(frame, dsize=(mini_width, mini_height))
        frameList.append(mini_frame)
    im_v = cv2.hconcat(frameList)
    cv2.imwrite(outName, im_v)
    
# # test
# video_path = f'/media/hiita/2C8CE78D8CE74FBE/www/html/_DPlayer/original.mp4'
# outName = f'/media/hiita/2C8CE78D8CE74FBE/www/html/_DPlayer/hconcat100_thumbnail.jpg'
