import numpy as np
import imutils
import cv2
import top_view
from imutils import contours

answer={0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

image=cv2.imread("omr.png")
cv2.imshow("original",image)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray,(5,5),0)  #(5,5) flter size
canny_edged=cv2.Canny(gray,100,200) #image threshold1 threshold2   https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html

# cv2.imshow("Gray",gray)
# cv2.imshow("Blur",blur)
cv2.imshow("canny",canny_edged)


cnts=cv2.findContours(canny_edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# If you pass cv2.CHAIN_APPROX_NONE, all the boundary points are stored. But actually do we need all the points? For eg, you found the contour of a straight line. Do you need all the points on the line to represent that line? No, we need just two end points of that line. This is what cv2.CHAIN_APPROX_SIMPLE does. It removes all redundant points and compresses the contour, thereby saving memory.
# CV2.RETR_EXTERNAL it returns the extreme outer contour    https://docs.opencv.org/3.1.0/d9/d8b/tutorial_py_contours_hierarchy.html
cnts=imutils.grab_contours(cnts)
frame_cnt=None
if len(cnts)>0:
	cnts=sorted(cnts,key=cv2.contourArea,reverse=True)

	for c in cnts:
		perimeter=cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c,0.02*perimeter,True)

		if len(approx)==4:
			frame_cnt=approx
			break

original=top_view.four_point_transform(image,frame_cnt.reshape(4,2))
warped=top_view.four_point_transform(gray,frame_cnt.reshape(4,2))

cv2.imshow("transform original",original)
# cv2.imshow("transform gray",warped)

# THE ABOVE ALL PART WAS TO CREATE A TOP VIEW OF THE IMAGE


ret,thresh=cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
# cv2.imshow("threshold",thresh)
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
qstn=[]
temp=0

for c in cnts:
	(x,y,w,h)=cv2.boundingRect(c)
	ar=w/float(h)

	if w>=20 and h>=20 and ar>=0.9 and ar<=1.1:
		qstn.append(c)

# for c in cnts:
# 	(x,y),r=cv2.minEnclosingCircle(c)

# 	if r>=21:
# 		qstn.append(c)

# cv2.drawContours(original,qstn,-1,(0,255,0),2)
# cv2.imshow("Image",original)

# print("question",qstn)
# print("length",len(qstn))		 

qstn=contours.sort_contours(qstn,method="top-to-bottom")[0]
correct=0
# print("question",qstn)
# print("length",len(qstn))		 

for (q,i) in enumerate(np.arange(0,len(qstn),5)):
	print("i",i)
	cnts=contours.sort_contours(qstn[i:i+5])[0]
	bubbled=None
	for (j,c) in enumerate(cnts):
		print("j",j)
		mask=np.zeros(thresh.shape,dtype="uint8")
		cv2.drawContours(mask,[c],-1,255,-1)
		mask=cv2.bitwise_and(thresh,thresh,mask=mask)
		total=cv2.countNonZero(mask)

		if bubbled is None or total>bubbled[0]:
			bubbled=(total,j)
			color=(0,0,255)
			k=answer[q]
			print("correct 1",correct)	
			if k==bubbled[1]:
				color=(0,255,0)
				correct=correct+1

			print("correct 2",correct)	

			cv2.drawContours(original,[cnts[k]],-1,color,3)	

print("correct",correct)
cv2.imshow("answer",original)


cv2.waitKey(0)
cv2.destroyAllWindows()