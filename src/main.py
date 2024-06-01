from rcm.detector import Detector
from cube_map import CubeMap


if __name__ == '__main__':
    detector = Detector()
    cube_map = CubeMap(detector)
    cube_map.show_map()
    while True:
        # detector
        frame = detector.update_frame()
        frame_face_cordinates = detector.draw_face_cordinates(frame)
        # now_colors = detector.detect_color(frame_face_cordinates)
        detector.show_frame(frame_face_cordinates)
        
        # cube_map
        cube_map.event_handler()