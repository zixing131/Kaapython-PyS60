from kaapython import app, TextWindow
import e32
import keypress
from key_codes import EKeyPageUp, EStdKeyPageUp, EKeyPageDown, EStdKeyPageDown

def page_up(self):
    keypress.simulate_key(EKeyPageUp, EStdKeyPageUp)
    e32.ao_yield()



def page_down(self):
    keypress.simulate_key(EKeyPageDown, EStdKeyPageDown)
    e32.ao_yield()


app.settings.text.remove('pagesizeport')
app.settings.text.remove('pagesizefull')
app.settings.text.remove('pagesizeland')
setattr(TextWindow, 'move_page_up', page_up)
setattr(TextWindow, 'move_page_down', page_down)

