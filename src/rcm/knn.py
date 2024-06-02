import numpy as np
import math

class Knn:
    def __init__(self):
        '''
            KNN 演算法
        '''
        f = open('./rcm/dataset/output.txt', 'r')
        data = np.array([])
        line = f.readlines()
        data = np.append(data, line)
        np.random.shuffle(data)
        f.close()
        self.X = np.ones((len(data), 2))
        X1 = np.array([], dtype=int)
        X2 = np.array([])
        self.Y = np.array([])

        for line in data:
            X1 = np.append(X1, int(line.split(',')[0]))
            X2 = np.append(X2, int(line.split(',')[1]))
            self.Y = np.append(self.Y, line.split(',')[2])

        self.X[..., 0] = X1
        self.X[..., 1] = X2

    def predict_color(self, feature_Mat):
        '''
            預測面的顏色 9 個 block
            
            Args:
                feature_Mat: 9 個 block 的特徵矩陣
            Returns:
                final_prediction_seq: 9 個 block 的顏色
        '''
        final_prediction_seq = np.empty(9, dtype=str)
        for i, feature in enumerate(feature_Mat):
            final_prediction_seq[i] = self.predict_single_face_color(feature)
        return list(final_prediction_seq)

    def predict_single_face_color(self, features):
        '''
            預測單一個 block 的顏色
            
            利用 KNN 演算法，找出最近的 20 個點，並取出顏色。
            
            Args:
                features: 一個 block 的特徵
            Returns:
                final_colour: 一個 block 的顏色
        '''
        closest_dist = np.zeros((540))
        closest_label = np.empty(540, dtype=object)
        for i, training in enumerate(self.X):
            Htrain, Strain = training[0], training[1]
            closest_dist[i] = math.sqrt(math.pow((features[0] - Htrain), 2) + math.pow(features[1] - Strain, 2))
            closest_label[i] = self.Y[i]
        u = np.transpose(np.array([closest_dist, closest_label]))
        # drop [0.0 None] values
        u = u[~(u == np.array([0.0, None])).all(1)]
        sorted = u[u[:, 0].argsort()]
        colour = np.unique(sorted[1:20, 1])[0]
        final_colour = str(colour).upper()
        return final_colour