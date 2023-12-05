import cv2
import MAP

def drawTargets(map_draw=None):
    if map_draw is None:
        map_img = MAP.getMap()
        map_draw = cv2.merge((map_img, map_img, map_img))
    cv2.drawMarker(map_draw, MAP.TARGET_POSITION, (0,255,0),
                markerType=cv2.MARKER_TILTED_CROSS,
                markerSize=10, thickness=2)
    cv2.drawMarker(map_draw, MAP.CAR_POSITION, (0,0,255),
                markerType=cv2.MARKER_TRIANGLE_UP,
                markerSize=10, thickness=2, line_type=cv2.FILLED)
    return map_draw

def showTargets(map_draw=None, block=False):
    if map_draw is None:
        map_img = MAP.getMap()
        map_draw = cv2.merge((map_img, map_img, map_img))
    cv2.drawMarker(map_draw, MAP.TARGET_POSITION, (0,255,0),
                markerType=cv2.MARKER_TILTED_CROSS,
                markerSize=10, thickness=2)
    cv2.drawMarker(map_draw, MAP.CAR_POSITION, (0,0,255),
                markerType=cv2.MARKER_TRIANGLE_UP,
                markerSize=10, thickness=2, line_type=cv2.FILLED)

    cv2.imshow("MAP", map_draw)

    wait_time = 0 if block else 1
    cv2.waitKey(wait_time)
    return map_draw

def showCost(cost_grid, block=False, wait_time=1):
    heatmap = cv2.applyColorMap(cost_grid, cv2.COLORMAP_JET)
    mask_cost = 255 - cv2.inRange(cost_grid, 0, 1)
    heatmap = cv2.bitwise_and(heatmap, heatmap, mask=mask_cost)
    map_draw = drawTargets(heatmap)

    cv2.imshow("COST MAP", heatmap)

    if block:
        wait_time = 0
    cv2.waitKey(wait_time)
    return map_draw


def showPath(path, map_draw=None, block=False):
    if map_draw is None:
        map_img = MAP.getMap()
        map_draw = cv2.merge((map_img, map_img, map_img))

    for i, point in enumerate(path):
        cv2.drawMarker(map_draw, point, (255,0,0),
                markerType=cv2.MARKER_SQUARE,
                markerSize=5, thickness=2, line_type=cv2.FILLED)
        if i < len(path) - 1:
            cv2.line(map_draw, point, path[i + 1], [255, 0, 0], 2) 

    cv2.imshow("MAP", map_draw)

    wait_time = 0 if block else 1
    cv2.waitKey(wait_time)
    return map_draw

def getTargetPose():
    return MAP.getTargetPose()
