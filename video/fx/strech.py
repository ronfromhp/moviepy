import cv2
import numpy as np
import math

# def strech(clip,direction="center",max=2, x=math.exp):
#     """ Replaces each frame at time t by the mean of `nframes` equally spaced frames
#     taken in the interval [t-d, t+d]. This results in motion blur."""

#     def timecurve(absT):
#         if clip.duration:
#             t = absT/clip.duration
#         else: t=0

#         return 1+ max*x(t)
#         # return 1+(max/x(1))*x(t)
    
#     def fl(gf, t):
   
#         oImage = gf(t)
#         w= oImage.shape[0]
#         h= oImage.shape[1]
#             # img = cv2.imread('your_image.jpg')
#         res = cv2.resize(gf(t),dsize=(0,0), fx=timecurve(t),fy=1, interpolation=cv2.INTER_CUBIC)
        
#         if(direction== "left"):
#             res = res[res.shape[0]-w:res.shape[0], res.shape[1]-h:res.shape[1]]
#         if(direction== "right"):
#             res = res[0:w:,0:h]
#         if(direction== "center"):
#             res = res[res.shape[0]/2-w/2:res.shape[0]/2+w/2, res.shape[1]/2-h/2:res.shape[1]/2+h/2]
#         return res

#     return clip.transform(fl)



def strech(clip, direction="center",axis="horizontal" , max=2, x=math.exp ):
    """ Replaces each frame at time t by the mean of `nframes` equally spaced frames
    taken in the interval [t-d, t+d]. This results in motion blur."""

    def timecurve(absT):
        if clip.duration:
            t = absT/clip.duration
        else: 
            t = 0

        return 1 + max * x(t)

    def fl(gf, t):

        oImage = gf(t)
        w = oImage.shape[0]
        h = oImage.shape[1]

        if axis == "horizontal":
            res = cv2.resize(gf(t), dsize=(0, 0), fx=timecurve(t), fy=1, interpolation=cv2.INTER_CUBIC)
        elif axis == "vertical":
            res = cv2.resize(gf(t), dsize=(0, 0), fx=1, fy=timecurve(t), interpolation=cv2.INTER_CUBIC)
        
        if direction == "left" or direction == "up":
            res = res[res.shape[0]-w:, res.shape[1]-h:]
        elif direction == "right" or direction == "down":
            res = res[:w, :h]
        elif direction == "center":
            res = res[int(res.shape[0]/2-w/2):int(res.shape[0]/2+w/2), int(res.shape[1]/2-h/2):int(res.shape[1]/2+h/2)]
        
        return res

    return clip.transform(fl)

