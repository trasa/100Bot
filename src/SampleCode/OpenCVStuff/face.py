import sys
from cv import *
from opencv.cv import *
 
def detect(image):
    image_size = GetSize(image)
 
    # create grayscale version
    grayscale = CreateImage(image_size, 8, 1)
    CvtColor(image, grayscale, CV_BGR2GRAY)
 
    # create storage
    storage = CreateMemStorage(0)
#    cv.cvClearMemStorage(storage)
 
    # equalize histogram
    EqualizeHist(grayscale, grayscale)
 
    # detect objects
    cascade = cvLoadHaarClassifierCascade('haarcascade_frontalface_alt.xml', cvSize(1,1))
    # 1= HAAR_DO_CANNY_PRUNING
    faces = HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 1) 
#1.2,  # scale factor 
#2,  # neighbors
#1  # HAAR_DO_CANNY_PRUNING
#)
 
    if faces:
        print 'face detected!'
        for i in faces:
            Rectangle(image, CvPoint( int(i.x), int(i.y)),
                         CvPoint(int(i.x + i.width), int(i.y + i.height)),
                         RGB(0, 255, 0), 3, 8, 0)
 
if __name__ == "__main__":
    
 
    print "Press ESC to exit ..."
 
    # create windows
    NamedWindow('Camera')
 
    # create capture device
    device = 0 # assume we want first device
    capture = CaptureFromCAM(0)
    SetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 640)
    SetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 480)
        
 
    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
 
    while True:
        # do forever
 
        # capture the current frame
        frame = QueryFrame(capture)
        if frame is None:
            break
 
        # mirror
        Flip(frame, None, 1)
 
        # face detection
        detect(frame)
 
        # display webcam image
        ShowImage('Camera', frame)
 
        # handle events
        k = WaitKey(10)
 
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break