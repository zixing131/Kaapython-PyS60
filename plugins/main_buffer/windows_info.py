

from fgimage import FGImage
from graphics import Image
import appuifw2 as aw
from keycapture import KeyCapturer
import akntextutils

class Window:
    __module__ = __name__
    
    def __init__(s):
        s.capture = KeyCapturer(s.keys_answer)
        s.window = FGImage()
        try:
            s.layout = aw.app.layout(aw.EMainPane)
        except AttributeError:
            s.layout = ((176, 144), (0, 44))
        s.size = s.layout[0]
        s.imgnone = Image.new((1, 1))
        s.focusflag = 0
        s.resource = None
        s.color_window =  0xffffbb
        s.color_outline = 0xaa9050
        s.color_text =  0
        s.color_indicator = 0xff8000
        s.y, s.z = 0, 0


    def start(s, resource, callback=lambda: None, func_delete=lambda: None, stop_callback=lambda: None, func_vector=lambda: None):
        s.y, s.z = 0, 0
        y = 0
        s.resource = resource
        s.callback = callback
        s.func_delete = func_delete
        s.stop_callback = stop_callback
        s.func_vector = func_vector
        if not s.resource:
            return None
        s.list = akntextutils.wrap_text_to_array(s.resource, 'annotation', s.size[0] - 25)
        s.lenlist = len(s.list)
        s.max_str_display = s.size[1] / 20
        s.imgsize = (s.size[0] - 10, min(s.max_str_display * 20, s.lenlist * 20))
        try:
            del s.img
        except AttributeError:
            pass
        s.img = Image.new(s.imgsize)
        s.capture.keys = [63495, 63496, 63497, 63498, 63557, 63554, 63555, 35, 42, 63586, 8] + range(48, 58)
        s.capture.forwarding = 0
        aw.app.focus = s.focus
        s.capture.start()
        s.picture()

    def focus(s, f):
        if not f:
            s.window.unset()
            s.capture.stop()
        else:
            if s.focusflag:
                s.window.set(5, s.layout[1][1], s.img._bitmapapi())
                s.capture.start()

    def stop(s):
            s.window.unset()
            s.capture.stop()
            s.focusflag = 0

    def keys_answer(s, code):
        if code == 63498:
            if s.z < s.lenlist - s.max_str_display:
                s.z += 1
        elif code == 63497:
            if s.z > 0:
                s.z -= 1
        elif code == 8:
            s.func_delete()
            return None
        elif code == 63495 or code == 63496:
            s.func_vector(1, code)
            return None
        elif code == 63554 or code == 63557:
            s.callback()
            s.stop()
            return None
        else:
            s.stop_callback()
            s.stop()
            return None
        s.picture()

    def picture(s):
        s.img.rectangle((0, 0, s.imgsize[0], s.imgsize[1]), s.color_outline, s.color_window)
        a = 0
        for t in s.list[s.z:s.max_str_display + s.z]:
            color = s.color_text
            s.img.text((3, a * 20 + 15), t, color, 'annotation')
            a += 1
        if s.lenlist > s.max_str_display:
            s.img.rectangle((s.imgsize[0] - 5, 1, s.imgsize[0] - 1, s.imgsize[1] - 1), fill=s.color_window)
            s.img.rectangle((s.imgsize[0] - 4, s.z * (s.imgsize[1] - 2) / s.lenlist + 1, s.imgsize[0] - 2, s.z * (s.imgsize[1] - 2) / s.lenlist + max(s.max_str_display * (s.imgsize[1] - 2) / s.lenlist, 1) + 1), fill = s.color_indicator)
        s.window.set(5, s.layout[1][1], s.img._bitmapapi())
        s.focusflag = 1
