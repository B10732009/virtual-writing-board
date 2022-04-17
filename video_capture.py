import cv2
import mediapipe as mp
import math


class VedioCapture:
    def __init__(self):
        # initialize basic objects
        self.vedio_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.mp_hands = mp.solutions.hands
        self.hands = mp.solutions.hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils

        # image from camera
        self.success, self.img = self.vedio_capture.read()
        self.img_height, self.img_width, _ = self.img.shape

        # landmarks
        self.landmarks = []
        self.landmark_list = []

        # drawing mode
        self.mode = "drawing"

    def refresh_image(self):
        self.ret, self.img = self.vedio_capture.read()

    def refresh_landmarks(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.landmarks = self.hands.process(img_rgb).multi_hand_landmarks

    def refresh_landmark_list(self):
        self.landmark_list = []
        for landmark in self.landmarks:
            lm_list = []
            for lm in landmark.landmark:
                lm_list.append([int(lm.x*self.img_width),
                                int(lm.y*self.img_height)])
            self.landmark_list.append(lm_list)

    def refresh_drawing_mode(self):
        for lm_list in self.landmark_list:
            '''dis = (lm_list[4][0]-lm_list[8][0])**2 + \
                (lm_list[4][1]-lm_list[8][1])**2
            thres = 1000
            if dis < thres:
                self.mode = "selecting"
            else:
                self.mode = "drawing"'''

            v1 = (lm_list[6][0]-lm_list[5][0], lm_list[6][1]-lm_list[5][1])
            v2 = (lm_list[7][0]-lm_list[6][0], lm_list[7][1]-lm_list[6][1])
            if angle(v1, v2) > 30:
                self.mode = "selecting"
            else:
                self.mode = "drawing"
            # print(self.mode)

    def draw_hand_skeleton(self):
        for landmark in self.landmarks:
            self.mp_draw.draw_landmarks(
                self.img, landmark, self.mp_hands.HAND_CONNECTIONS)


# -------------------------------------------------
def vlength(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def vdot(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]


def angle(v1, v2):
    #print('--', vdot(v1, v2)/vlength(v1)/vlength(v2))
    #print(math.acos(vdot(v1, v2)/vlength(v1)/vlength(v2)))
    cos_value = vdot(v1, v2)/(vlength(v1)+0.01)/(vlength(v2)+0.01)
    if cos_value > 1:
        cos_value = 1
    if cos_value < -1:
        cos_value = -1
    return math.acos(cos_value)*(180/math.pi)
