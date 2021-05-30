import math

class Gene():

    def __init__(self, center, radius, colors, width, height):
        
        if(not self.collision(0, 0, width, height, center[0], center[1], radius)):
            self.center = center
            self.radius = radius
            self.valid = False
        else:
            self.center = center
            self.radius = radius
            self.valid = True

        if len(colors) != 4:
            print("Missing color value. Correct syntax: (R, G, B, ALPHA)")
            exit()
        elif (False in [(0 <= color <= 255) for color in colors[:-1]]) or (not 0 <= colors[-1] <= 1):
            print("Invalid color value! The correct value range: 0<=RGB<=255 and 0<=A<=1")
            exit()
        else:
            self.colors = colors[:-1]
            self.alpha = colors[-1]
        
    def collision(self, rleft, rtop, width, height,   # rectangle definition
                center_x, center_y, radius):  # circle definition
        """ Detect collision between a rectangle and circle. """

        # complete boundbox of the rectangle
        rright, rbottom = rleft + width, rtop + height

        # bounding box of the circle
        cleft, ctop     = center_x-radius, center_y-radius
        cright, cbottom = center_x+radius, center_y+radius

        # trivial reject if bounding boxes do not intersect
        if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
            return False  # no collision possible

        # check whether any point of rectangle is inside circle's radius
        for x in (rleft, rleft+width):
            for y in (rtop, rtop+height):
                # compare distance between circle's center point and each point of
                # the rectangle with the circle's radius
                if math.hypot(x-center_x, y-center_y) <= radius:
                    return True  # collision detected

        # check if center of circle is inside rectangle
        if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
            return True  # overlaid

        return False  # no collision detected