class Color:
    def __init__(self):
        self.rgb = {
            'red'   : (0, 0, 255),
            'orange': (0, 165, 255),
            'blue'  : (255, 0, 0),
            'green' : (0, 255, 0),
            'white' : (255, 255, 255),
            'yellow': (0, 255, 255)
        }
    
    def get_closet_color(self, color):
        if color in self.rgb:
            return self.rgb[color]
        return None