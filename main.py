import cv2

import video_capture
import fps
import painter

#-----------------------------main-----------------------------#
# declare objects
vc = video_capture.VedioCapture()
f = fps.FPS()
pt = painter.Painter(vc.img_height, vc.img_width)

if_x = 0
if_y = 0

while True:
    # refresh the image from camera
    # and check if it is successfully captured
    vc.refresh_image()
    if not vc.ret:
        continue

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
            if_x = lm_list[finger_num][0]
            if_y = lm_list[finger_num][1]

            vc.refresh_drawing_mode()
            z = pt.zone(if_x, if_y)
            if vc.mode == "drawing":
                if z == "drawing":
                    if not pt.is_drawing:
                        pt.start_draw((if_x, if_y))
                    pt.draw((if_x, if_y))
                else:
                    pt.end_draw()
                break
            else:
                pt.end_draw()
                if z == "selecting":
                    pt.select_color(int(if_x/pt.color_box_width))
                elif z == "cleaning":
                    pt.refresh_canvas(pt.canvas_height, pt.canvas_width)
                break
    else:
        pt.end_draw()

    # merge the camera image with canvas
    merged_img = cv2.addWeighted(vc.img, 0.3, pt.canvas, 0.7, 0)

    cv2.circle(merged_img, (if_x, if_y), 5,
               pt.color_list[pt.color], -1)

    # change the direction of image
    merged_img = cv2.flip(merged_img, 1)

    # refresh the FPS value and print out it
    f.refresh()
    cv2.putText(merged_img, 'FPS:{} MODE:{}'.format(f.get_fps(), vc.mode), (10, 20), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # adjust the size of image
    merged_img = cv2.resize(merged_img, ((int)(640*1.2), (int)(480*1.2)),
                            interpolation=cv2.INTER_AREA)

    # add the title to the window and show it
    cv2.imshow('VIRTUAL WRITTING BOARD', merged_img)

    # set the stopping key
    if cv2.waitKey(1) == ord(' '):
        break
