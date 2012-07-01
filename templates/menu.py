import appuifw
from e32 import Ao_lock

def std_target():
    appuifw.note(unicode(appuifw.app.body.current()))

def item_factory(title=None, target=None, submenu=None):
    item = {'title': title}
    if submenu: item['submenu'] = submenu
    if target: item['target'] = target
    return item

_ = item_factory

struct = []
struct.append(_(
    (u'Item No.0', u'[submenu]'),
    submenu=[
        _((u'Item No.0', u'[description]'), target=std_target),
        _((u'Item No.1', u'[description]'), target=std_target),
        _((u'Item No.2', u'[description]'), target=std_target)
        ]))

level = []

def select_click():
    id = listbox.current()
    level.append(id)
    item = struct
    for i in level:
        try: item = item['target']
        except (KeyError, TypeError):
            try: item = item['submenu']
            except (KeyError, TypeError):
                item = item[i]
    submenu, target = item.get('submenu', None), item.get('target', None)
    if target is None:
        listbox.set_list([i['title'] for i in submenu])
        appuifw.app.exit_key_handler = lambda: listbox.set_list(main_body) or len(level) > 1 and level.pop()
    else:
        target()

main_body = [i['title'] for i in struct]

listbox = appuifw.Listbox(main_body, select_click)

appuifw.app.body = listbox

lock = Ao_lock()
appuifw.app.exit_key_handler = lock.signal
lock.wait()
