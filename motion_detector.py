import cv2, time, pandas
from datetime import datetime

first_frame=None

status_list =[None,None] #since initially it will have only one value and [-2] index will throw an error
times=[]

df=pandas.DataFrame(columns=["start","end"])

video=cv2.VideoCapture(0)

while True:
	check, frame = video.read()
	status=0
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray=cv2.GaussianBlur(gray,(21,21),0)

	if first_frame is None:
		first_frame=gray
		continue #go to begining of loop, nothing below will be executed

	delta_frame=cv2.absdiff(first_frame,gray)
	thresh_frame=cv2.threshold(delta_frame, 120, 255, cv2.THRESH_BINARY)[1]
	thresh_frame=cv2.dilate(thresh_frame,None, iterations=2)

	(__,cnts,__)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 5000:
			continue
		status=1
		(x,y,w,h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)    # (0,255,0) is the green color | '3' is the width of the rectangele

	status_list.append(status)

	status_list=status_list[-2:]

	if status_list[-1]==1 and status_list[-2]==0:
		times.append(datetime.now())
	if status_list[-1]==0 and status_list[-2]==1:
		times.append(datetime.now())

	cv2.imshow("Gray Frame", gray)
	cv2.imshow("Delta Frame", delta_frame)
	cv2.imshow("Threshold frame", thresh_frame)
	cv2.imshow("Color Frame",frame)

	key=cv2.waitKey(1)

	if key==ord('q'):
		if status==1:
			times.append(datetime.now())
		break
	print(status)

print(status_list)
print(times)

for i in range(0,len(times),2):
	df=df.append({"start":times[i],"end":times[i+1]},ignore_index=True)

df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows