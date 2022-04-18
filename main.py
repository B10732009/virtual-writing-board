import cv2
import video_capture
import fps
import painter

#-----------------------------main-----------------------------#
# declare objects
vc = video_capture.VedioCapture()
f = fps.FPS()
pt = painter.Painter(vc.img_height, vc.img_width)

now_x = 0
now_y = 0

while True:
    # refresh the image from camera
    # and check if it is successfully captured
    vc.refresh_image()
    if not vc.success:
        continue

    mode = "none"
    # refresh ladnmarks
    # and check if it is successfully captured
    vc.refresh_landmarks()
    if vc.landmarks:
        # draw the skeleton of hands on the image
        vc.draw_hand_skeleton()

        # transform the landmarks to a list
        vc.refresh_landmark_list()
        for lm_list in vc.landmark_list:
            finger_num = 8
            now_x = lm_list[finger_num][0]
            now_y = lm_list[finger_num][1]

            vc.refresh_drawing_mode()
            mode = vc.mode
            z = pt.zone(now_x, now_y)
            if vc.mode == "drawing":
                if z == "drawing":
                    if not pt.is_drawing:
                        pt.start_draw((now_x, now_y))
                    pt.draw((now_x, now_y))
                else:
                    pt.end_draw()
                break
            else:
                pt.end_draw()
                if z == "selecting":
                    pt.select_color(int(now_x/pt.color_box_width))
                elif z == "cleaning":
                    pt.refresh_canvas()
                break
    else:
        pt.end_draw()

    # merge the camera image with canvas
    merged_img = cv2.addWeighted(vc.img, 0.3, pt.canvas, 0.7, 0)

    # add a circle at current position
    if not (mode == "none"):
        if pt.color == len(pt.color_list)-1:
            cv2.circle(merged_img, (now_x, now_y), 20,
                       (255, 255, 255), 2)
        else:
            cv2.circle(merged_img, (now_x, now_y), 5,
                       pt.color_list[pt.color], -1)

    # change the direction of image
    merged_img = cv2.flip(merged_img, 1)

    # refresh the FPS value
    f.refresh()

    # print out FPS and mode infomation
    cv2.putText(merged_img, 'FPS:{}'.format(f.get_fps()), (10, 20), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(merged_img, 'MODE:{}'.format(mode), (10, 40), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # adjust the size of image
    merged_img = cv2.resize(merged_img, ((int)(640*1.2), (int)(480*1.2)),
                            interpolation=cv2.INTER_AREA)

    # add the title to the window and show it
    cv2.imshow('VIRTUAL WRITTING BOARD', merged_img)

    # set the stopping key
    if cv2.waitKey(1) == ord(' '):
        break
