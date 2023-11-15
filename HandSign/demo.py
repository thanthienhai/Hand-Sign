# Importing thư viện 
import numpy as np
import cv2
import math

# class
class hand(object):
	hand_cascade = cv2.CascadeClassifier('data.xml')

# lấy ảnh từ camera
	cap = cv2.VideoCapture(0)
	while 1:
		ret, img = cap.read()
		blur = cv2.GaussianBlur(img,(5,5),0) # làm mờ hình ảnh để làm mịn các cạnh
		# đa màu => màu đen trắng 
		gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
		# khung giới hạn của hình ảnh 
		retval2,thresh1 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		# phát hiện tay trong khung giới hạn của hình ảnh 
		hand = hand_cascade.detectMultiScale(thresh1, 1.3, 5)
		#create mask
		mask = np.zeros(thresh1.shape, dtype = "uint8")
		for (x,y,w,h) in hand:
			cv2.rectangle(img,(x,y),(x+w,y+h), (122,122,0), 2)
			cv2.rectangle(mask, (x,y),(x+w,y+h),255,-1)
		img2 = cv2.bitwise_and(thresh1, mask)
		final = cv2.GaussianBlur(img2,(7,7),0)
		contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		cv2.drawContours(img, contours, 0, (255,255,0), 3)
		cv2.drawContours(final, contours, 0, (255,255,0), 3)

		if len(contours) > 0:
			cnt=contours[0]
			hull = cv2.convexHull(cnt, returnPoints=False)
			# tìm điểm lồi 
			defects = cv2.convexityDefects(cnt, hull)
			count_defects = 0
			if defects is not None:
				for i in range(defects.shape[0]):
					p,q,r,s = defects[i,0]
					finger1 = tuple(cnt[p][0])
					finger2 = tuple(cnt[q][0])
					dip = tuple(cnt[r][0])
					# tìm chiều dài của tất cả các cạnh của tam giác
					a = math.sqrt((finger2[0] - finger1[0])**2 + (finger2[1] - finger1[1])**2)
					b = math.sqrt((dip[0] - finger1[0])**2 + (dip[1] - finger1[1])**2)
					c = math.sqrt((finger2[0] - dip[0])**2 + (finger2[1] - dip[1])**2)
					# áp dụng quy tắc cosin ở đây
					angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.29
					if angle <= 90:
						count_defects += 1
			# xác định các hành động cần thiết
			if count_defects == 1:
				cv2.putText(img,"2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
			elif count_defects==0:
				cv2.putText(img,"1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
			elif count_defects == 2:
				cv2.putText(img, "3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
			elif count_defects == 3:
				cv2.putText(img,"4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
			elif count_defects == 4:
				cv2.putText(img,"5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
		cv2.imshow('img',thresh1)
		cv2.imshow('img1',img)
		cv2.imshow('img2',img2)


		k = cv2.waitKey(1) & 0xff
		if k == 27:
			break
	cap.release()
	cv2.destroyAllWindows()
