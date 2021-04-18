import cv2
background = cv2.imread('Background.bmp')

group_of_events = []
index = 0
delta = 300000
time_start = 119557
with open("events.txt") as events:
    for line in events:
        timestamp, x_pos, y_pos, polarity = line.split()
        timestamp = int(timestamp)
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        polarity = int(polarity)

        if (timestamp - time_start) < delta:
            group_of_events.append([timestamp, x_pos, y_pos, polarity])
        else:
            im_cp = background.copy()
            for i in range(0, len(group_of_events)):
                if group_of_events[i][3] == 1:
                    cv2.circle(im_cp, (group_of_events[i][1], group_of_events[i][2]), radius=0, color=(0, 0, 255), thickness=2)
                else:
                    cv2.circle(im_cp, (group_of_events[i][1], group_of_events[i][2]), radius=0, color=(255, 0, 0), thickness=2)
            group_of_events.clear()

            group_of_events.append([timestamp, x_pos, y_pos, polarity])
            time_start = timestamp

            cv2.imshow("Background", im_cp)
            cv2.waitKey(1)





