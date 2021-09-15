import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils

# Returns image object from image filename.
def read_image(filename):
    return cv2.imread(filename)

# Returns height, width dimension of image.
def return_dim(img):
    return img.shape[:2]

# Performs canny edge detection on image.
def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.Canny(img, 50, 200)
    return img

# Displays image in original RGB color scheme.
def plt_imshow(title, image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.title(title)
    plt.show()

# Detects template object on canvas and returns coefficient, location and scale ratio of best match.
def detect_object(canvas, template):
    found = None
    (tH, tW) = return_dim(template)
    for scale in np.linspace(0.1, 2.0, 50)[::-1]:
        cResized = imutils.resize(canvas, width=int(canvas.shape[1] * scale))
        ratio = canvas.shape[1] / float(cResized.shape[1])

        if cResized.shape[0] < tH or cResized.shape[1] < tW:
            break

        cEdged = preprocess_image(cResized)
        result = cv2.matchTemplate(cEdged, template, cv2.TM_CCOEFF_NORMED)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, ratio)
            print('Scale Size: ', scale)
            print('maxLoc: ', found[1])
            print('maxVal: ', found[0], '\n')
    return found

# Draws detected template object onto canvas.
def draw_match(found_result, canvas, template):
    (tH, tW) = return_dim(template)
    (maxVal, maxLoc, ratio) = found_result
    (startX, startY) = (int(maxLoc[0] * ratio), int(maxLoc[1] * ratio))
    (endX, endY) = (int((maxLoc[0] + tW) * ratio), int((maxLoc[1] + tH) * ratio))
    cv2.rectangle(canvas, (startX, startY), (endX, endY), (0, 0, 255), 5)
    plt_imshow('Final Result: Detected Pepsi Logo', canvas)
    