from rcm.detector import Detector
from cube_map import CubeMap


if __name__ == '__main__':
    detector = Detector()
    cube_map = CubeMap(detector)
    cube_map.show_map()
    while True:
        # detector
        detector.update_frame()
        detector.draw_face_cordinates()
        
        # cube_map
        cube_map.event_handler()
        
        detector.show_frame()