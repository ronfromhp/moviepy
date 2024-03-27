import cv2
import numpy as np

def blurout(clip, duration, max_blur_size=5):
    """
    Makes the clip progressively blurrier over ``duration`` seconds at the end of the clip.
    The ``max_blur_size`` determines the strength of the blurring effect at the end.
    """

    def filter(get_frame, t):
        if (clip.duration - t) >= duration:
            return get_frame(t)
        else:
            # Calculate the progressive blurring size based on the elapsed time
            blur_strength = (1.0 * (duration - (clip.duration - t)) / duration) * max_blur_size
            blur_size = (int(2 * round(blur_strength/2) + 1), int(2 * round(blur_strength/2) + 1))
            
            # Apply Gaussian blur
            frame = get_frame(t)
            return cv2.GaussianBlur(frame, blur_size, 0)

    return clip.transform(filter)

def blurin(clip, duration, max_blur_size=5):
    """
    Starts the clip with a blurring effect and sharpens it progressively over 
    ``duration`` seconds at the beginning of the clip.
    The ``max_blur_size`` determines the strength of the blurring effect at the start.
    """

    def filter(get_frame, t):
        if t >= duration:
            return get_frame(t)
        else:
            # Calculate the progressive blurring size based on the elapsed time
            blur_strength = (1.0 * (duration - t) / duration) * max_blur_size
            blur_size = (int(2 * round(blur_strength/2) + 1), int(2 * round(blur_strength/2) + 1))
            
            # Apply Gaussian blur
            frame = get_frame(t)
            return cv2.GaussianBlur(frame, blur_size, 0)

    return clip.transform(filter)