import cv2
background = cv2.imread('Background.bmp')

group_of_events = []
index = 0
group_number = 3000
with open("events.txt") as events:
    for line in events:
        timestamp, x_pos, y_pos, polarity = line.split()
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        polarity = int(polarity)
        index += 1
        group_of_events.append([x_pos, y_pos, polarity])

        if len(group_of_events) == group_number:
            im_cp = background.copy()
            for i in range(0, group_number):
                if group_of_events[i][2] == 1:
                    cv2.circle(im_cp, (group_of_events[i][0], group_of_events[i][1]), radius=0, color=(0, 0, 255), thickness=2)
                else:
                    cv2.circle(im_cp, (group_of_events[i][0], group_of_events[i][1]), radius=0, color=(255, 0, 0), thickness=2)
            index = 0
            group_of_events.clear()
            cv2.imshow("Background", im_cp)
            cv2.waitKey(1)





