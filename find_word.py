import pyautogui
import numpy as np
import cv2
import pytesseract
from imutils.object_detection import non_max_suppression

def find_word(word):
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    orig = image.copy()
    H, W = image.shape[:2]
    newW, newH = 3840, 2112
    rW, rH = W / float(newW), H / float(newH)
    image = cv2.resize(image, (newW, newH))
    H, W = image.shape[:2]

    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    scores, geometry = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

    numRows, numCols = scores.shape[2:4]
    rects, confidences = [], []
    ignored_regions = [(4, 3, 256, 90), (313, 7, 281, 27), (1238, 2, 680, 40), (1765, 47, 152, 45), (3, 868, 613, 212)]

    for y in range(numRows):
        scoresData = scores[0, 0, y]
        xData0, xData1, xData2, xData3, anglesData = geometry[0, 0, y], geometry[0, 1, y], geometry[0, 2, y], geometry[0, 3, y], geometry[0, 4, y]
        for x in range(numCols):
            if scoresData[x] < 0.1:
                continue

            offsetX, offsetY = x * 4.0, y * 4.0
            angle, cos, sin = anglesData[x], np.cos(anglesData[x]), np.sin(anglesData[x])
            h, w = xData0[x] + xData2[x], xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX, startY = int(endX - w), int(endY - h)

            startX_rescaled, startY_rescaled, endX_rescaled, endY_rescaled = (
                int(startX * rW), int(startY * rH), int(endX * rW), int(endY * rH)
            )

            if any(startX_rescaled < ix + iw and endX_rescaled > ix and startY_rescaled < iy + ih and endY_rescaled > iy for ix, iy, iw, ih in ignored_regions):
                continue

            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences)
    blur_ksize, padding = 3, 0.05

    for startX, startY, endX, endY in boxes:
        width, height = endX - startX, endY - startY
        startX, startY = max(0, int(startX - padding * width)), max(0, int(startY - padding * height))
        endX, endY = min(W, int(endX + padding * width)), min(H, int(endY + 0.2 * height))
        startX, startY, endX, endY = int(startX * rW), int(startY * rH), int(endX * rW), int(endY * rH)

        roi = orig[startY:endY, startX:endX]
        blurred_roi = cv2.GaussianBlur(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), (blur_ksize, blur_ksize), 0)
        text = pytesseract.image_to_string(blurred_roi, lang='pol').lower()

        if word.lower() in text:
            return (startX + (endX - startX) // 2, startY + (endY - startY) // 2)

    return None