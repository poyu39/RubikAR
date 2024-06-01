import os
import numpy as np
import cv2
from matplotlib import pyplot as plt


class Output:
    def __init__(self):
        self.f = open('./rcm/dataset/output.txt', 'w')
        self.color = {
            'r': 'red',
            'b': 'blue',
            'g': 'green',
            'y': 'yellow',
            'w': 'grey',
            'o': 'orange'
        }
    
    def histogram_cal(self, hsv, color_id):
        hue = hsv[..., 0].flatten()
        sat = hsv[..., 1].flatten()
        hist_hue = np.histogram(hue, bins=np.arange(256))
        hist_sat = np.histogram(sat, bins=np.arange(256))
        h = np.argmax(hist_hue[0])
        s = np.argmax(hist_sat[0])
        plt.scatter(h, s, color=self.color[color_id])
        self.f.write(f'{h},{s},{color_id},\n')
    
    def __del__(self):
        self.f.close()

if __name__ == '__main__':
    output = Output()
    for folder in os.listdir('./rcm/dataset/train'):
        color_id = str(folder)
        dir = f'./rcm/dataset/train/{color_id}'
        for img in os.listdir(dir):
            pixel = cv2.imread(f'{dir}/{img}')
            hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
            output.histogram_cal(hsv, color_id)
    output.__del__()
    plt.savefig('./rcm/dataset/output.png')
    plt.show()