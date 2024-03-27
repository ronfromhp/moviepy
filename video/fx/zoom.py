resize_possible = True

try:
    # TRY USING OpenCV AS RESIZER
    #raise ImportError #debugging
    import cv2
    import numpy as np
    def resizer (pic, newsize):
        lx, ly = int(newsize[0]), int(newsize[1])
        if lx > pic.shape[1] or ly > pic.shape[0]:
            # For upsizing use linear for good quality & decent speed
            interpolation = cv2.INTER_LINEAR
        else:
            # For dowsizing use area to prevent aliasing
            interpolation = cv2.INTER_AREA
        return cv2.resize(+pic.astype('uint8'), (lx, ly),
                          interpolation=interpolation)

    resizer.origin = "cv2"
                
except ImportError:
    
    
    try:
        # TRY USING PIL/PILLOW AS RESIZER
        from PIL import Image
        import numpy as np
        def resizer(pic, newsize):
            newsize = list(map(int, newsize))[::-1]
            shape = pic.shape
            if len(shape)==3:
                newshape = (newsize[0],newsize[1], shape[2] )
            else:
                newshape = (newsize[0],newsize[1])
                
            pilim = Image.fromarray(pic)
            resized_pil = pilim.resize(newsize[::-1], Image.ANTIALIAS)
            #arr = np.fromstring(resized_pil.tostring(), dtype='uint8')
            #arr.reshape(newshape)
            return np.array(resized_pil)
            
        resizer.origin = "PIL"
            
    except ImportError:
        # TRY USING SCIPY AS RESIZER
        try:
            from scipy.misc import imresize
            resizer = lambda pic, newsize : imresize(pic,
                                            map(int, newsize[::-1]))
            resizer.origin = "Scipy"
                                               
        except ImportError:
            resize_possible = False
            
        
        
    
from moviepy.decorators import apply_to_mask


def zoom(clip, newsize=None,x= lambda t:t, apply_to_mask=True):
  


    def timecurve(absT):
        if clip.duration:
            t = absT/clip.duration
        else: t=0

        return 1+ (newsize-1)*x(t)

    w, h = clip.size
        
       
    def trans_newsize(ns):
        
        if isinstance(ns, (int, float)):
            return [ns * w, ns * h]
        else:
            return ns
            
        
    newsize2 = lambda t : trans_newsize(timecurve(t))
    
    if clip.is_mask:
        
        fun = lambda gf,t: (1.0*resizer((255 * gf(t)).astype('uint8'),
                                            newsize2(t))/255)
    else:
        
        fun = lambda gf,t: resizer(gf(t).astype('uint8'),
                                    newsize2(t))
        
    return clip.transform(fun, keep_duration=True,
                    apply_to= (["mask"] if apply_to_mask else []))
        

    

        
        
  


if not resize_possible:
    
    # doc = resize.__doc__
    def resize(clip, newsize=None, height=None, width=None):
        raise ImportError("fx resize needs OpenCV or Scipy or PIL")
    # resize.__doc__ = doc
