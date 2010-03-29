#from opencv.highgui import cvLoadImage
#from opencv.cv import cvLoad
import cv
#from opencv.cv import *

winName = 'findcontour'
storage = cv.CreateMemStorage(0)

img = cv.LoadImage("question_answers.png")

imgGray = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
cv.Threshold(imgGray, imgGray, 160, 255, cv.CV_THRESH_BINARY)

displayImg = imgGray


#seq = cv.FindContours(imgGray, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
seq = cv.FindContours(imgGray, storage)


#red = cv.Scalar(250, 0, 0)

#for c in contours:
#    print c

# display original image
cv.NamedWindow(winName)
#cv.ShowImage(winName, img)
cv.ShowImage(winName, displayImg)


cv.WaitKey()
    