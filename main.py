# v0.1.1B
# 針對有人很小的問題進行修復

import cv2
from ultralytics import YOLO


# 載入模型
model = YOLO('yolov8n.pt')
model.classes = [0]  # Assuming class 0 is your target

# 打開鏡頭
video_path = 0
cap = cv2.VideoCapture(video_path)


while cap.isOpened():

    success, frame = cap.read()
    frame = cv2.resize(frame, (720, 480))

    # 根據不同設備像素設定中心點
    camera_width = frame.shape[1]
    camera_height = frame.shape[0]
    
    width_center = camera_width / 2
    

    print(width_center)
    print(camera_height-50)

    if success:

        # 將 frame 丟入模型進行追蹤
        results = model.track(frame, persist=True,classes=[0])

        # frame = results[0].plot()

        boxes = results[0].boxes.xywh.cpu()

        # boxes 儲存所有追蹤到的人的座標

        # 判斷是否有看到一個人或以上
        if len(boxes) == 0:
            
            # 沒看到人 停下來
            # 這裡放停下來的程式

            print('stop')

            # 跳過下面的程式 直接進入下一個迴圈
            continue
        
        # 執行到這裡代表有看到人

        box_id = 0

        # 把所有看到的人的座標畫在畫面上
        for box in boxes:
            
            # 取出中心點座標
            middle_x = int(box[0])
            middle_y = int(box[1])
            # 取出寬度
            width = int(box[2])


            # 判斷是否是第一個看到的人 如果不是就不會追蹤
            if(box_id == 0):
                
                cv2.line(frame, ( int(width_center), int(camera_height-50) ), (middle_x, middle_y), (255, 255, 255), 10)

                # 計算和中心點的偏移量
                move = width_center - middle_x
                print(move)

                cv2.putText(frame, str(move), (middle_x, middle_y), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 10, cv2.LINE_AA)


                # move代表偏移量 可以用他來調整速度

                if move >= 0:
                    # 人在左邊的程式
                    # 這裡放人在左邊的程式
                    print('left')
            
                elif move < 0:
                    # 人在右邊的程式
                    # 這裡放人在右邊的程式
                    print('right')


                cv2.circle(frame, (middle_x, middle_y), int(width/2), (255, 255, 255), 20)
                box_id += 1
            else:
                cv2.circle(frame, (middle_x, middle_y), int(width/2), (255, 255, 255), 10)


        cv2.imshow("YOLOv8 Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
