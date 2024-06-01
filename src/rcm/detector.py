import cv2
import numpy as np
from .knn import Knn


class Detector:
    def __init__(self, camera=0):
        self.camera = cv2.VideoCapture(camera)
        self.camera_center = (int(self.camera.get(3) / 2), int(self.camera.get(4) / 2))
        self.cal_cordintes()
        self.knn = Knn()
    
    def cal_cordintes(self):
        self.cordintes = np.array([])
        block_size = 130
        offset_camera_center = (self.camera_center[0] - block_size, self.camera_center[1] - block_size)
        for i in range(3):
            for j in range(3):
                point1 = (offset_camera_center[0] + (i - 1) * block_size, offset_camera_center[1] + (j - 1) * block_size)
                point2 = (offset_camera_center[0] + (i) * block_size, offset_camera_center[1] + (j) * block_size)
                self.cordintes = np.append(self.cordintes, [point1, point2])
        self.cordintes = self.cordintes.reshape((9, 2, 2)).astype(int)
    
    def update_frame(self):
        _, frame = self.camera.read()
        self.frame = frame
        return frame
    
    def draw_face_cordinates(self, frame):
        for cordinate in self.cordintes:
            point1 = tuple(cordinate[0])
            point2 = tuple(cordinate[1])
            cv2.rectangle(frame, point1, point2, (255, 255, 255), 2)
        return frame
    
    def detect_color(self, frame=None):
        if not frame:
            frame = self.frame
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frames = []
        for cordinate in self.cordintes:
            frames.append(frame_hsv[cordinate[0, 1]:cordinate[1, 1], cordinate[0, 0]:cordinate[1, 0]])
        feature_matrix = np.zeros((9, 2))
        for i, face in enumerate(frames):
            hue = face[..., 0].flatten()
            sat = face[..., 1].flatten()
            hist_hue, hist_sat = np.histogram(hue, bins=np.arange(256)), np.histogram(sat, bins=np.arange(256))
            feature_matrix[i] = [np.argmax(hist_hue[0]), np.argmax(hist_sat[0])]
        colors = self.knn.predict_color(feature_matrix)
        return colors
        # print(self.knn.predict_color(feature_matrix))
        
    def show_frame(self, frame):
        cv2.imshow('frame', frame)


if __name__ == '__main__':
    detector = Detector()
    while True:
        frame = detector.update_frame()
        frame_face_cordinates = detector.draw_face_cordinates(frame)
        detector.detect_color(frame_face_cordinates)
        detector.show_frame(frame_face_cordinates)
        if (cv2.waitKey(1) == 27):  # esc key
            break