import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# def supersample(clip, d, n_frames):
#     """Replaces each frame at time t by the mean of `n_frames` equally spaced frames
#     taken in the interval [t-d, t+d]. This results in motion blur.
#     """

#     def filter(get_frame, t):
#         timings = np.linspace(t - d, t + d, n_frames)
#         frame_average = np.mean(
#             1.0 * np.array([get_frame(t_) for t_ in timings], dtype="uint16"), axis=0
#         )
#         return frame_average.astype("uint8")

#     return clip.transform(filter)

# @lru_cache(maxsize=None)  # Unlimited cache
# def get_frames(gf, t,d,nframes):
#     if t - d > 0:
#         start = t-d
#     else:
#         start = 0 
#     tt = np.linspace(start, t, nframes)
#     frames = np.array([gf(t_) for t_ in tt], dtype='uint16')
#     return frames


# def supersample(clip, d, nframes): #GPT-4 CODE INTERPRETER
#     """ Replaces each frame at time t by the mean of `nframes` equally spaced frames
#     taken in the interval [t-d, t+d]. This results in motion blur."""
    
#     def filter(gf, t):
#         frames = get_frames(gf, t,d,nframes)
#         avg = np.mean(frames, axis=0).astype('uint8')
#         return avg

#     return clip.transform(filter)





# def supersample(clip, d, nframes): #GPT-4 CODE INTERPRETER
#     """ Replaces each frame at time t by the mean of `nframes` equally spaced frames
#     taken in the interval [t-d, t+d]. This results in motion blur."""
    
#     def filter(gf, t):
#         if t - d > 0:
#             start = t-d
#         else:
#             start = 0 
#         tt = np.linspace(start, t, nframes)
#         frames = np.array([gf(t_) for t_ in tt], dtype='uint16')
#         avg = np.mean(frames, axis=0).astype('uint8')
#         return avg

#     return clip.transform(filter)


def supersample(clip, d, nframes): 
    """Replaces each frame at time t by the mean of `nframes` equally spaced frames
    taken in the interval [t-d, t+d]. This results in motion blur."""

    def filter(gf, t):
        # Calculate the start time
        start = max(0, t-d)
        tt = np.linspace(start, t, nframes)

        # Fetch frames and stack them along a new axis for efficient mean computation
        frames = np.stack([gf(t_) for t_ in tt])

        # Compute the mean along the new axis and convert the result to 'uint8'
        avg = np.mean(frames, axis=0).astype('uint8')
        return avg

    return clip.transform(filter)