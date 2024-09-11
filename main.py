import cv2
import math

img = cv2.imread("real.png", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 이진화 처리
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
binary = cv2.bitwise_not(binary)

# 외곽선 검출
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 각 contour에 대해 처리
for i in range(len(contours)):
    # 외곽선 그리기(red)
    cv2.drawContours(img, [contours[i]], 0, (0, 0, 255), 2)

    # 그린 원 넓이
    extent_of_drawn =  cv2.contourArea(contours[i])
    print("Contour", i, "넓이:", extent_of_drawn)

    # 원의 중심과 반지름 계산
    (x, y), r = cv2.minEnclosingCircle(contours[i])
    center = (int(x), int(y))
    r = int(r)

    # 외접원 그리기(blue)
    cv2.circle(img, center, r, (0, 255, 0), 2)

    # 외접원의 넓이
    extent_of_Perfect = math.pi * r * r
    print("외접원의 넓이:", extent_of_Perfect)

    # 퍼센트 계산
    persent = round((extent_of_drawn/extent_of_Perfect) * 100, 2)
    if persent > 100:
        persent = 100
    print(f"{persent}%")
    persent = str(persent) + "%"

    # 텍스트 크기 계산
    text_size = cv2.getTextSize(persent, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    
    # 이미지의 크기 얻기
    img_height, img_width = img.shape[:2]
    
    # 텍스트를 화면 하단 중앙에 배치
    text_x = (img_width - text_size[0]) // 2
    text_y = img_height - 50  # 하단에서 50px 위에 배치

    # 텍스트 출력 (하단 중앙)
    cv2.putText(img, persent, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    cv2.imshow("src", img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
