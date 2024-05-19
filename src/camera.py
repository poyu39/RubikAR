import cv2
import numpy as np
import argparse

class Camera:
    def __init__(self, id=0):
        self.cap = cv2.VideoCapture(id)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.frame = None
        self.masks = {
            'red': ([163, 107,  11], [180, 255, 255]),
            'blue': ([79, 155, 50], [107, 255, 255]),
            'yellow': ([17, 58, 50], [34, 255, 255]),
            'orange': ([5, 130, 50], [20, 255, 255]),
            'green': ([68, 86, 50], [89, 255, 255]),
            'white': ([0, 0, 50], [180, 37, 255])
        }
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        self.frame = frame
    
    def release(self):
        self.cap.release()
        
    def __del__(self):
        self.release()
    
    def update(self):
        self.get_frame()
    
    def draw_contours(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 用面積排序
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        # 只取矩形
        contours_squre = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                contours_squre.append(approx)
        # 取面積最相似的 9 個方塊
        contours_squre = contours_squre[:9]
        for contour in contours_squre:
            area = cv2.contourArea(contour)
            if area > 1000:
                cv2.drawContours(self.frame, contour, -1, (0, 255, 0), 3)
    
    def show(self):
        cv2.imshow('frame', self.frame)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int, default=0)
    args = parser.parse_args()
    cam = Camera(args.id)
    while True:
        cam.update()
        cam.draw_contours()
        cam.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()