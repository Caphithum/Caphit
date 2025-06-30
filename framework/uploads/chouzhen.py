import cv2

cap = cv2.VideoCapture("D:\\heirun/xxxxxl/framework/static/uploaded_videos/a.mp4")
isOpened = cap.isOpened

imageNum = 0
sum = 0
timef = 60

while (isOpened):
    if imageNum == 200:
        break
    sum += 1
    (frameState, frame) = cap.read()

    if frameState == True and sum % timef == 0:
        imageNum += 1
        fileName = 'D:\\heirun\\xxxxxl\\framework\\static\\videos_img' + '/' + str(imageNum) + '.jpg'
        cv2.imwrite(fileName, frame)
        print(fileName + " successfully write in")
    elif frameState == False:
        break

print('finish!')
cap.release()  # 释放视频资源
