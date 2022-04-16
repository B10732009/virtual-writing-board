import cv2
import numpy as np

import video_capture as vcap
import fps
import painter


def coodr_trans(img, perc_x, perc_y):
    x = (int)(img.shape[1]*perc_x)
    y = (int)(img.shape[0]*perc_y)
    return (x, y)


def create_empty_canvas(canvas_height, canvas_width):
    np.zeros((canvas_height, canvas_width, 3), np.uint8)


#------main------#
vc = vcap.VedioCapture()
f = fps.FPS()
pt = painter.Painter(vc.img_height, vc.img_width)


while True:
    vc.refresh_image()
    if vc.ret:
        vc.refresh_landmarks()
        if vc.landmarks:
            vc.draw_hand_skeleton()
            vc.refresh_landmark_list()
            # vc.refresh_finger_status()

            for lm_list in vc.landmark_list:
                finger_num = 8
                if_x = lm_list[finger_num][0]
                if_y = lm_list[finger_num][1]
                vc.refresh_drawing_mode()
                if vc.mode == "drawing":
                    if not pt.is_drawing:
                        pt.start_draw(
                            (if_x, if_y))
                    pt.draw((if_x, if_y))
                    break
                else:
                    pt.end_draw()
                    if (0 < if_y and if_y < 50) and (0 < if_x and if_x < 640):
                        pt.select_color((int)(if_x/160))

        merged_img = cv2.addWeighted(vc.img, 0.3, pt.canvas, 0.7, 0)
        merged_img = cv2.flip(merged_img, 1)

        f.refresh()
        cv2.putText(merged_img, 'FPS:{}'.format(f.get_fps()), (10, 20), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

        merged_img = cv2.resize(merged_img, ((int)(640*1.2), (int)(480*1.2)),
                                interpolation=cv2.INTER_AREA)

        cv2.imshow('VIRTUAL WRITTING BOARD', merged_img)

    if cv2.waitKey(1) == ord(' '):
        break
