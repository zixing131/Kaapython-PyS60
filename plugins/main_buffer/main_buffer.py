# -*- coding: utf-8 -*-
# main_buffer.py by dimy44

import appuifw2 as aw
import e32
import sys
import os
import time
from keycapture import KeyCapturer
import windows_info
import imp
from kaapython import app

class Buffer:
    __module__ = __name__

    def __init__(s):
        s.path = '%s\\plugins\\main_buffer\\' %os.path.dirname(sys.argv[0])
        s.list = []
        s.index = 0
        s.capture = KeyCapturer(s.control_of_buffer)
        s.capture.keys = [63554, 0xf862]
        s.capture.forwarding = 1
        s.capture.start()
        s.info = windows_info.Window()
        try:
            s.clipboard = imp.load_dynamic('clipboard', 'C:\\sys\\bin\\clipboard2.pyd')
        except Exception:
            try:
                s.clipboard = imp.load_dynamic('clipboard', 'E:\\sys\\bin\\clipboard2.pyd')
            except Exception:
                s.clipboard = imp.load_dynamic('clipboard', 'F:\\sys\\bin\\clipboard2.pyd')


    def control_of_buffer(s, c):
            try:
                s.list = eval(open('%ssource' %s.path, "r").read())
            except Exception:
                s.list = []
            txt = s.clipboard.Get().encode("utf-8")
            if not txt: return None
            if s.list:
                if txt in [i[1] for i in s.list]:
                    return None
            s.list.insert(0, [time.strftime('%Y%m%d%H%M%S'), txt])
            if len(s.list) > app.settings.plugins.main_buffer.length_of_history:
                s.list.pop(-1)
            open('%ssource' %s.path, 'w').write(repr(s.list))
            e32.ao_yield()

    def delete_copy(s):
        try:
            s.list.pop(s.index)
        except IndexError:
            return None
        if s.list:
            open('%ssource' %s.path, 'w').write(repr(s.list))
            if s.index > len(s.list) - 1:
                s.index -= 1
            s.startinfo(arg = 1)
        else:
            os.remove('%ssource' %s.path)
            s.info.stop()
            s.stopinfo()


    def startinfo(s, arg=None, move=None):
        if not s.list:
            aw.note('Нет сохраненных копий'.decode("utf-8"))
            return None
        def window():
            i = s.index
            m = ('янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек')
            t = s.list[i][0]
            s.info.start(s.list[i][1].decode("utf-8"), lambda: s.stopinfo(1), s.delete_copy, s.stopinfo, s.startinfo)
            aw.app.title = u'[%d/%d] %s %s\n%s : %s : %s' %(i + 1, len(s.list), t[6:8], m[int(t[4:6]) - 1], t[8:10], t[10:12], t[12:14])
            e32.ao_yield()
        if not arg:
            s.capture.stop()
            s.old_title = aw.app.title
        elif arg and move == 63495:
            s.index -= 1
            if s.index < 0:
                s.index = len(s.list) - 1
            window()
        elif arg and move == 63496:
            s.index += 1
            if s.index > len(s.list) - 1:
                s.index = 0
            window()
        if not move:
            window()


    def stopinfo(s, arg=None):
        aw.app.title = s.old_title
        s.capture.start()
        if arg:
            aw.app.body.add(s.list[s.index][1].decode("utf-8"))
        s.index = 0

