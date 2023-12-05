import cv2

MAP_FILE = "cityLargeBin.png"
CAR_POSITION = (290, 250)
TARGET_POSITION = (275, 30)

MAP_WIDTH = 400
MAP_HEIGHT = 400

def getMap():
    map_img = cv2.imread(MAP_FILE, cv2.IMREAD_GRAYSCALE)
    return map_img

def getTargetPose():
    return TARGET_POSITION

def getCarPose():
    return CAR_POSITION

