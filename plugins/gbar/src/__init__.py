import time
import e32
from graphics import Image, FONT_ANTIALIAS
from fgimage import FGImage
from appswitch import application_list
import kaapython
import ui
_timer = e32.Ao_timer()
((width, height,), (x, y,),) = ui.layout(ui.EControlPane)
gbar = FGImage()
image = Image.new((width,
 height))
_ = kaapython.get_plugin_translator(__file__)
kaapython.app.settings.plugins.append('gbar', ui.SettingsGroup(_('Graphical Bar')))
kaapython.app.settings.plugins.gbar.append('time_interval', ui.FloatSetting(_('Time interval'), value=0.5, vmin=0.1, vmax=60))



def info(self=None, python=kaapython.PythonFileWindow, settings=kaapython.app.settings.plugins.gbar):
    _timer.cancel()
    if (application_list(1)[0] != u'Kaapython'):
        gbar.unset()
        return _timer.after(settings.time_interval, info)
    if self is None:
        self = ui.screen.windows[0]
    if self.__class__ == python:
        pos = self.body.get_pos()
        if (self.body.pos2xy(pos)[1] + 5) >= y:
            gbar.unset()
            return _timer.after(settings.time_interval, info)
        text = self.body.get(0, pos)
        lines = text.count(u'\u2029') + 1
        line = text[(text.rfind(u'\u2029') + 1):]
        indent = len(line) - len(line.lstrip())
        image.clear(0)
        image.text((1,
         ((height / 2) - 1)), ((u'i:%4d|L:%7d|%8.2f%%|' % (indent,
         lines,
         (pos / ((self.body.len() / 100.0) or 1)))) + unicode((time.strftime('%H:%M:%S', time.localtime(time.time())) + (' $%d' % self.shortcut_mode)))), fill=(255,
         255,
         255), font=(None,
         (height / 2),
         FONT_ANTIALIAS))
        image.text((1,
         (height - 1)), (u'w:%2d|e:%s|%s' % ((len(ui.screen.windows) - 1),
         self.encoding,
         self.title)), fill=(255,
         255,
         255), font=(None,
         (height / 2),
         FONT_ANTIALIAS))
        gbar.set(x, y, image._bitmapapi())
    else:
        gbar.unset()
    return _timer.after(settings.time_interval, info)


def new_open(self, focus=True):
    info(self)
    old_open(self, focus)

old_open = kaapython.repattr(kaapython.Window, 'open', new_open)

