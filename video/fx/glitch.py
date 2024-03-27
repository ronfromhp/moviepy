from moviepy.editor import VideoClip
import numpy as np

def glitch(clip, max_shift=20):
    """Applies an advanced color glitch effect to the provided clip."""
    
    def effect_fun(frame):
        # Separate RGB channels
        R, G, B = frame[:,:,0], frame[:,:,1], frame[:,:,2]
        
        # Random channel crop and shift
        crop_shift_R = np.random.randint(-max_shift, max_shift)
        crop_shift_G = np.random.randint(-max_shift, max_shift)
        crop_shift_B = np.random.randint(-max_shift, max_shift)
        
        R = np.roll(R, shift=crop_shift_R, axis=np.random.choice([0, 1]))
        G = np.roll(G, shift=crop_shift_G, axis=np.random.choice([0, 1]))
        B = np.roll(B, shift=crop_shift_B, axis=np.random.choice([0, 1]))

        # Occasional blackouts
        if np.random.rand() < 0.05:
            blackout_size = np.random.randint(10, 50)
            blackout_x = np.random.randint(0, frame.shape[0] - blackout_size)
            blackout_y = np.random.randint(0, frame.shape[1] - blackout_size)
            R[blackout_x:blackout_x+blackout_size, blackout_y:blackout_y+blackout_size] = 0
            G[blackout_x:blackout_x+blackout_size, blackout_y:blackout_y+blackout_size] = 0
            B[blackout_x:blackout_x+blackout_size, blackout_y:blackout_y+blackout_size] = 0

        # Color inversion
        if np.random.rand() < 0.1:
            inversion_size = np.random.randint(30, 100)
            inversion_x = np.random.randint(0, frame.shape[0] - inversion_size)
            inversion_y = np.random.randint(0, frame.shape[1] - inversion_size)
            R[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size] = 255 - R[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size]
            G[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size] = 255 - G[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size]
            B[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size] = 255 - B[inversion_x:inversion_x+inversion_size, inversion_y:inversion_y+inversion_size]

        # Recombine channels
        glitched_frame = np.stack([R, G, B], axis=2).astype('uint8')
        return glitched_frame

    return clip.image_transform(effect_fun)

# Note: This creates a more intense and advanced glitch effect. Adjust the probabilities and parameters to fine-tune the appearance.
