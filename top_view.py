import numpy as np
import cv2
import imutils

def order_points(pts,image):
	# Forming an 4X2 matrix 
	print("pts",pts)
	rect=np.zeros((4,2),dtype="float32")
	# print(rect)
	# output
	# [[0. 0.]
 	# 	[0. 0.]
 	# 	[0. 0.]
 	# 	[0. 0.]]

 	# It sums all the x and y coordinate
	s=np.sum(pts,axis=1)
	# print(s,"sum")
	# output [110 276 247 409] argmin returns the indice of least element and argmax for highest
	
	rect[0]=pts[np.argmin(s)] #top left
	rect[2]=pts[np.argmax(s)] #bottom right
	# cv2.rectangle(image,(rect[0][0],rect[0][1]),(rect[2][0],rect[2][1]),(0,255,0),2)
	# cv2.imshow("rectangle",imutils.resize(image,height=500))
	# It performs diff between all x and y coordinate
	d=np.diff(pts,axis=1)
	print(d)   
	#output [[ -60][-226][  77][ -93]]
	
	rect[1]=pts[np.argmin(d)] #top right
	rect[3]=pts[np.argmax(d)] #bottom left
	# print("rect",rect)
	return rect


# pts="[(85,25),(251,25),(85,162),(251,158)]"

# pts = np.array(eval(pts), dtype = "float32")
# print(pts)


def four_point_transform(image,pts):
	
	
	rect=order_points(pts,image)

	(tl,tr,bl,br)=pts
	
	# Finding the max height betweeen X and Y coordinate using Eucledian distance i.e sqrt((X1-X2)^2+(Y1-Y2)^2)
	
	widthA=np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))
	widthB=np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
	width=max(int(widthA),int(widthB))

	heightA=np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
	heightB=np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
	height=max(int(heightA),int(heightB))

	dst=np.array([[0,0],[width-1,0],[width-1,height-1],[0,height-1]],dtype="float32")
				   # TL        TR	           BR             BL

	# For perspective transformation, you need a 3x3 transformation matrix. 
	# Straight lines will remain straight even after the transformation. 
	# To find this transformation matrix, you need 4 points on the input image and corresponding points on the output image. Among these 4 points, 3 of them should not be collinear. Then transformation matrix can be found by the function cv2.getPerspectiveTransform. Then apply cv2.warpPerspective with this 3x3 transformation matrix.
	# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
	M=cv2.getPerspectiveTransform(rect,dst)
	wrapped=cv2.warpPerspective(image,M,(width,height))
	# cv2.imshow("wrappy",wrapped)
	return wrapped





# pts=[[85,25],[251,25],[85,162],[251,158]]

# image=cv2.imread("source.jpeg")
# wrapped=four_point_transform(image,pts)

# cv2.imshow("original",image)
# cv2.imshow("top_view",wrapped)
# cv2.waitKey(0)
