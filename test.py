import cv2 

cam = cv2.VideoCapture(0)

result, img = cam.read()


t = cv2.imwrite("test.png", img)