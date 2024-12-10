import cv2
import numpy
import numpy as np
import math


def load_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    assert img is not None
    return img


def preprocess_image_1(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = cv2.bitwise_not(binary)
    return gray, binary


def preprocess_image_2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = cv2.bitwise_not(binary)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return gray, binary
def find_contours(binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def analyze_contour(contour):
    area = cv2.contourArea(contour)
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
    perfect_circle_area = math.pi * radius * radius
    circularity = min(area / perfect_circle_area * 100, 100)
    return center, radius, area, perfect_circle_area, circularity


def draw_results(img, contour, center, radius, circularity):
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)
    cv2.circle(img, center, radius, (0, 255, 0), 2)
    cv2.putText(img, f"{circularity:.2f}%", (center[0] - 40, center[1] + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


def process_image(image):
    if type(image) != numpy.ndarray: img = load_image(image)
    else: img = image

    check = False
    current = 0

    try:
        _, binary = preprocess_image_1(img)
        contours = find_contours(binary)

        for contour in contours:
            center, radius, area, perfect_area, circularity = analyze_contour(contour)
            draw_results(img, contour, center, radius, circularity)
            check = True
            current = circularity

    except:
        _, binary = preprocess_image_2(img)
        contours = find_contours(binary)
        for contour in contours:
            center, radius, area, perfect_area, circularity = analyze_contour(contour)
            draw_results(img, contour, center, radius, circularity)
            check = True
            current = circularity
    finally:
        if check: return current
        return -1
# usage : process_image(numpy.ndarray or string(path))
# plz use try catch syntax