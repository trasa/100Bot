import cv

def frameiter(cap=None):
    if cap is None:
        cap = cv.CaptureFromCAM(0)
    while True:
        img = cv.QueryFrame(cap)
        yield img
    

win = 'Show Cam'
cv.NamedWindow(win)
it = frameiter()
while cv.WaitKey(1) != 27:
    img = it.next()
    if img is not None: 
        cv.ShowImage(win, img)
        