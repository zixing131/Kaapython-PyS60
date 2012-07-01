from __future__ import generators

import os
import e32
from appuifw2_Text import *
from key_codes import *
try:
    reset_inactivity = e32.reset_inactivity
except AttributeError:
    try:
        from miso import reset_inactivity
    except ImportError:
        reset_inactivity = lambda: None

try:
    from appuifw import InfoPopup
except ImportError:
    pass


try: enumerate
except NameError:
    def enumerate(seq):
        for (index, item) in zip(xrange(len(seq)), seq):
            yield (index, item)

def run_menu_item(menu):
    def wrapper():
        item = menu.popup()
        if item: item.target()
    return wrapper


from keycapture import KeyCapturer

def menu_key_handler(win=None):
    pass

def exit_key_handler(win=None):
    pass

def power_key_handler(win=None):
    pass

def keyhook(keycode):
    k = keycode
    win = screen.windows[0]
    if k == 63554:
        try: menu_key_handler(win)
        except: pass
    elif k == 63555:
        try: exit_key_handler(win)
        except: pass
    elif k == 63556:
        try: power_key_handler()
        except NameError: pass
    keycapturer.stop()

keycapturer = KeyCapturer(keyhook)
keycapturer.keys = 63554, 63555, 63556
keycapturer.forwarding = 0
break_keycapturer = e32.Ao_timer()


ETextInputMode = 1
ENumericInputMode = 2

def pop(dict_, key, *default):
    if default:
        value = dict_.get(key, *default)
    else:
        value = dict_[key]
    try:
        del dict_[key]
    except KeyError:
        pass
    return value


import __builtin__
__builtin__.pop = pop
del __builtin__
class Event(object):
    __module__ = __name__

    def __init__(self):
        self.lock = e32.Ao_lock()
        self.clear()



    def wait(self):
        if (not self.isSet()):
            self.lock.wait()



    def set(self):
        self.lock.signal()
        self.signaled = True



    def clear(self):
        self.signaled = False



    def isSet(self):
        return self.signaled



    def __repr__(self):
        return ('<%s; set=%s>' % (object.__repr__(self)[1:-1],
         self.isSet()))



class MenuItem(object):
    __module__ = __name__

    def __init__(self, title, **kwargs):
        self.title = title
        self.hidden = False
        self.__dict__.update(kwargs)



    def fw_item(self):
        try:
            item = tuple(self.submenu.fw_menu())
        except AttributeError:
            try:
                item = self.target
            except AttributeError:
                item = lambda :None

        return (unicode(self.title), item)



    def copy(self):
        item = MenuItem(**self.__dict__)
        try:
            item.submenu = item.submenu.copy()
        except AttributeError:
            pass
        return item



    def __repr__(self):
        return ('<%s; title=%s>' % (object.__repr__(self)[1:-1],
         repr(self.title)))



class Menu(list):
    __module__ = __name__

    def __init__(self, title = u'', items = []):
        if title:
            self.title = title
        else:
            self.title = u''
        list.__init__(self, items)



    def fw_menu(self):
        return [x.fw_item() for x in self if (not x.hidden)]



    def copy(self):
        return Menu(self.title, [ x.copy() for x in self ])



    def find(self, **kwargs):
        items = []
        for item in self:
            for (name, val,) in kwargs.items():
                if ((not hasattr(item, name)) or (getattr(item, name) != val)):
                    break
            else:
                items.append(item)


        return tuple(items)



    def __repr__(self):
        return ('%s(%s, %s)' % (self.__class__.__name__,
         repr(self.title),
         list.__repr__(self)))



    def __defcompare(a, b):
        return -(unicode(a.title).lower() < unicode(b.title).lower())



    def sort(self, compare = _Menu__defcompare):
        list.sort(self, compare)



    def popup(self, full_screen = False, search_field = False, description=False, left_softkey_label=None, right_softkey_label=None):
        if search_field:
            full_screen = True
        if full_screen:
            win = screen.focused_window()
            if win:
                wintitle = win.title
        menu = self
        try:
            while True:
                items = [x for x in menu if (not x.hidden)]
                if description and menu and len(screen.windows) > 4:
                    titles = [(unicode(x.title), (getattr(screen.windows[n + 1], description, '<virtual_memory>') or '<virtual_memory>').decode('utf8')) for n, x in enumerate(items)]
                else:
                    titles = [unicode(x.title) for x in items]
                if full_screen:
                    if win:
                        win.title = menu.title
                    i = selection_list(titles, search_field)
                elif menu:
                    i = popup_menu(titles, unicode(menu.title), left_softkey_label=left_softkey_label, right_softkey_label=right_softkey_label)
                else:
                    i = None
                if ((i is None) or (i < 0)):
                    item = None
                    break
                item = items[i]
                try:
                    menu = item.submenu
                except AttributeError:
                    break


        finally:
            if (full_screen and win):
                win.title = wintitle

        return item



    def multichoice(self, style = 'checkbox', search_field = False):
        items = [ x for x in self if (not x.hidden) ]
        titles = [ unicode(x.title) for x in items ]
        win = screen.focused_window()
        if win:
            wintitle = win.title
            win.title = self.title
        try:
            ret = multi_selection_list(titles, style, search_field)
            return tuple([ items[x] for x in ret ])

        finally:
            if win:
                win.title = wintitle




sizNormal = 'normal'
sizLarge = 'large'
sizFull = 'full'
oriAutomatic = 'automatic'
oriPortrait = 'portrait'
oriLandscape = 'landscape'
_umOrientation = 1
_umSize = 2
_umBody = 4
_umTitle = 8
_umMenu = 16
_umExit = 32
_umAll = 63
class Screen(object):
    __module__ = __name__

    def __init__(self):
        self.windows = []
        self._Screen__control_key_timer = None
        self._Screen__control_key_last = None
        self._Screen__blank_win = None
        self.rootwin = None



    def find_windows(self, *classes):
        if (not classes):
            classes = (Window,)
        windows = []
        for win in self.windows:
            for klass in classes:
                if isinstance(win, klass):
                    windows.append(win)
                    break


        return windows



    def close_windows(self, *classes):
        for win in [ x for x in self.find_windows(*classes) if (x != self.rootwin) ]:
            if (not win.close()):
                return False

        return (not [ x for x in self.find_windows(*classes) if (x != self.rootwin) ])



    def focused_window(self):
        if self.windows:
            win = self.windows[0]
            while win._Window__overlapped:
                win = win._Window__overlapped

            return win



    def redraw(self):
        self._Screen__update_fw()
        e32.ao_yield()



    def open_blank_window(self, title = None, color = None):
        if (title is None):
            title = _('Please wait...')
        if (self._Screen__blank_win and self._Screen__blank_win.is_opened()):
            self._Screen__blank_win.title = title
            self._Screen__blank_win.focus = True
        else:
            if (color is None):
                self._Screen__blank_win = BlankWindow(title=title)
            else:
                self._Screen__blank_win = BlankWindow(title=title, color=color)
            self._Screen__blank_win.open()
        return self._Screen__blank_win



    def __window_open(self, win):
        ofwin = self.focused_window()
        self.windows.append(win)
        if isinstance(win, RootWindow):
            self.rootwin = win
        nfwin = self.focused_window()
        if (ofwin and (ofwin != nfwin)):
            ofwin.focus_changed(False)
        if (nfwin == win):
            nfwin.focus_changed(True)
            reset_inactivity()
        self._Screen__update_fw()



    def __window_get_focus(self, win):
        return (win == self.focused_window())



    def __window_set_focus(self, win, focus):
        fwin = self.focused_window()
        if focus:
            while True:
                owners = [ x for x in self.windows if (x.overlapped == win) ]
                if (not owners):
                    break
                win = owners[0]

            while True:
                self.windows.remove(win)
                self.windows.insert(0, win)
                if (not win._Window__overlapped):
                    break
                win = win._Window__overlapped

        else:
            while True:
                self.windows.remove(win)
                self.windows.append(win)
                if (not win._Window__overlapped):
                    break
                win = win._Window__overlapped

        win = self.focused_window()
        if (fwin != win):
            fwin.focus_changed(False)
            win.focus_changed(True)
            reset_inactivity()
            fwin.reset_control_key()
            self._Screen__update_fw()



    def __window_close(self, win):
        fwin = self.focused_window()
        self.windows.remove(win)
        for w in self.windows:
            if (w._Window__overlapped == win):
                w._Window__overlapped = None

        if (win == self.rootwin):
            self.rootwin = None
        if (fwin == win):
            win.focus_changed(False)
        fwin = self.focused_window()
        if fwin:
            fwin.focus_changed(True)
        win.reset_control_key()
        self._Screen__update_fw()



    def __update_fw(self, mask = _umAll):
        win = self.focused_window()
        if win:
            if (mask & _umOrientation):
                app.orientation = win.orientation
            if (mask & _umSize):
                app.screen = win.size
            if (mask & _umBody):
                app.body = win.body
            if (mask & _umTitle):
                app.title = unicode(win.title)
            if (mask & _umMenu):
                if (win.menu is not None):
                    
                    app.menu = win.menu.fw_menu()
                else:
                    app.menu = []
            if (mask & _umExit):
                try:
                    assert win.typename == 'Python'
                except (AttributeError, AssertionError):
                    app.exit_key_handler = win.close
                else:
                    app.exit_key_handler = win.popup_file_menu



    def __ekeyyes_handler(self):
        keycapturer.start()
        break_keycapturer.cancel()
        break_keycapturer.after(1, keycapturer.stop)
        win = self.focused_window()
        in_time = (self._Screen__control_key_timer is not None)
        if in_time:
            self._Screen__control_key_timer.cancel()
        self._Screen__control_key_timer = e32.Ao_timer()
        self._Screen__control_key_timer.after(1.2, win.reset_control_key)
        if ((win is not None) and hasattr(win._Window__body, 'focus')):
            win._Window__body.focus = False
        if (in_time and (self._Screen__control_key_last is None)):
            win.reset_control_key()
            schedule(self._Screen__selector)
            return 
        if (win is not None):

            def make_key_handler(key):
                return lambda :self._Screen__control_key_handler(key)



            for key in win._Window__control_keys:
                win._Window__body.bind(key, make_key_handler(key))

        self._Screen__control_key_last = None



    def __control_key_reset(self, win):
        if (self._Screen__control_key_timer is not None):
            self._Screen__control_key_timer.cancel()
            self._Screen__control_key_timer = None
            if (win is not None):
                if hasattr(win._Window__body, 'focus'):
                    win._Window__body.focus = True
                for key in win._Window__control_keys:
                    win._Window__body.bind(key, lambda :None
)

                win._Window__set_keys(win._Window__keys)
        self._Screen__control_key_last = None



    def __control_key_handler(self, key):
        if (self._Screen__control_key_timer is None):
            return 
        win = self.focused_window()
        self._Screen__control_key_timer.cancel()
        if (self._Screen__control_key_last not in (None,
         key)):
            win.reset_control_key()
            if (key in win._Window__keys):
                win.key_press(key)
            return 
        if win.control_key_press(key):

            def restore(self, body):
                self._Screen__update_fw(_umBody)
                if ((self._Screen__control_key_timer is not None) and hasattr(body, 'focus')):
                    body.focus = False


            app.body = Canvas()
            schedule(lambda self = self, body = win._Window__body:restore(self, body)
)
        if (self._Screen__control_key_timer is not None):
            self._Screen__control_key_timer = e32.Ao_timer()
            self._Screen__control_key_timer.after(1.0, win.reset_control_key)
        self._Screen__control_key_last = key



    def __selector(self):
        win = self.focused_window()
        while (not win.selector):
            owners = [x for x in self.windows if (x.overlapped == win)]
            if (not owners):
                title = None
                break
            win = owners[0]
        else:
            title = win._Window__title

        menu = Menu(title)
        for win in [x for x in self.windows if ((x != win) and x.selector)]:
            menu.append(MenuItem(win._Window__title, window=win))

        item = menu.popup(description='path')
        if item:
            item.window.focus = True



    def get_windows_menu(self):
        menu = Menu()

        def make_activator(win):

            def activate():
                win.focus = True


            return activate


        for win in self.windows:
            if win.selector:
                menu.append(MenuItem(win._Window__title, window=win, target=make_activator(win)))

        return menu



    def __len__(self):
        return len(self.windows)



    def __getitem__(self, i):
        return self.windows[i]



class Window(object):
    __module__ = __name__

    def __init__(self, **kwargs):
        self._Window__status = 0
        self._Window__title = pop(kwargs, 'title', self.__class__.__name__)
        self._Window__body = None
        self._Window__menu = pop(kwargs, 'menu', Menu())
        if ('size' in kwargs):
            self._Window__size = pop(kwargs, 'size')
        else:
            try:
                self._Window__size = screen.rootwin.size
            except AttributeError:
                self._Window__size = sizNormal
        if ('orientation' in kwargs):
            self._Window__orientation = pop(kwargs, 'orientation')
        else:
            try:
                self._Window__orientation = screen.rootwin.orientation
            except AttributeError:
                self._Window__orientation = oriAutomatic
        self.selector = pop(kwargs, 'selector', True)
        self._Window__overlapped = None
        self._Window__keys = []
        self._Window__control_keys = []
        self._Window__modal_event = None
        self.modal_result = None
        if kwargs:
            raise TypeError(('Window.__init__() got an unexpected keyword argument(s): %s' % ', '.join([ repr(x) for x in kwargs.keys() ])))



    def open(self, focus = True):
        if (self._Window__status == 0):
            screen._Screen__window_open(self)
            if focus:
                screen._Screen__window_set_focus(self, True)
            self._Window__status = 2



    def is_opened(self):
        return (self._Window__status == 2)



    def is_closed(self):
        return (self._Window__status == 1)



    def can_close(self):
        return ((not self._Window__overlapped) or (not self._Window__overlapped.is_opened()))



    def close(self):
        if (self.is_opened() and self.can_close()):
            self._Window__status = 1
            screen._Screen__window_close(self)
            if (self._Window__body is not None):
                for key in self._Window__keys:
                    self._Window__body.bind(key, None)

                for key in self._Window__control_keys:
                    self._Window__body.bind(key, None)

                self._Window__body = None
            self._Window__menu = None
            if self._Window__modal_event:
                self._Window__modal_event.set()
                e32.ao_yield()
            return True
        return False



    def modal(self, owner = None):
        if (not self.is_closed()):
            if (not self.is_opened()):
                self.open()
            self._Window__modal_event = Event()
            self.focus = True
            if (owner is not None):
                state = (owner.overlapped,
                 self.selector)
                owner.overlapped = self
                self.selector = False
            self._Window__modal_event.wait()
            if owner:
                (owner.overlapped, self.selector,) = state
            self._Window__modal_event = None
            return self.modal_result



    def key_press(self, key):
        pass


    def control_key_press(self, key):
        return False



    def focus_changed(self, focus):
        pass


    def reset_control_key(self):
        screen._Screen__control_key_reset(self)



    def __set_title(self, title):
        self._Window__title = title
        self._Window__update_fw(_umTitle)



    def __set_body(self, body):
        self._Window__body = body
        self._Window__update_fw(_umBody)
        if ((not self.is_closed()) and hasattr(body, 'bind')):
            body.bind(EKeyYes, screen._Screen__ekeyyes_handler)
            body.bind(EKeyLeftCtrl, screen._Screen__ekeyyes_handler)

            def make_key_handler(key):
                return lambda :self.key_press(key)



            for key in self._Window__keys:
                body.bind(key, make_key_handler(key))




    def __set_menu(self, menu):
        self._Window__menu = menu
        self._Window__update_fw(_umMenu)



    def update_menu(self):
        self._Window__update_fw(_umMenu)



    def __set_size(self, size):
        self._Window__size = size
        self._Window__update_fw(_umSize)



    def __set_orientation(self, orientation):
        self._Window__orientation = orientation
        self._Window__update_fw(_umOrientation)



    def __set_keys(self, keys):
        keys = dict([ (x,
         None) for x in keys ]).keys()
        try:
            keys.remove(EKeyYes)
        except ValueError:
            pass
        try:
            keys.remove(EKeyLeftCtrl)
        except ValueError:
            pass
        if (self._Window__body is not None):
            for key in self._Window__keys:
                self._Window__body.bind(key, lambda :None
)

        self._Window__keys = tuple(keys)
        if (self._Window__body is not None):

            def make_key_handler(key):
                return lambda :self.key_press(key)



            for key in keys:
                self._Window__body.bind(key, make_key_handler(key))




    def __set_control_keys(self, control_keys):
        keys = dict([ (x,
         None) for x in control_keys ]).keys()
        try:
            keys.remove(EKeyYes)
        except ValueError:
            pass
        try:
            keys.remove(EKeyLeftCtrl)
        except ValueError:
            pass
        self._Window__control_keys = tuple(keys)



    def __update_fw(self, mask = _umAll):
        if self.focus:
            screen._Screen__update_fw(mask)



    def __get_focus(self):
        if self.is_opened():
            return screen._Screen__window_get_focus(self)
        return False



    def __set_focus(self, focus):
        if self.is_opened():
            screen._Screen__window_set_focus(self, focus)



    def __set_overlapped(self, win):
        self._Window__overlapped = win
        self._Window__update_fw()



    def __repr__(self):
        return ('<%s; title=%s>' % (object.__repr__(self)[1:-1],
         repr(self.title)))


    title = property(lambda self:self._Window__title
, _Window__set_title)
    body = property(lambda self:self._Window__body
, _Window__set_body)
    menu = property(lambda self:self._Window__menu
, _Window__set_menu)
    size = property(lambda self:self._Window__size
, _Window__set_size)
    orientation = property(lambda self:self._Window__orientation
, _Window__set_orientation)
    focus = property(_Window__get_focus, _Window__set_focus)
    keys = property(lambda self:self._Window__keys
, _Window__set_keys)
    control_keys = property(lambda self:self._Window__control_keys
, _Window__set_control_keys)
    overlapped = property(lambda self:self._Window__overlapped
, _Window__set_overlapped)

class RootWindow(Window):
    __module__ = __name__

    def __init__(self, **kwargs):
        self.color = pop(kwargs, 'color', 8947848)
        kwargs.setdefault('title', app.title)
        kwargs.setdefault('selector', False)
        Window.__init__(self, **kwargs)
        self.body = Canvas(redraw_callback=self.redraw_callback, event_callback=self.event_callback)



    def redraw_callback(self, rect):
        self.body.clear(self.color)



    def event_callback(self, event):
        pass


    def close(self):
        if self.is_opened():
            if (not screen.close_windows()):
                return False
            return Window.close(self)
        return False



class BlankWindow(Window):
    __module__ = __name__

    def __init__(self, **kwargs):
        self.color = pop(kwargs, 'color', 8947848)
        kwargs.setdefault('selector', False)
        Window.__init__(self, **kwargs)
        self.body = Canvas(redraw_callback=self.redraw_callback)



    def redraw_callback(self, rect):
        self.body.clear(self.color)



    def focus_changed(self, focus):
        Window.focus_changed(self, focus)
        if (not focus):
            self.close()



class WindowTab(object):
    __module__ = __name__

    def __init__(self, **kwargs):
        self._WindowTab__title = pop(kwargs, 'title', self.__class__.__name__)
        self._WindowTab__menu = pop(kwargs, 'menu', Menu())
        self._WindowTab__body = pop(kwargs, 'body', None)
        self._WindowTab__keys = pop(kwargs, 'keys', ())
        self._WindowTab__control_keys = pop(kwargs, 'control_keys', ())
        self.window = None
        if kwargs:
            raise TypeError(('WindowTab.__init__() got an unexpected keyword argument(s): %s' % ', '.join([ repr(x) for x in kwargs.keys() ])))



    def attach(self, window):
        self.window = window



    def __set_window_property(self, prop, value):
        if (self.window is not None):
            if (self.window.current_tab == self):
                setattr(self.window, prop, value)



    def __set_title(self, title):
        self._WindowTab__title = title
        self.window.tabs = self.window.tabs



    def __set_body(self, body):
        self._WindowTab__body = body
        self._WindowTab__set_window_property('body', body)



    def __set_menu(self, menu):
        self._WindowTab__menu = menu
        self._WindowTab__set_window_property('menu', menu)



    def __set_keys(self, keys):
        self._WindowTab__keys = keys
        self._WindowTab__set_window_property('keys', keys)



    def __set_control_keys(self, control_keys):
        self._WindowTab__control_keys = control_keys
        self._WindowTab__set_window_property('control_keys', control_keys)


    title = property(lambda self:self._WindowTab__title
, _WindowTab__set_title)
    body = property(lambda self:self._WindowTab__body
, _WindowTab__set_body)
    menu = property(lambda self:self._WindowTab__menu
, _WindowTab__set_menu)
    keys = property(lambda self:self._WindowTab__keys
, _WindowTab__set_keys)
    control_keys = property(lambda self:self._WindowTab__control_keys
, _WindowTab__set_control_keys)

class TabbedWindow(Window):
    __module__ = __name__

    def __init__(self, **kwargs):
        tabs = pop(kwargs, 'tabs', ())
        Window.__init__(self, **kwargs)
        self._TabbedWindow__tabs = ()
        self._TabbedWindow__current_tab = -1
        if tabs:
            self._TabbedWindow__set_tabs(tabs)



    def focus_changed(self, focus):
        Window.focus_changed(self, focus)
        if (focus and self.tabs):
            app.set_tabs([ unicode(x.title) for x in self.tabs ], self._TabbedWindow__tab_changed)
            app.activate_tab(self._TabbedWindow__current_tab)
        else:
            app.set_tabs([], None)



    def tab_changed(self, prev):
        pass


    def __update_win(self):
        if (self._TabbedWindow__current_tab >= 0):
            tab = self._TabbedWindow__tabs[self._TabbedWindow__current_tab]
            self._Window__keys = tab.keys
            self._Window__control_keys = tab.control_keys
            self._Window__body = None
            self.body = tab.body
            self.menu = tab.menu
        else:
            self.keys = ()
            self.control_keys = ()
            self.body = None
            self.menu = Menu()



    def __tab_changed(self, n):
        prev = self.current_tab
        self._TabbedWindow__current_tab = n
        self._TabbedWindow__update_win()
        e32.ao_yield()
        self.tab_changed(prev)



    def __set_tabs(self, tabs):
        tabs = tuple(tabs)
        different = (self._TabbedWindow__tabs != tabs)
        if different:
            try:
                prev = self.current_tab
            except IndexError:
                prev = None
            self._TabbedWindow__tabs = tabs
            if (len(tabs) <= self._TabbedWindow__current_tab):
                self._TabbedWindow__current_tab = (len(tabs) - 1)
            elif (self._TabbedWindow__current_tab < 0):
                self._TabbedWindow__current_tab = 0
            for tab in tabs:
                tab.attach(self)

        if self.focus:
            if tabs:
                app.set_tabs([ unicode(x.title) for x in tabs ], self._TabbedWindow__tab_changed)
                app.activate_tab(self._TabbedWindow__current_tab)
            else:
                app.set_tabs([], None)
        self._TabbedWindow__update_win()
        if different:
            self.tab_changed(prev)



    def __set_current_tab(self, n):
        if (n >= len(self.tabs)):
            n = (len(self.tabs) - 1)
        elif (n < 0):
            n = 0
        self._TabbedWindow__tab_changed(n)
        if self.focus:
            app.activate_tab(n)


    current_tab = property(lambda self:self._TabbedWindow__tabs[self._TabbedWindow__current_tab]
)
    tabs = property(lambda self:self._TabbedWindow__tabs
, _TabbedWindow__set_tabs)
    current_tab_index = property(lambda self:self._TabbedWindow__current_tab
, _TabbedWindow__set_current_tab)

class FilteredListboxModifier(object):
    __module__ = __name__

    def __init__(self, nomatch_item):
        self.filter_menu_item = MenuItem(_('Edit filter...'), target=self._FilteredListboxModifier__edit)
        self._FilteredListboxModifier__menu = Menu()
        self._FilteredListboxModifier__menu.append(MenuItem(_('Show all'), target=self._FilteredListboxModifier__showall))
        self._FilteredListboxModifier__menu.append(MenuItem(_('Edit filter...'), target=self._FilteredListboxModifier__edit))
        self._FilteredListboxModifier__nomatch = nomatch_item
        self.keys += (EKeyHash,)
        self._FilteredListboxModifier__list = []
        self._FilteredListboxModifier__filter = None
        self._FilteredListboxModifier__callback = None
        self._FilteredListboxModifier__title = self.title



    def key_press(self, key):
        if (key == EKeyHash):
            if (self._FilteredListboxModifier__filter is not None):
                item = self._FilteredListboxModifier__menu.popup()
                if (item is not None):
                    item.target()
            else:
                self._FilteredListboxModifier__edit()



    def current(self):
        flst = self.filter_list(self._FilteredListboxModifier__list)
        try:
            return self._FilteredListboxModifier__list.index(flst[self.body.current()])
        except ValueError:
            return -1



    def filter_list(self, lst):
        if (self._FilteredListboxModifier__filter is not None):
            lst = [ item for item in lst if self.filter_item(item, self._FilteredListboxModifier__filter) ]
            if (not lst):
                lst.append(self._FilteredListboxModifier__nomatch)
        return lst



    def filter_item(self, item, filter):
        if isinstance(item, tuple):
            item = item[0]
        return (item.lower().find(filter) >= 0)



    def set_listbox(self, lst, callback):
        self._FilteredListboxModifier__list = list(lst)
        flst = self.filter_list(self._FilteredListboxModifier__list)
        self._FilteredListboxModifier__callback = callback
        self.body = Listbox(flst, self._FilteredListboxModifier__select)



    def set_list(self, lst, act = 0):
        if (lst is not None):
            self._FilteredListboxModifier__list = list(lst)
        flst = self.filter_list(self._FilteredListboxModifier__list)
        try:
            act = flst.index(self._FilteredListboxModifier__list[act])
        except ValueError:
            if (act >= len(flst)):
                act = (len(flst) - 1)
        except IndexError:
            act = 0
        self.body.set_list(flst, act)



    def set_filter(self, filter):
        if (filter is None):
            if (self._FilteredListboxModifier__filter is None):
                return 
            act = self.current()
            self._FilteredListboxModifier__filter = None
            self.filter_menu_item.title = _('Edit filter...')
            self.filter_menu_item.target = self._FilteredListboxModifier__edit
            try:
                del self.filter_menu_item.submenu
            except AttributeError:
                pass
        else:
            act = max(self.current(), 0)
            self._FilteredListboxModifier__filter = filter.lower()
            self.filter_menu_item.title = _('Filter')
            self.filter_menu_item.submenu = self._FilteredListboxModifier__menu
            try:
                del self.filter_menu_item.target
            except AttributeError:
                pass
        self.set_list(None, act)
        self._FilteredListboxModifier__set_title(self._FilteredListboxModifier__title)
        self.update_menu()



    def __showall(self):
        self.set_filter(None)



    def __edit(self):
        filter = query(_('Filter:'), 'text', self._FilteredListboxModifier__filter)
        if (filter is not None):
            self.set_filter(filter)



    def __select(self):
        if (self.current() >= 0):
            self._FilteredListboxModifier__callback()



    def __set_title(self, title):
        self._FilteredListboxModifier__title = title
        if (self._FilteredListboxModifier__filter is not None):
            self.title = ('%s | %s' % (self._FilteredListboxModifier__filter,
             title))
        else:
            self.title = title


    filter_title = property(lambda self:self._FilteredListboxModifier__title
, _FilteredListboxModifier__set_title)

(fbmOpen, fbmSave,) = range(2)
class FileBrowserWindow(Window,
 FilteredListboxModifier):
    __module__ = __name__
    links = []
    aliases = []
    icons_path = ''
    settings_path = ''
    max_recents = 100

    def __init__(self, **kwargs):
        self.mode = pop(kwargs, 'mode', fbmOpen)
        self.filter_ext = pop(kwargs, 'filter_ext', ())
        (self.path, self.name,) = os.path.split(pop(kwargs, 'path', ''))
        kwargs.setdefault('title', _('File browser'))
        Window.__init__(self, **kwargs)
        if (not os.path.exists(self.icons_path)):
            raise IOError('Missing file browser icons file')
        icons_type = os.path.splitext(self.icons_path)[-1].lower()
        icons_list = [('loading',
          8,
          16390),
         ('info',
          6,
          16390),
         ('drive',
          2,
          16384),
         ('folder',
          0,
          16388),
         ('empty',
          12,
          16386),
         ('.txt',
          4,
          16394),
         ('.py',
          10,
          16392)]
        self.icons = {}
        path = self.icons_path.decode('utf8')
        for (name, mbm, mif,) in icons_list:
            if (icons_type == '.mif'):
                self.icons[name] = Icon(path, mif, (mif + 1))
            else:
                self.icons[name] = Icon(path, mbm, (mbm + 1))

        FilteredListboxModifier.__init__(self, (_('(no match)'), u'', self.icons['info']))
        self.gtitle = self.filter_title
        self.settings = SettingsGroup(filename=self.settings_path)
        self.settings.append('main', SettingsGroup())
        self.settings.main.append('recents', Setting('Recents', []))
        self.settings.main.append('aliases', Setting('Aliases', []))
        self.settings.try_to_load()
        self.filter_nomatch_item = (_('(no match)'), u'', self.icons['info'])
        self.set_listbox([(_('(empty)'), u'',
          self.icons['info'])], self.select_click)
        self.keys += (EKeyLeftArrow,
         EKeyRightArrow,
         EKey0,
         EKeyHash,
         EKeyBackspace)
        self.control_keys += (EKeyUpArrow,
         EKeyDownArrow)
        self.busy = False
        (self.DRIVE, self.DIR, self.FILE, self.INFO,) = range(4)
        self.update(self.name)



    def add_link(cls, link, title = None):
        if (link and ((link[1:] != ':\\') and os.path.exists(link))):
            if (link.lower() in [ x[0].lower() for x in cls.links ]):
                return False
            if (title is None):
                (path, name,) = os.path.split(link)
                title = (_('%s in %s') % (name.decode('utf8'),
                 path.decode('utf8')))
            cls.links.append((link,
             title))
            return True
        return False


    add_link = classmethod(add_link)

    def add_alias(cls, alias):
        key, link = alias
        if os.path.exists(link):
            cls.aliases.append((key,
             link))
            self.settings.save()
            return True
        return False


    add_aliases = classmethod(add_aliases)

    def add_recent(self, filename):
        recents = self.settings.main.recents
        for name in recents:
            if (name.lower() == filename.lower()):
                recents.remove(name)
                break
        else:
            if (len(recents) == self.max_recents):
                recents.pop()

        recents.insert(0, filename)
        self.settings.save()



    def get_file_icon(self, name):
        ext = os.path.splitext(name)[1].lower()
        try:
            return self.icons[ext]
        except KeyError:
            return self.icons['empty']



    def update(self, mark = ''):
        (app.menu_key_text, app.exit_key_text,) = (_('Options'),
         _('Exit'))
        self.set_list([(_('Loading...'), u'...  ' + '.   .   ' * 10,
          self.icons['loading'])])
        e32.ao_yield()
        if (self.path == ''):
            self.filter_title = self.gtitle
            self.lstall = [ (self.DRIVE,
             self.icons['drive'],
             x,
             x.encode('utf8')) for x in e32.drive_list() ]

            def format(link):
                if os.path.isfile(link[0]):
                    return (self.FILE,
                     self.get_file_icon(link[0]),
                     link[1],
                     link[0])
                else:
                    return (self.DIR,
                     self.icons['folder'],
                     link[1],
                     link[0])


            self.lstall += map(format, self.links)
            if os.path.exists('C:\\System\\Mail\\00001001_S'):
                self.lstall.append((self.DIR,
                 self.icons['folder'],
                 _('Messages'),
                 ':messages'))
        elif (self.path == ':recents'):
            self.filter_title = _('Recent files')

            def format(filename):
                (path, name,) = os.path.split(filename)
                title = (_('%s in %s') % (name.decode('utf8'),
                 path.decode('utf8')))
                return (self.FILE,
                 self.get_file_icon(filename),
                 title,
                 filename)


            recents = self.settings.main.recents
            recentslen = len(recents)
            for filename in list(recents):
                if (not os.path.exists(filename)):
                    recents.remove(filename)

            if (len(recents) != recentslen):
                self.settings.save()
            self.lstall = map(format, recents)
        elif (self.path == ':messages'):
            self.filter_title = _('Messages')

            def scandir(path):
                lst = []
                for name in os.listdir(path):
                    fullpath = os.path.join(path, name)
                    if os.path.isdir(fullpath):
                        lst.extend(scandir(fullpath))
                    elif (os.path.isfile(fullpath) and path.endswith('_F')):
                        lst.append((self.FILE,
                         self.get_file_icon(fullpath),
                         name.decode('utf8'),
                         fullpath))

                return lst


            self.lstall = scandir('C:\\System\\Mail\\00001001_S')
        else:
            if (self.path[-2:] == ':\\'):
                self.filter_title = self.path[:2].decode('utf8')
            else:
                self.filter_title = os.path.split(self.path)[1].decode('utf8')
            e32.ao_yield()

            def format(name):
                if os.path.isfile(os.path.join(self.path, name)):
                    return (self.FILE,
                     self.get_file_icon(name),
                     name.decode('utf8'),
                     name)
                else:
                    return (self.DIR,
                     self.icons['folder'],
                     name.decode('utf8'),
                     name)


            try:
                ldir = os.listdir(self.path)
            except OSError:
                note(_('Cannot list directory'), 'error')
                self.parent_click()
                return 
            else:
                self.lstall = map(format, ldir)

        def compare(a, b):
            if (a[0] > b[0]):
                return 0
            if (a[0] < b[0]):
                return -1
            return -(unicode(a[2]).lower() < unicode(b[2]).lower())


        self.lstall.sort(compare)
        if (self.path == ''):
            self.lstall.insert(0, (self.DIR,
             self.icons['folder'],
             _('Recent files'),
             ':recents'))
        active = 0
        if (mark != ''):
            try:
                active = [ x[3].lower() for x in self.lstall ].index(mark.lower())
            except ValueError:
                pass
        self.set_lstall(active)
        self.make_menu()



    def make_menu(self):
        menu = Menu()
        if ((self.mode == fbmSave) and ((self.path != '') and (not self.path.startswith(':')))):
            menu.append(MenuItem(_('Save here...'), target=self.save_click))
        menu.append(MenuItem(_('Open'), target=self.select_click))
        if self.path.startswith(':'):
            menu.append(MenuItem(_('Drives'), target=self.drives_click))
            if (self.path == ':recents'):
                menu.append(MenuItem(_('Delete'), target=self.delete_click))
        elif (self.path != ''):
            menu.append(MenuItem(_('Parent'), target=self.parent_click))
            menu.append(MenuItem(_('Drives'), target=self.drives_click))
            menu.append(MenuItem(_('Rename'), target=self.rename_click))
            menu.append(MenuItem(_('Delete'), target=self.delete_click))
            menu.append(MenuItem(_('Create folder...'), target=self.mkdir_click))
        menu.append(self.filter_menu_item)
        menu.append(MenuItem(_('Add alias'), target=self.__class__.add_alias))
        menu.append(MenuItem(_('Exit'), target=self.close))
        self.menu = menu



    def set_lstall(self, active = None):
        if (active is None):
            active = self.current()
            if (active < 0):
                active = 0
        lst = self.lstall
        if self.filter_ext:
            lst = [ x for x in lst if ((x[0] != self.FILE) or (os.path.splitext(x[3])[-1].lower() in (self.filter_ext,))) ]
        try:
            active = lst.index(self.lstall[active])
        except (ValueError,
         IndexError):
            active = 0
        if (not lst):
            lst.append((self.INFO,
             self.icons['info'],
             _('(empty)'),
             None))
        self.set_list([(
          (
            len(y) >= 3 and ' '.join(y[:-2])
          ) or x[2],
          (
            len(y) >= 3 and ' '.join(y[-2:])
          ) or u'',
         x[1]) for x in lst for y in (x[2].split(' '),)], active)
        self.lst = lst



    def select_click(self):
        if self.busy:
            return 
        self.busy = True
        try:
            i = self.current()
            if (i < 0):
                return 
            item = self.lst[i]
            if (item[0] == self.DRIVE):
                self.path = ('%s\\' % item[3])
                self.set_filter(None)
                self.update()
            elif (item[0] == self.DIR):
                self.path = os.path.join(self.path, item[3])
                self.set_filter(None)
                self.update()
            elif (item[0] == self.FILE):
                if (self.mode == fbmOpen):
                    self.path = os.path.join(self.path, item[3])
                    self.modal_result = self.path
                    self.add_recent(self.path)
                    self.close()
                else:
                    self.save_click((os.path.splitext(item[3])[0] + os.path.splitext(self.name)[1]))

        finally:
            self.busy = False




    def key_press(self, key):
        if (key == EKeyLeftArrow):
            self.parent_click()
        elif (key == EKeyRightArrow):
            self.enter_click()
        elif (key == EKeyBackspace):
            self.delete_click()
        elif (key == EKey0):
            self.info_click()
        elif (key == EKeyStar):
            self.drives_click()
        else:
            FilteredListboxModifier.key_press(self, key)
            Window.key_press(self, key)



    def control_key_press(self, key):
        if (key == EKeyUpArrow):
            self.set_lstall((self.current() - 5))
        elif (key == EKeyDownArrow):
            self.set_lstall((self.current() + 5))
        else:
            return Window.control_key_press(self, key)
        return False



    def enter_click(self):
        i = self.current()
        if (i < 0):
            return 
        item = self.lst[i]
        if (item[0] == self.FILE):
            (path, name,) = os.path.split(item[3])
            if path:
                self.path = path
                self.update(name)
        else:
            self.select_click()



    def parent_click(self):
        if (self.path != ''):
            if (self.path[-2:] == ':\\'):
                mark = self.path[:2]
                self.path = ''
            else:
                (self.path, mark,) = os.path.split(self.path)
            self.set_filter(None)
            self.update(mark)



    def drives_click(self):
        if (self.path != ''):
            mark = self.path[:2]
            self.path = ''
            self.set_filter(None)
            self.update(mark)



    def save_click(self, name = None):
        if (name is None):
            name = self.name
        (name, ext,) = os.path.splitext(name)
        path = None
        while True:
            name = query((_('Name (%s):') % ext.decode('utf8')), 'text', name.decode('utf8'))
            if (name is None):
                return 
            name = name.encode('utf8')
            (name, newext,) = os.path.splitext(name)
            if newext:
                ext = newext
            path = os.path.join(self.path, (name + ext))
            if os.path.exists(path):
                if os.path.isdir(path):
                    note(_('Invalid name'), 'error')
                    continue
                elif (not query(_('Already exists. Overwrite?'), 'query')):
                    continue
            break

        self.add_recent(path)
        self.name = (name + ext)
        self.modal_result = path
        self.close()



    def delete_click(self):
        if (self.path == ':messages'):
            return 
        i = self.current()
        if (i < 0):
            return 
        item = self.lst[i]
        if (item[0] not in [self.FILE,
         self.DIR]):
            return 
        if query((_('Delete %s?') % item[2]), 'query'):
            path = os.path.join(self.path, item[3])
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    os.rmdir(path)
            except OSError:
                note(_('Cannot delete'), 'error')
            else:
                self.update()



    def rename_click(self):
        i = self.current()
        if (i < 0):
            return 
        item = self.lst[i]
        if (item[0] not in [self.FILE,
         self.DIR]):
            return 
        (name, ext,) = os.path.splitext(item[3])
        while True:
            name = query((_('Name (%s):') % ext.decode('utf8')), 'text', name.decode('utf8'))
            if (name is None):
                break
            name = name.encode('utf8')
            (name, newext,) = os.path.splitext(name)
            if newext:
                ext = newext
            src = os.path.join(self.path, item[3])
            dst = os.path.join(self.path, (name + ext))
            try:
                if (os.path.exists(dst) and (src.lower() != dst.lower())):
                    if os.path.isdir(dst):
                        note(_('Already exists as a directory'), 'error')
                        continue
                    if (not query(_('Already exists. Overwrite?'), 'query')):
                        continue
                    os.remove(dst)
                os.rename(src, dst)
                self.update((name + ext))
                break
            except OSError:
                note(_('Cannot rename'), 'error')
                break




    def mkdir_click(self):
        name = query(_('Name:'), 'text')
        if (name is not None):
            try:
                os.mkdir(os.path.join(self.path, name.encode('utf8')))
                self.update(name.encode('utf8'))
            except OSError:
                note(_('Cannot create folder'), 'error')



    def info_click(self):
        i = self.current()
        if (i < 0):
            return 
        item = self.lst[i]
        if ((item[0] not in [self.DRIVE,
         self.FILE,
         self.DIR]) or item[3].startswith(':')):
            return 
        if (item[0] == self.DRIVE):
            from sysinfo import free_drivespace
            n = free_drivespace()[item[2]]
            text = (u'%d B' % n)
            if (n > 1024):
                n /= 1024.0
                text = (u'%.1f KB' % n)
            if (n > 1024):
                n /= 1024.0
                text = (u'%.1f MB' % n)
            text = (_('Free: %s') % text)
        else:
            import time
            stat = os.stat(os.path.join(self.path, item[3]))
            if (item[0] == self.FILE):
                n = stat.st_size
                text = (u'%d B' % n)
                if (n > 1024):
                    n /= 1024.0
                    text = (u'%.1f KB' % n)
                if (n > 1024):
                    n /= 1024.0
                    text = (u'%.1f MB' % n)
                text += u'\n'
            else:
                text = u''
            text += time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(stat.st_mtime))
        try:
            infopopup.show(text)
        except NameError:
            note(text)



class Setting(object):
    __module__ = __name__

    def __init__(self, title, value):
        self.title = title
        self.value = value



    def get(self):
        return self.value



    def set(self, value):
        self.value = value



    def edit(self, owner = None):
        return False



    def __str__(self):
        return str(self.value)



    def __unicode__(self):
        return unicode(self.value)



class StringSetting(Setting):
    __module__ = __name__

    def __init__(self, title, value = u''):
        Setting.__init__(self, title, value)



    def edit(self, owner = None):
        v = query(unicode(self.title), 'text', unicode(self.value))
        if (v is not None):
            self.value = v
            return True
        return False



class IntegerSetting(Setting):
    __module__ = __name__

    def __init__(self, title, value = 0, vmin = None, vmax = None):
        if ((vmin is not None) and ((vmax is not None) and (vmin > vmax))):
            vmin = vmax
        if ((vmin is not None) and (value < vmin)):
            value = vmin
        if ((vmax is not None) and (value > vmax)):
            value = vmax
        Setting.__init__(self, title, value)
        self.vmin = vmin
        self.vmax = vmax



    def edit(self, owner = None):
        v = self.value
        while True:
            v = query(unicode(self.title), 'number', v)
            if (v is None):
                return False
            if ((self.vmin is not None) and (v < self.vmin)):
                note((_('Minimal value is %s') % self.vmin))
                continue
            if ((self.vmax is not None) and (v > self.vmax)):
                note((_('Maximal value is %s') % self.vmax))
                continue
            self.value = v
            break

        return True



class FloatSetting(IntegerSetting):
    __module__ = __name__

    def __init__(self, title, value = 0.0, vmin = None, vmax = None):
        IntegerSetting.__init__(self, title, float(value), float(vmin), float(vmax))



    def edit(self, owner = None):
        v = self.value
        while True:
            v = query(unicode(self.title), 'float', v)
            if (v is None):
                return False
            if ((self.vmin is not None) and (v < self.vmin)):
                note((_('Minimal value is %s') % ('%.2f' % self.vmin)))
                continue
            if ((self.vmax is not None) and (v > self.vmax)):
                note((_('Maximal value is %s') % ('%.2f' % self.vmax)))
                continue
            self.value = v
            break

        return True



class BoolSetting(Setting):
    __module__ = __name__

    def __init__(self, title, value = False, true = None, false = None):
        if (true is None):
            true = _('On')
        if (false is None):
            false = _('Off')
        Setting.__init__(self, title, value)
        self.true = true
        self.false = false



    def edit(self, owner = None):
        self.value = (not self.value)
        return True



    def __unicode__(self):
        if self.value:
            return unicode(self.true)
        return unicode(self.false)



class ChoiceSetting(Setting):
    __module__ = __name__

    def __init__(self, title, value = None, choices = [], **kwargs):
        Setting.__init__(self, title, value)
        self.choices = choices
        self.kwargs = kwargs



    def edit(self, owner = None):
        menu = Menu(self.title)
        for choice in self.choices:
            if (choice == self.value):
                menu.insert(0, MenuItem((u'* %s' % choice), choice=choice))
            else:
                menu.append(MenuItem(choice, choice=choice))

        item = menu.popup(**self.kwargs)
        if (item is not None):
            self.value = item.choice
            return True
        return False



class ChoiceValueSetting(Setting):
    __module__ = __name__

    def __init__(self, title, value = None, choices = [], **kwargs):
        Setting.__init__(self, title, value)
        self.choices = choices
        self.kwargs = kwargs



    def edit(self, owner = None):
        menu = Menu(self.title)
        for choice, value in self.choices:
            if value == self.value:
                menu.insert(0, MenuItem((u'* %s' % choice), value=value))
            else:
                menu.append(MenuItem(choice, value=value))

        item = menu.popup(**self.kwargs)
        if (item is not None):
            self.value = item.value
            return True
        return False



    def __str__(self):
        for (choice, value,) in self.choices:
            if (value == self.value):
                return str(choice)

        return ''



    def __unicode__(self):
        for (choice, value,) in self.choices:
            if (value == self.value):
                return unicode(choice)

        return u''



class TimeSetting(Setting):

    def __init__(self, title, value = 0.0):
        Setting.__init__(self, title, value)



    def edit(self, owner = None):
        v = query(unicode(self.title), 'time', self.value)
        if (v is not None):
            self.value = v
            return True
        return False



    def __str__(self):
        from time import strftime, localtime
        return strftime('%H:%M', localtime(self.value))



    def __unicode__(self):
        from time import strftime, localtime
        return unicode(strftime('%H:%M', localtime(self.value)))



class DateSetting(Setting):

    def __init__(self, title, value = 0.0):
        Setting.__init__(self, title, value)



    def edit(self, owner = None):
        v = query(unicode(self.title), 'date', self.value)
        if (v is not None):
            from time import timezone
            if (e32.s60_version_info >= (3,
             0)):
                timezone -= 3600
            self.value = (v - timezone)
            return True
        return False



    def __str__(self):
        from time import strftime, localtime
        return strftime('%d.%m.%Y', localtime(self.value))



    def __unicode__(self):
        from time import strftime, localtime
        return unicode(strftime('%d.%m.%Y', localtime(self.value)))



class GroupSettingWindow(Window):

    def __init__(self, **kwargs):
        self.setting = pop(kwargs, 'setting')
        Window.__init__(self, **kwargs)
        self.body = Listbox(self.get_list(), self.change_click)
        self.menu.append(MenuItem(_('Add'), target=self.add_click))
        self.menu.append(MenuItem(_('Change'), target=self.change_click))
        self.menu.append(MenuItem(_('Delete'), target=self.delete_click))
        self.menu.append(MenuItem(_('Exit'), target=self.close))
        self.keys += (EKeyBackspace,)
        self.modal_result = False



    def key_press(self, key):
        if (key == EKeyBackspace):
            self.delete_click()
            return 
        Window.key_press(self, key)



    def change_click(self):
        try:
            setting = self.setting.value.values()[self.body.current()]
        except IndexError:
            menu = Menu()
            menu.append(self.menu[0])
            item = menu.popup()
            if (item is not None):
                item.target()
            return 
        if setting.edit(self):
            self.body.set_list(self.get_list(), self.body.current())
            self.modal_result = True



    def add_click(self):
        try:
            (name, title,) = self.setting.get_new_name()
        except TypeError:
            return 
        if name:
            setting = self.setting.get_new(title)
            if (setting is not None):
                if setting.edit(self):
                    if (name in self.setting.value.keys()):
                        if (not query(_('Already exists. Replace?'), 'query')):
                            return 
                        self.setting.value.remove(name)
                    self.setting.value.append(name, setting)
                    self.setting.value.sort()
                    i = self.setting.value.keys().index(name)
                    self.body.set_list(self.get_list(), i)
                    self.modal_result = True



    def delete_click(self):
        try:
            (name, setting,) = self.setting.value.items()[self.body.current()]
        except IndexError:
            note(_('Nothing to delete'))
            return 
        title = self.setting.to_item(setting)
        if isinstance(title, tuple):
            title = title[0]
        if query((_('Delete %s?') % title), 'query'):
            self.setting.value.remove(name)
            self.body.set_list(self.get_list(), self.body.current())



    def get_list(self):
        items = [ self.setting.to_item(item) for item in self.setting.value.values() ]
        if (not items):
            items.append(self.setting.to_item(None))
        return items



class GroupSetting(Setting):

    def __init__(self, title, value = None, item_title = None):
        if (value is None):
            value = SettingsGroup(title)
        Setting.__init__(self, title, value)
        if (item_title is None):
            item_title = _('Name')
        self.item_title = item_title



    def get(self):
        return dict([ (name,
         item.get()) for (name, item,) in self.value.items() ])



    def set(self, value):
        self.value.clear()
        for (name, val,) in value.items():
            setting = self.get_new(self.item_title, val)
            if (setting is not None):
                self.value.append(name, setting)

        self.value.sort()



    def edit(self, owner = None):
        items = self.value.items()
        return GroupSettingWindow(title=self.title, setting=self).modal(owner)



    def to_item(self, setting):
        if (setting is not None):
            return unicode(setting)
        else:
            return _('(no data)')



    def get_new(self, title, value = u''):
        return StringSetting(title, value)



    def get_new_name(self):
        i = 1
        while True:
            for name in self.value.keys():
                if (name == str(i)):
                    break
            else:
                return (str(i),
                 self.item_title)

            i += 1




    def __str__(self):
        return str((_('%s item(s)') % len(self.value)))



    def __unicode__(self):
        return unicode((_('%s item(s)') % len(self.value)))



class CustomSetting(Setting):

    def __init__(self, title, value = None, edit_callback = None):
        Setting.__init__(self, title, value)
        self.edit_callback = edit_callback



    def edit(self, owner = None):
        if self.edit_callback:
            v = self.edit_callback(self.title, self.value, owner)
            if (v is not None):
                self.value = v



class SettingsGroup(object):
    __doc__ = 'Groups together a set of settings or settings groups in\n    an ordered list.\n    '

    def __init__(self, title = None, info = None, filename = None):
        if (title is None):
            title = self.__class__.__name__
        self.title = title
        if (info is None):
            info = _('(more options)')
        self.info = info
        self.filename = filename
        self.objs = {}
        self.order = []
        self.window = None



    def append(self, name, obj):
        if isinstance(obj, (SettingsGroup,
         Setting)):
            self.objs[name] = obj
            if (name in self.order):
                self.order.remove(name)
            self.order.append(name)
        else:
            raise TypeError("'obj' must be a Setting or a SettingsGroup object")



    def remove(self, name):
        self.order.remove(name)
        del self.objs[name]



    def clear(self):
        self.objs.clear()
        self.order = []



    def allkeys(self):
        keys = []
        for name in self.order:
            keys.append(name)
            obj = self.objs[name]
            if isinstance(obj, SettingsGroup):
                keys.append(obj.allkeys())

        return keys



    def items(self):
        return [ (x,
         self.objs[x]) for x in self.order ]



    def keys(self):
        return list(self.order)



    def values(self):
        return [ self.objs[x] for x in self.order ]



    def get(self):
        return self



    def set(self, value):
        raise AttributeError(('cannot set a SettingsGroup (to %s)' % repr(value)))



    def sort(self):

        def compare(a, b):
            return -(unicode(self.objs[a].title).lower() < unicode(self.objs[b].title).lower())


        self.order.sort(compare)



    def edit(self, owner = None):
        if self.window:
            self.window.focus = True
            return False
        self.window = SettingsGroupWindow(title=self.title, group=self)
        r = self.window.modal(owner)
        self.window = None
        return r



    def set_filename(self, filename):
        self.filename = filename



    def load(self):
        if (self.filename is None):
            raise ValueError('filename not set')
        import marshal
        f = file(self.filename, 'rb')
        while True:
            try:
                name = marshal.load(f)
                value = marshal.load(f)
                obj = self
                try:
                    for part in name.split('/'):
                        try:
                            part = int(part)
                        except ValueError:
                            pass
                        obj = obj[part]

                except KeyError:
                    pass
                else:
                    obj.set(value)
            except EOFError:
                break

        f.close()



    def save(self):
        if (self.filename is None):
            raise ValueError('filename not set')
        import marshal

        def save_group(f, group, path = ''):
            for (name, obj,) in group.items():
                if path:
                    curpath = ('%s/%s' % (path,
                     name))
                else:
                    curpath = name
                if isinstance(obj, SettingsGroup):
                    save_group(f, obj, curpath)
                else:
                    marshal.dump(curpath, f)
                    marshal.dump(obj.get(), f)



        f = file(self.filename, 'wb')
        save_group(f, self)
        f.close()



    def try_to_load(self):
        try:
            self.load()
        except IOError:
            pass



    def listbox_list(self):
        return [ (unicode(x.title),
         unicode(x)) for x in self.values() if x ]



    def listbox_click(self, n, owner = None):
        return self.values()[n].edit(owner)



    def __getitem__(self, name):
        return self.objs[name]



    def __getattr__(self, name):
        if (name == 'objs'):
            raise AttributeError
        try:
            obj = self.objs[name]
        except KeyError:
            raise AttributeError(('%s object has no attribute %s' % (repr(self),
             repr(name))))
        else:
            return obj.get()



    def __setattr__(self, name, value):
        try:
            obj = self.objs[name]
        except (AttributeError,
         KeyError):
            return object.__setattr__(self, name, value)
        else:
            obj.set(value)



    def __contains__(self, name):
        return (name in self.objs)



    def __len__(self):
        return len(self.objs)



    def __nonzero__(self):
        return (not (not self.objs))



    def __str__(self):
        return str(self.info)



    def __unicode__(self):
        return unicode(self.info)



class SettingsGroups(SettingsGroup):
    __doc__ = 'Same as SettingGroup but does not support settings, only\n    settings groups. The advantage is that that a TabbedWindow\n    is used to edit these groups.\n    '

    def __init__(self, *args, **kwargs):
        SettingsGroup.__init__(self, *args, **kwargs)



    def listbox_click(self, n, owner = None):
        win = SettingsTabsWindow(title=self.title, group=self, active=n)
        return win.modal(owner)



    def append(self, name, obj):
        if isinstance(obj, SettingsGroup):
            SettingsGroup.append(self, name, obj)
        else:
            raise TypeError("'obj' must be a SettingsGroup object")



class SettingsGroupWindow(Window):

    def __init__(self, **kwargs):
        self.group = pop(kwargs, 'group')
        Window.__init__(self, **kwargs)
        self.body = Listbox(self.group.listbox_list(), self.select_click)
        self.menu.append(MenuItem(_('Change'), target=self.select_click))
        self.menu.append(MenuItem(_('Exit'), target=self.exit_click))
        self.modal_result = False



    def select_click(self):
        if self.group.listbox_click(self.body.current(), self):
            self.body.set_list(self.group.listbox_list(), self.body.current())
            self.modal_result = True



    def close(self, exit = False):
        if exit:
            owners = [ win for win in screen.windows if ((win.overlapped is self) and isinstance(win, (SettingsGroupWindow,
             SettingsTabsWindow))) ]
            Window.close(self)
            for win in owners:
                win.close(exit=True)

        else:
            Window.close(self)



    def exit_click(self):
        self.close(exit=True)



class SettingsTab(WindowTab):

    def __init__(self, **kwargs):
        self.group = pop(kwargs, 'group')
        WindowTab.__init__(self, **kwargs)
        self.body = Listbox(self.group.listbox_list(), self.select_click)
        self.menu.append(MenuItem(_('Open'), target=self.select_click))
        self.menu.append(MenuItem(_('Exit'), target=self.exit_click))



    def select_click(self):
        if self.group.listbox_click(self.body.current(), self.window):
            self.body.set_list(self.group.listbox_list(), self.body.current())
            self.window.modal_result = True



    def exit_click(self):
        self.window.close(exit=True)



class SettingsTabsWindow(TabbedWindow):

    def __init__(self, **kwargs):
        self.group = pop(kwargs, 'group')
        active = pop(kwargs, 'active', 0)
        TabbedWindow.__init__(self, **kwargs)
        self.modal_result = False
        self.tabs = [ SettingsTab(title=x.title, group=x) for x in self.group.values() if x ]
        self.current_tab_index = active



    def close(self, exit = False):
        if exit:
            owners = [ win for win in screen.windows if ((win.overlapped is self) and isinstance(win, (SettingsGroupWindow,
             SettingsTabsWindow))) ]
            TabbedWindow.close(self)
            for win in owners:
                win.close(exit=True)

        else:
            TabbedWindow.close(self)



class Translator(object):

    def __init__(self, filename = None):
        self.translations = {}
        if filename:
            self.load(filename)



    def load(self, filename):
        f = open(filename)
        self.translations = {}
        for ln in f.readlines():
            ln = ln.strip()
            if ((not ln) or ln.startswith('#')):
                continue
            try:
                x = eval(('{\n%s\n}' % ln))
            except:
                raise ValueError(('%s: syntax error' % repr(ln)))
            if x:
                dst = x.values()[0]
                if dst:
                    if isinstance(dst, str):
                        dst = dst.decode('utf8')
                    elif (not isinstance(dst, type(u''))):
                        raise TypeError('translation file must contain strings only')
                    self.translations[x.keys()[0]] = dst

        f.close()



    def try_to_load(self, filename):
        try:
            self.load(filename)
        except IOError:
            pass



    def unload(self):
        self.translations = {}



    def __getitem__(self, name):
        return self.translations[name]



    def __call__(self, *strings):
        for s in strings:
            try:
                return self.translations[s]
            except KeyError:
                pass

        return unicode(strings[-1])




def available_text_fonts():
    """Returns a sorted list of text fonts."""
    bad = [u'acalc',
     u'acb',
     u'aco',
     u'acp']
    all = available_fonts()
    fonts = []
    for f in all:
        if (f == u'Series 60 ZDigi'):
            continue
        for b in bad:
            try:
                if (f.lower().startswith(b) and f[len(b)].isdigit()):
                    break
            except IndexError:
                pass
        else:
            fonts.append(f)



    def compare(a, b):
        return -(a.lower() < b.lower())


    fonts.sort(compare)
    return fonts



def schedule(target, *args, **kwargs):
    e32.ao_sleep(0, lambda :target(*args, **kwargs)
)


if (e32.s60_version_info < (2,
 8)):
    (EScreen, EApplicationWindow, EStatusPane, EMainPane, EControlPane, ESignalPane, EContextPane, ETitlePane, EBatteryPane, EUniversalIndicatorPane, ENaviPane, EFindPane, EWallpaperPane, EIndicatorPane, EAColumn, EBColumn, ECColumn, EDColumn, EStaconTop, EStaconBottom, EStatusPaneBottom, EControlPaneBottom, EControlPaneTop, EStatusPaneTop,) = range(24)
    __layout = {EApplicationWindow: ((176,
                           208),
                          (0,
                           0)),
     EScreen: ((176,
                208),
               (0,
                0)),
     EMainPane: ((176,
                  144),
                 (0,
                  44))}

    def layout(eid):
        try:
            return __layout[eid]
        except KeyError:
            return ((0,
              0),
             (0,
              0))


else:

    def layout(eid):
        return app.layout(eid)


screen = Screen()
translator = _ = Translator()
try:
    infopopup = InfoPopup()
except NameError:
    pass

