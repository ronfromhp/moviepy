from moviepy.editor import CompositeVideoClip
import numpy as np

def tile(clip): 
    """Replaces each frame at time t by the mean of `nframes` equally spaced frames
    taken in the interval [t-d, t+d]. This results in motion blur."""

    def filter(gf, t):
        # Calculate the start time
        rgb_image= gf(t)

        symmetric_padded_rgb_image = np.pad(rgb_image,((int(rgb_image.shape[0]), int(rgb_image.shape[0])),  (int(rgb_image.shape[1]),int( rgb_image.shape[1])),  (0, 0)), mode='symmetric')
        
        return symmetric_padded_rgb_image

    return clip.transform(filter)