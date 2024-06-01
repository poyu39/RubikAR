import pygame
import kociemba
import sys


class CubeMap:
    def __init__(self):
        '''
            Rubik's cube map
        '''
        self.create_map()
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        self.window.fill((255, 255, 255))
    
    def create_map(self):
        '''
            Create a 3x3x3 Rubik's cube map
            
                U
            L   F   R   B
                D
            
            1   2   3
            4   5   6
            7   8   9
        '''
        self.map = {
            'U': ['W'] * 9,
            'R': ['G'] * 9,
            'F': ['O'] * 9,
            'D': ['Y'] * 9,
            'L': ['B'] * 9,
            'B': ['R'] * 9,
        }
    
    def get_seq_map(self):
        '''
            取得 kociemba 所需要的序列
            
            Return:
                list: sequence of the cube map
        '''
        seq_index = 'URFDLB'
        seq_map = []
        for seq in seq_index:
            for i in range(9):
                seq_map.append(self.map[seq][i])
        return seq_map
    
    def get_position(self, seq, i):
        '''
            取得方塊的位置
            
            Args:
                seq (str): 方塊序列
                i (int): 方塊位置
            
            Return:
                tuple: 方塊的 x, y 座標
        '''
        x = 0
        y = 0
        if seq == 'U':
            x = 300 + (i % 3) * 50
            y = 100 + (i // 3) * 50
        elif seq == 'R':
            x = 450 + (i % 3) * 50
            y = 250 + (i // 3) * 50
        elif seq == 'F':
            x = 300 + (i % 3) * 50
            y = 250 + (i // 3) * 50
        elif seq == 'D':
            x = 300 + (i % 3) * 50
            y = 400 + (i // 3) * 50
        elif seq == 'L':
            x = 150 + (i % 3) * 50
            y = 250 + (i // 3) * 50
        elif seq == 'B':
            x = 600 + (i % 3) * 50
            y = 250 + (i // 3) * 50
        return x, y
    
    def get_color(self, color):
        '''
            取得方塊的顏色
            
            Args:
                color (str): 方塊顏色
            
            Return:
                tuple: 方塊的 RGB 顏色
        '''
        if color == 'W':
            return (255, 255, 255)
        elif color == 'G':
            return (0, 255, 0)
        elif color == 'O':
            return (255, 165, 0)
        elif color == 'Y':
            return (255, 255, 0)
        elif color == 'B':
            return (0, 0, 255)
        elif color == 'R':
            return (255, 0, 0)
        elif color == 'border':
            return (0, 0, 0)
    
    def show_map(self):
        '''
            顯示 Rubik's cube map
        '''
        self.window.fill((255, 255, 255))
        for face in self.map:
            for i, color in enumerate(self.map[face]):
                if color is not None:
                    x , y = self.get_position(face, i)
                    pygame.draw.rect(self.window, self.get_color(color), (x, y, 50, 50))
                    pygame.draw.rect(self.window, self.get_color('border'), (x, y, 50, 50), 1)
        pygame.display.update()
    
    def update(self):
        '''
            更新 Rubik's cube map
        '''
        pass

if __name__ == '__main__':
    cube_map = CubeMap()
    while True:
        cube_map.show_map()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()