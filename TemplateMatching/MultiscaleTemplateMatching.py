import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils

def plt_imshow(title, image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.title(title)
    plt.show()

template = cv2.imread('pepsi_template.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
print('Template Dimensions:', (tH, tW))

canvas = cv2.imread('pepsi_image.jpg')
#canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
#canvas = cv2.Canny(canvas, 50, 200)
(cH, cW) = canvas.shape[:2]
print('Canvas Dimensions:', (cH, cW))

#plt_imshow('Pepsi Template (Outline)', template)
#plt_imshow('Pepsi Canvas (Outline)', canvas)

'''
result = cv2.matchTemplate(canvas, template, cv2.TM_CCOEFF_NORMED)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
(startX, startY) = maxLoc
(endX, endY) = startX+template.shape[1], startY+template.shape[0]
cv2.rectangle(canvas, (startX, startY), (endX, endY), (255,0,0), 5)
plt_imshow('Final Template Matching', canvas)
'''

found = None
for scale in np.linspace(0.1, 1.0, 25)[::-1]:
    cResized = imutils.resize(canvas, width=int(canvas.shape[1]*scale))
    ratio = canvas.shape[1]/float(cResized.shape[1])

    if cResized.shape[0]<tH or cResized.shape[1]<tW:
        break

    cEdged = cv2.Canny(cResized, 50, 200)
    result = cv2.matchTemplate(cEdged, template, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    if found is None or maxVal>found[0]:
        found = (maxVal, maxLoc, ratio)
        print(cResized.shape)

(placeholder, maxLoc, ratio) = found
(startX, startY) = (int(maxLoc[0]*ratio), int(maxLoc[1]*ratio))
(endX, endY) = (int((maxLoc[0]+tW)*ratio), int((maxLoc[1]+tH)*ratio))

cv2.rectangle(canvas, (startX, startY), (endX, endY), (0,0,255), 10)
plt_imshow('Final Result: Detected Pepsi Logo', canvas)