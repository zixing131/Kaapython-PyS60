#table.py by dimy44

from fgimage import FGImage
from graphics import Image
import appuifw2 as aw
from keycapture import KeyCapturer
import resource

aw.e32.ao_yield()

def ru(text):
    return text.decode('utf-8')


class Table:
    __module__ = __name__

    def __init__(s, images, callback, screen='normal'):
        s.images = images
        s.list_s = resource.list_s
        s.list_coords = resource.list_coords
        s.callback = callback
        s.screen = screen
        s.window = FGImage()
        try:
            sz = aw.app.layout(aw.EMainPane)
            if screen == 'large':
                s.layout = ((sz[0][0], sz[0][1]+sz[1][1]), (0, 0))
            elif screen == 'normal':
                s.layout = sz
        except AttributeError:
            if screen == 'large':
                s.layout = ((176, 188), (0, 0))
            elif screen == 'normal':
                s.layout = ((176, 144), (0, 44))
        s.capture = KeyCapturer(s.move)
        s.coordX, s.coordY, s.dislocation_y, s.focus_flag = 0, 0, 0, 0
        s.index = None
        s.start_edit = 0
        s.flag_edit = 0


    def move(s, code):
        if code == 0xf862:
            s.start_edit = 1
            aw.app.title = 'Начало редактирования:'.decode("utf-8")
        elif code == 63555:
            s.stop_menu()
            return None
        elif code in xrange(48, 58):
            c = int(chr(code)) - 1
            if c < 0: c = 9
            if len(s.list_s) < c + 1:
                return None 
            s.coordY = c / s.abreast_x
            s.coordX = c % s.abreast_x
            code = 63557
        elif code == 42: # '*'
            if len(s.list_s) < 11:
                return None 
            s.coordY = 10 / s.abreast_x
            s.coordX = 10 % s.abreast_x
            code = 63557
        elif code == 35: # '#'
            if len(s.list_s) < 12:
                return None 
            s.coordY = 11 / s.abreast_x
            s.coordX = 11 % s.abreast_x        
            code = 63557
        elif code == 63495: 
            if s.coordX == 0 and s.coordY == 0 : 
                s.picture()
                return None
            s.coordX -= 1
            if s.coordX < 0 : 
                s.coordX = s.abreast_x - 1
                s.coordY -= 1
                if (s.coordY + s.dislocation_y) < 0 : 
                    s.dislocation_y += 1
        elif code == 63496 : 
            if (s.coordX == (s.distribution_icons[1] - 1) and s.coordY == (s.abreast_full_y - 1)) or (s.coordY == (s.abreast_full_y - 1) and s.coordX == s.abreast_x - 1):
                s.picture()
                return None
            s.coordX += 1
            if s.coordX > (s.abreast_x - 1) : 
                s.coordX = 0
                s.coordY += 1
                if (s.coordY + s.dislocation_y) > (s.abreast_layout_y - 1) : 
                    s.dislocation_y -= 1
        elif code == 63497:
            if s.coordY == 0 : 
                s.coordY = s.abreast_full_y - 1
                if s.coordX > (s.distribution_icons[1] - 1)  and  s.distribution_icons[1] > 0:
                    s.coordX = s.distribution_icons[1] - 1
                if s.abreast_full_y > s.abreast_layout_y: 
                    s.dislocation_y = - s.coordY + s.abreast_layout_y - 1
                s.picture()
                return None
            s.coordY -= 1
            if (s.coordY + s.dislocation_y) < 0:
                s.dislocation_y += 1
        elif code == 63498 : 
            if s.coordY == s.abreast_full_y - 1: 
                s.coordY = 0
                if s.abreast_full_y > s.abreast_layout_y:
                    s.dislocation_y = 0
                s.picture()
                return None
            s.coordY += 1
            if s.coordY == s.distribution_icons[0] and s.coordX > s.distribution_icons[1] - 1 and  s.distribution_icons[1] > 0: 
                s.coordX = (s.distribution_icons[1] - 1)
            if (s.coordY + s.dislocation_y) > (s.abreast_layout_y - 1) : 
                s.dislocation_y -= 1
        if code == 63557 or code == 63554:
            if s.start_edit:
                if not s.flag_edit:
                    aw.app.title = 'Пункт выбран'.decode("utf-8")
                    s.list_s2 = s.list_s[:]
                    s.list_coords2 = s.list_coords[:]
                    s.old_s = s.list_s2.pop(s.coordY * s.abreast_x + s.coordX)
                    s.old_coords = s.list_coords2.pop(s.coordY * s.abreast_x + s.coordX)
                    s.flag_edit = 1
                else:
                    aw.app.title = 'Пункт вставлен'.decode("utf-8")
                    s.list_s2.insert(s.coordY * s.abreast_x + s.coordX, s.old_s)
                    s.list_coords2.insert(s.coordY * s.abreast_x + s.coordX, s.old_coords)
                    s.list_s = s.list_s2
                    s.list_coords = s.list_coords2
                    s.flag_edit = 0
                    open(resource.__file__, 'w').writelines(['list_s = %s\n' %repr(s.list_s), 'list_coords = %s\n' %repr(s.list_coords)])
                    x, y = 0, 0
                    for i in s.list_coords:
                        s.img_1.blit(s.images, source = i, target = (x * s.icon_size_x, y *s.icon_size_y))
                        x += 1
                        if x == s.abreast_x : 
                            x = 0
                            y += 1
            else:
                s.stop_menu()
                s.index = s.coordY * s.abreast_x + s.coordX
                s.callback(s.list_s[s.index])
                return None
        s.picture()

    def picture(s):
        source = (s.coordX * s.icon_size_x, s.coordY * s.icon_size_y,  s.coordX * s.icon_size_x + s.icon_size_x, s.coordY * s.icon_size_y + s.icon_size_y)
        x, y = 0, 0
        for i in s.list_s:
            s.img_1.rectangle((x * s.icon_size_x, y * s.icon_size_y,  x * s.icon_size_x + s.icon_size_x, y * s.icon_size_y + s.icon_size_y), s.color_background, width=2)
            x += 1
            if x == s.abreast_x:
                x = 0
                y += 1
        s.img_1.rectangle(source, s.color_cursor, width=2)
        x, y = 0, 0
        for i in [u'%d' %i for i in xrange(1, 11)] + [u'*', u'#']:
            if i == u'10': i = u'0'
            s.img_1.text((x * s.icon_size_x + s.icon_size_x - 12, y * s.icon_size_y + s.icon_size_y - 3), i, 0xdd0000, (None, 12))
            x += 1
            if x == s.abreast_x:
                x = 0
                y += 1
        s.img.blit(s.img_1, target = (0, s.dislocation_y * s.icon_size_y))
        s.window.set(s.sh_x, s.layout[1][1] + s.sh_y, s.img._bitmapapi())

    def initialization(s):
        try:
            s.color_background = s.color_background
        except AttributeError:
            s.color_background = 0xffffff
        try:
            s.color_cursor = s.color_cursor
        except AttributeError:
            s.color_cursor = 0xcccccc
        s.icon_size_x = s.icon_size_y = s.images.size[1]
        s.abreast_x = s.layout[0][0] / s.icon_size_x
        s.abreast_layout_y = s.layout[0][1] / s.icon_size_y
        s.distribution_icons = divmod(len(s.list_s), s.abreast_x)
        if s.distribution_icons[1] : 
            s.abreast_full_y = s.distribution_icons[0] + 1
        else : 
            s.abreast_full_y = s.distribution_icons[0]
        s.sh_x = (s.layout[0][0] - s.abreast_x * s.icon_size_x) / 2
        s.sh_y = (s.layout[0][1] - s.abreast_layout_y * s.icon_size_y) / 2
        s.total_size = (s.abreast_x * s.icon_size_x, s.icon_size_y * s.abreast_full_y)
        s.img_1 = Image.new(s.total_size)
        s.img_1.clear(s.color_background)
        s.img = Image.new((s.total_size[0], min(s.layout[0][1] - s.sh_y * 2, s.total_size[1])))
        x, y = 0, 0
        for i in s.list_coords:
            s.img_1.blit(s.images, source = i, target = (x * s.icon_size_x, y *s.icon_size_y))
            x += 1
            if x == s.abreast_x : 
                x = 0
                y += 1


    def start_menu(s):
        s.title = aw.app.title
        s.screen_old = aw.app.screen
        aw.app.screen = s.screen
        s.focus_flag = 1
        s.capture.keys = [
            63495, 
            63496, 
            63497, 
            63498, 
            63557, 
            63554, 
            63555, 
            35, 
            42, 
            0xf862
            ]
        s.capture.keys += range(48, 58)
        s.capture.forwarding = 0
        s.capture.start()
        aw.app.focus = s.focus
        s.picture()

    def stop_menu(s):
        aw.app.title = s.title
        aw.app.screen = s.screen_old
        s.focus_flag = 0
        s.window.unset()
        s.capture.stop()
        s.start_edit = s.flag_edit = 0

    def focus(s, f):
        if f:
            if s.focus_flag:
                s.window.set(s.sh_x, s.layout[1][1] + s.sh_y, s.img._bitmapapi())
                s.capture.start()
        else:
                s.window.unset()
                s.capture.stop()