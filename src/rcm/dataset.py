import os
import cv2
import numpy as np
import argparse
import random


class Dataset:
    def __init__(self, camera=0, color='r'):
        self.camera = cv2.VideoCapture(camera)
        self.camera_center = (int(self.camera.get(3) / 2), int(self.camera.get(4) / 2))
        self.color = color
        self.cal_cordintes()
    
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
        return frame
    
    def draw_face_cordinates(self, frame):
        for cordinate in self.cordintes:
            point1 = tuple(cordinate[0])
            point2 = tuple(cordinate[1])
            cv2.rectangle(frame, point1, point2, (255, 255, 255), 2)
        return frame
    
    def take_picture(self, frame):
        blocks = []
        for cordinate in self.cordintes:
            blocks.append(frame[cordinate[0, 1]:cordinate[1, 1], cordinate[0, 0]:cordinate[1, 0]])
        if cv2.waitKey(1) == ord('s'):
            for block in blocks:
                dir = f'./dataset/train/{self.color}'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                id = len(os.listdir(dir)) + 1
                f = f'{dir}/{id}.jpg'
                cv2.imwrite(f, block)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', type=str, default='r')
    args = parser.parse_args()
    dataset = Dataset(color=args.color)
    while True:
        frame = dataset.update_frame()
        dataset.take_picture(frame)
        frame_face_cordinates = dataset.draw_face_cordinates(frame)
        cv2.imshow('dectector', frame_face_cordinates)
        if cv2.waitKey(1) == 27:
            break