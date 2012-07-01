import appuifw
import e32

class KeyHook:
    def __init__(self):
        self.d = 30
        self.step = 5
        self.x = self.y = self.d / 2
    def __call__(self, d):
        if d['scancode'] == 14:
            self.x -= self.step
        elif d['scancode'] == 15:
            self.x += self.step
        elif d['scancode'] == 16:
            self.y -= self.step
        elif d['scancode'] == 17:
            self.y += self.step
        else: return
        tabs[u'text'].add(u'x = %(x)d | y = %(y)d\u2029' % self.__dict__)
        tabs[u'canvas'].clear()
        tabs[u'canvas'].point((self.x, self.y), 0xff, 0xff00, width=30)

key_hook = KeyHook()

tabs = {
    u'canvas': appuifw.Canvas(event_callback=key_hook),
    u'text': appuifw.Text()
    }

def tab_hook(id):
    appuifw.app.body = tabs.values()[id]

appuifw.app.set_tabs(tabs.keys(), tab_hook) 

def exit():
    for body in tabs.keys(): del tabs[body]
    appuifw.app.set_tabs([], lambda x: None)
    lock.signal()

appuifw.app.body = tabs.values()[0]

lock = e32.Ao_lock()
appuifw.app.exit_key_handler = exit
lock.wait()
