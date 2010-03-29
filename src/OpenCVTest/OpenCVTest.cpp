// OpenCVTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "cv.h"
#include "highgui.h"

int _tmain(int argc, _TCHAR* argv[])
{
	CvSeq* contours = NULL;
	CvMemStorage* storage = cvCreateMemStorage(0);
	IplImage* img = cvLoadImage("answer_reveal.png");	

	cvNamedWindow("win");

	IplImage* grayImg = cvCreateImage(cvGetSize(img), 8, 1);
	cvCvtColor(img, grayImg, CV_RGB2GRAY);
	cvThreshold(grayImg, grayImg, 160, 255, CV_THRESH_BINARY);
	cvFindContours(grayImg, storage, &contours);
	
	// cvZero(grayImg);  -- if we were displaying the gray image with the contours, in only black and white
	
	if (contours) {
		cvDrawContours(img, contours, 
			cvScalar(255, 0, 0), // ext color (red)
			cvScalar(0, 255, 0), // hole color (green)
			100, // max level of contours to draw
			5); // thickness
	}

	cvShowImage("win", img);

	// experiment to read a frame from an image
	CvCapture* capture = cvCaptureFromFile("C:\\Projects\\meancat\\misc\\100Bot\\1v100_translated.mpeg");
	if (capture == NULL) {
		printf("capture is null");
	} else {
		cvSetCaptureProperty(capture, CV_CAP_PROP_POS_FRAMES, 0);
		IplImage* oneFrame = cvQueryFrame(capture);
		cvShowImage("win", oneFrame);
	}

	cvWaitKey(0);
	
	cvReleaseImage(&img);
	cvReleaseImage(&grayImg);

	return 0;
}

