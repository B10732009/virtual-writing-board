import cv2
import numpy as np

import video_capture
import fps
import painter


def coodr_trans(img, perc_x, perc_y):
    x = (int)(img.shape[1]*perc_x)
    y = (int)(img.shape[0]*perc_y)
    return (x, y)


def create_empty_canvas(canvas_height, canvas_width):
    np.zeros((canvas_height, canvas_width, 3), np.uint8)


#-----------------------------main-----------------------------#
# declare objects
vc = video_capture.VedioCapture()
f = fps.FPS()
pt = painter.Painter(vc.img_height, vc.img_width)

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
            if vc.mode == "drawing":
                if not pt.is_drawing:
                    pt.start_draw((if_x, if_y))
                pt.draw((if_x, if_y))
                break
            else:
                pt.end_draw()
                if pt.zone(if_x, if_y) == "selecting":
                    pt.select_color(int(if_x/pt.color_box_width))
    else:
        pt.end_draw()

    # merge the camera image with canvas
    merged_img = cv2.addWeighted(vc.img, 0.3, pt.canvas, 0.7, 0)

    # change the direction of image
    merged_img = cv2.flip(merged_img, 1)

    # refresh the FPS value and print out it
    f.refresh()
    cv2.putText(merged_img, 'FPS:{}'.format(f.get_fps()), (10, 20), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # adjust the size of image
    merged_img = cv2.resize(merged_img, ((int)(640*1.2), (int)(480*1.2)),
                            interpolation=cv2.INTER_AREA)

    # add the title to the window and show it
    cv2.imshow('VIRTUAL WRITTING BOARD', merged_img)

    # set the stopping key
    if cv2.waitKey(1) == ord(' '):
        break
