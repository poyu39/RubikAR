import sys
import json

import pygame
from magiccube.cube import Cube, Face
from magiccube.solver.basic.basic_solver import BasicSolver

from rcm.detector import Detector


class CubeMap:
    def __init__(self, dectector: Detector):
        '''
            Rubik's cube map
        '''
        self.create_map()
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        self.window.fill((255, 255, 255))
        
        self.decetor = dectector
        
        # mode
        self.mode = 'init'
        self.now_scan_face = 0
    
    def create_map(self):
        '''
            建立 Rubik's cube map
            
                U
            L   F   R   B
                D
            
            1   2   3
            4   5   6
            7   8   9
        '''
        # 創建空白 map
        self.map = {
            'U': ['X'] * 9,
            'R': ['X'] * 9,
            'F': ['X'] * 9,
            'D': ['X'] * 9,
            'L': ['X'] * 9,
            'B': ['X'] * 9,
        }
        # 每個面中間是固定的顏色
        self.map['U'][4] = 'Y'
        self.map['L'][4] = 'R'
        self.map['F'][4] = 'G'
        self.map['R'][4] = 'O'
        self.map['B'][4] = 'B'
        self.map['D'][4] = 'W'
    
    def get_seq_map(self):
        '''
            取得 magiccube 所需要的序列
            
            Return:
                list: sequence of the cube map
        '''
        face_index = 'ULFRBD'
        seq_map = []
        for face in face_index:
            for i in range(9):
                seq_map.append(self.map[face][i])
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
        elif color == 'X':  # None
            return (128, 128, 128)
        elif color == 'border':
            return (0, 0, 0)
        elif color == 'select': # light blue
            return (137, 235, 242)
    
    def show_map(self, map=None):
        '''
            顯示 Rubik's cube map
        '''
        self.window.fill((255, 255, 255))
        map = map or self.map
        for face in map:
            for i, color in enumerate(map[face]):
                if color is not None:
                    x , y = self.get_position(face, i)
                    pygame.draw.rect(self.window, self.get_color(color), (x, y, 50, 50))
                    pygame.draw.rect(self.window, self.get_color('border'), (x, y, 50, 50), 1)
    
    def update(self):
        '''
            更新 Rubik's cube map
        '''
        pass
    
    def draw_select_box(self, face):
        '''
            繪製選擇框
        '''
        x, y = self.get_position(face, 0)
        pygame.draw.rect(self.window, self.get_color('select'), (x, y, 150, 150), 5)
    
    def scan_map(self, face=None):
        '''
            掃描 Rubik's cube map
        '''
        all_face = 'ULFRBD'
        face = face or all_face[self.now_scan_face]
        colors = self.decetor.detect_color()
        self.tmp_map = self.map.copy()
        self.tmp_map[face] = colors
        self.show_map(self.tmp_map)
        self.draw_select_box(face)
    
    def cube_to_seq_map(self, cube: Cube):
        seq_map = []
        for face in 'ULFRBD':
            seq_map.append(cube.get_face_flat())
        return seq_map
    
    def solve_map(self):
        '''
            解答 Rubik's cube map
        '''
        seq_map = self.get_seq_map()
        seq = ''.join(seq_map)
        self.cube = Cube(3, seq)
        solver = BasicSolver(self.cube)
        self.solution = solver.solve()
        self.now_step = 0
        # 模擬每一步的 map
        self.steps_seq_map = []
        for step in self.solution:
            print(step)
            self.cube.rotate(str(step))
            print(self.cube_to_seq_map(self.cube))
            self.steps_seq_map.append(self.cube.get_all_faces())
    
    def draw_solution_move(self, move):
        '''
            繪製解答箭頭步驟
        '''
        if len(move) == 1:
            move = move + '1'
    
    def draw_solution(self):
        '''
            繪製解答
        '''
        pass
    
    def event_handler(self):
        '''
            事件處理
        '''
        self.title_handler()
        for event in pygame.event.get():
            self.event = event
            self.key_handler()
            self.exit_handler()
            
        pygame.display.update()
    
    def key_handler(self):
        '''
            鍵盤事件處理
        '''
        if self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_s:
                print('scan-map')
                self.mode = 'scan-map'
                self.scan_map()
            elif self.event.key == pygame.K_n:
                if self.mode == 'scan-map' and self.now_scan_face < 5:
                    print('next-face')
                    self.now_scan_face += 1
                    self.map = self.tmp_map
                    self.scan_map()
                elif self.mode == 'scan-map' and self.now_scan_face == 5:
                    print('scan-map-end')
                    self.mode = 'solve'
                    self.now_scan_face = 0
                    self.map = self.tmp_map
                    self.show_map()
                    json.dump(self.map, open('./map.json', 'w'))
                    self.solve_map()
            elif self.event.key == pygame.K_l:
                self.map = json.load(open('./map.json', 'r'))
                self.show_map()
                self.mode = 'solve'
                self.solve_map()
    
    def title_handler(self):
        '''
            標題事件處理
        '''
        if self.mode == 'init':
            text = '請按 s 掃描更新當前的面，如果掃描完畢請按 n 進行下一個面的掃描。'
        elif self.mode == 'scan-map':
            text = '請按 s 掃描更新當前的面，如果掃描完畢請按 n 進行下一個面的掃描。'
        elif self.mode == 'solve':
            text = '解答中...'
        font = pygame.font.Font('./font/msjh.ttc', 18)
        text = font.render(text, True, (0, 0, 0))
        self.window.blit(text, (10, 10))
    
    def exit_handler(self):
        '''
            退出事件處理
        '''
        if self.event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    cube_map = CubeMap()
    while True:
        cube_map.show_map()
        cube_map.event_handler()