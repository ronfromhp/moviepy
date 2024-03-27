# from ..compositing.CompositeVideoClip import CompositeVideoClip
# from ..compositing.concatenate import concatenate_videoclips
from moviepy.editor import *
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.strech import strech
from moviepy.video.fx.curves import *
from moviepy.video.fx.blur import *
from moviepy.video.fx.tile import tile
from moviepy.video.fx.zoom import zoom
from moviepy.video.fx.invert_colors import invert_colors
import inspect


def transitions():
    print("transitions loaded")
    return 0

def crossover(Vd1,Vd2, transitionTime):
    return concatenate_videoclips([Vd1, Vd2.crossfadein(transitionTime)], padding=-1*transitionTime, method="compose")

def blurTransition(Vd1,Vd2, transitionTime):
    Vd1 = Vd1.fx(blurout,transitionTime/2,300)
    Vd2 = Vd2.fx(blurin,transitionTime/2,300)
    return concatenate_videoclips([Vd1,Vd2])

def fadetowhite(Vd1,Vd2, transitionTime):
    return concatenate_videoclips([Vd1.fadeout(transitionTime/2,[255, 255, 255]),
                         Vd2.fadein(transitionTime/2,[255, 255, 255])])

def fadetoblack(Vd1,Vd2, transitionTime):
    return concatenate_videoclips([Vd1.fadeout(transitionTime/2,[0, 0, 0]),
                         Vd2.fadein(transitionTime/2,[0, 0, 0])])


def mattTransition(bgVideo,bgVideo1,matt="vecteezy_glitch-noise-static-television-vfx-pack-visual-video_11405807_954.mp4",duration=1):
    maskVideo = VideoFileClip(matt).subclip(0, duration).to_mask()
    bgVideoTransition = bgVideo.subclip(bgVideo.duration - duration, bgVideo.duration).copy()
    bgVideoTransition.mask =  maskVideo.fx(invert_colors)

    bgVideo1 = CompositeVideoClip([bgVideo1, bgVideoTransition])
    bgVideo = bgVideo.subclip(0, bgVideo.duration - 1)
    clipfile = concatenate_videoclips([bgVideo, bgVideo1])
    return clipfile


def overlayTransition(Video1,Video2,transitionclip,transitionTime=0.5):
    if not transitionclip:
        print("No Transition Overlay Clip")
    else:
        tClip = VideoFileClip(transitionclip,target_resolution=(1920, 1080),has_mask=True).with_fps().subclip(0,transitionTime).copy()
        # tClip.mask = mask_color(tClip).to_mask()

    #Creating Transition clips
    tt1 = transitionTime/2
    tt2 = transitionTime/2

    t1 = Video1.subclip(Video1.duration-tt1,Video1.duration).copy()
    t2 = Video2.subclip(0,tt2).copy()

    t = concatenate_videoclips([t1,t2])
    
    # if transitionclip:
    t = CompositeVideoClip([t,tClip])

    return(concatenate_videoclips([Video1.subclip(0,Video1.duration-tt1),t,Video2.subclip(tt2,Video2.duration)]))

def strechTransition(Vd1,Vd2,direction="left",transitionTime=0.5):
    strechdir = { 'right': ["right","left","horizontal"],
                    'left': ["left","right","horizontal"],
                    'up': ["up","down","vertical"],
                    'down': ["down","up","vertical"]}

    tt1=transitionTime
    tt2=transitionTime
    # print('caller name:', inspect.stack()[1][3])
    # print(f"VD1 start: {Vd1.duration-transitionTime}")
    # print(f"VD1 end: {Vd1.duration}")
    t1 = (
    Vd1.subclip( Vd1.duration-tt1, Vd1.duration).with_fps(150)
    .fx(strech,direction = strechdir[direction][0],axis=strechdir[direction][2],x=easeInQuint)
    .fx(supersample,d=1/150*15 ,nframes=15)
    .with_fps(30)
    )
    # t1 = CompositeVideoClip([t1], size=screensize)
    # t1 = supersample(t1,1/150*15 ,15)
    # t1.with_fps(30)

    t2 = (
        Vd2.subclip(0,transitionTime).with_fps(150)
        .fx(strech,direction= strechdir[direction][1],axis=strechdir[direction][2],x=inverseEaseInQuint)
        .fx(supersample,d=1/150*15 ,nframes=15)
        .with_fps(30)
        )
    # t2 = supersample(t2,1/150*15 ,15)
    # t2.with_fps(30)

    return (concatenate_videoclips([Vd1.subclip(0,Vd1.duration-tt1),t1,t2,Vd2.subclip(tt2,Vd2.duration)]))


def zoomInMotionblur(Vd1,Vd2,transitionTime=0.3):
    screensize = Vd1.size    
    tt1=transitionTime
    tt2=transitionTime

    Vd1 = Vd1.with_fps(30)
    t1 = (
        Vd1.subclip(Vd1.duration-transitionTime,Vd1.duration).with_fps(150)
        .resize(screensize)
        .fx(zoom,2,easeInQuint)
        .with_position(('center', 'center'))
        )

    t1 = CompositeVideoClip([t1], size=screensize)
    t1 = supersample(t1,1/150*15 ,15)
    t1.with_fps(30)

    t2 = (
        Vd2.subclip(0,transitionTime).with_fps(150)
        .fx(tile)
        .crop(scale=2)
        .resize(screensize)
        .fx(zoom,1.5,easeOutQuint)
        .with_position(('center', 'center'))
        )

    t2 = CompositeVideoClip([t2], size=screensize)
    t2 = supersample(t2,d=1/150*15 ,nframes=15)
    t2.with_fps(30)


    Vd1 = Vd1.resize(screensize)
    Vd2 = Vd2.resize(screensize)

    return concatenate_videoclips([Vd1.subclip(0,Vd1.duration-tt1),t1,t2,Vd2.subclip(tt2,Vd2.duration)])

def zoomOutMotionblur(Vd1,Vd2,transitionTime=0.3):
    screensize = Vd1.size    
    tt1=transitionTime
    tt2=transitionTime

    Vd1 = Vd1.with_fps(30)
    t1 = (
        Vd1.subclip(Vd1.duration-transitionTime,Vd1.duration).with_fps(150)
        .fx(tile)
        .crop(scale=2)
        .resize(screensize)
        .fx(zoom,1.5,inverseEaseOutQuint)
        .with_position(('center', 'center'))
        )

    t1 = CompositeVideoClip([t1], size=screensize)
    t1 = supersample(t1,1/150*15 ,15)
    t1.with_fps(30)

    t2 = (
        Vd2.subclip(0,transitionTime).with_fps(150)
        .resize(screensize)
        .fx(zoom,2,inverseEaseInQuint)
        .with_position(('center', 'center'))
        )

    t2 = CompositeVideoClip([t2], size=screensize)
    t2 = supersample(t2,d=1/150*15 ,nframes=15)
    t2.with_fps(30)


    Vd1 = Vd1.resize(screensize)
    Vd2 = Vd2.resize(screensize)

    return concatenate_videoclips([Vd1.subclip(0,Vd1.duration-tt1),t1,t2,Vd2.subclip(tt2,Vd2.duration)])

