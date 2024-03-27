def scale(
    clip,
    x1=None,
    y1=None,
    x2=None,
    y2=None,
    width=None,
    height=None,
    x_center=None,
    y_center=None,
    scale=None
    
):  
    def timecurve(absT):
        if clip.duration:
            t = absT/clip.duration
        else: t=0

        return startsize+ (newsize-1)*x(t)

    def filter(gf, t):
        # Calculate the start time
       
        fac = lambda x,y : tuple(z/y for z in x.size)
        if scale is not None:
            x_center,y_center = fac(clip,2)
            width,height = fac(clip,scale)

        if width and x1 is not None:
            x2 = x1 + width
        elif width and x2 is not None:
            x1 = x2 - width

        if height and y1 is not None:
            y2 = y1 + height
        elif height and y2 is not None:
            y1 = y2 - height

        if x_center:
            x1, x2 = x_center - width / 2, x_center + width / 2

        if y_center:
            y1, y2 = y_center - height / 2, y_center + height / 2

        


    x1 = x1 or 0
    y1 = y1 or 0
    x2 = x2 or clip.size[0]
    y2 = y2 or clip.size[1]

       
       
       
       
       
       
       
       
       
        start = max(0, t-d)
        tt = np.linspace(start, t, nframes)

        # Fetch frames and stack them along a new axis for efficient mean computation
        frames = np.stack([gf(t_) for t_ in tt])

        # Compute the mean along the new axis and convert the result to 'uint8'
        avg = np.mean(frames, axis=0).astype('uint8')
        return  lambda frame: frame[int(y1) : int(y2), int(x1) : int(x2)], apply_to=["mask"]

    return clip.image_transform(filter)
       
    