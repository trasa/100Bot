// FindFaces.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "cv.h"
#include "highgui.h"


void detect(IplImage* frame);


CvHaarClassifierCascade* cascade;
CvMemStorage* storage;

int _tmain(int argc, _TCHAR* argv[])
{
	cvNamedWindow("faces");
	CvCapture* capture = cvCaptureFromCAM(0);
	cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 640);
	cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 480);


	//cascade = cvLoadHaarClassifierCascade("haarcascade_frontalface_alt.xml", cvSize(1, 1));
	cascade = cvLoadHaarClassifierCascade("1v100.xml", cvSize(1, 1));
	storage = cvCreateMemStorage(0);
	
	assert(capture && cascade && storage);

	IplImage* frame = NULL;
	while(1){
		frame = cvQueryFrame(capture);

		// flipping is required because... ?
		cvFlip(frame, 0, 1);
		detect(frame);
		cvFlip(frame, 0, 1);

		cvShowImage("faces", frame);

		int k = cvWaitKey(10);
		if (k == 0x1b) {
			printf("exiting..");
			break;
		}
	}

	cvReleaseCapture(&capture);
	cvReleaseMemStorage(&storage);
	return 0;
}

void detect(IplImage* frame) {
	CvSize size = cvGetSize(frame);
	IplImage* grayScale = cvCreateImage(size, 8, 1);
	cvCvtColor(frame, grayScale, CV_BGR2GRAY);
	cvEqualizeHist(grayScale, grayScale);

	// for detecting faces:
	//CvSeq* faces = cvHaarDetectObjects(grayScale, cascade, storage, 1.2, 3, CV_HAAR_DO_CANNY_PRUNING, cvSize(55, 55));
	
	// for testing false-positive rate vs. 1v100 screen:
	CvSeq* faces = cvHaarDetectObjects(grayScale, cascade, storage, 1.2, 4, CV_HAAR_DO_CANNY_PRUNING, cvSize(80, 80));
	for (int i=0; i < faces->total; i++) {
		CvRect rect = *(CvRect*)cvGetSeqElem(faces, i);
		
		printf("width %d height %d\r\n", rect.width, rect.height);
		
		cvRectangle(frame, 
			cvPoint(rect.x, rect.y), 
			cvPoint(rect.x+rect.width, rect.y+rect.height),
			CV_RGB(255, 0, 0), 
			3);
	}
	
}
