from __future__ import generators
__version__ = '11 beta'
__versionname__ = u'\n%sBlack and white%s' % (unichr(171), unichr(187))
__debugmode__ = 0
__features__ = """

$:

$$
"""


import operator
import sys
from sys import setdefaultencoding
setdefaultencoding('utf8')
del setdefaultencoding
import time
import e32, e32posix
import os
from graphics import Image
import appswitch
import ui
tokenize = decompile = None
if not hasattr(ui, 'infopopup'):
    try:
        ui.infopopup = __import__('msg')
    except ImportError:
        pass


def _gensym():
    n = 1
    while True:
        yield n
        n += 1

gensym = _gensym().next


def add_tabchar_to(string, _tabchar=' ' + unichr(187)):
    return string + _tabchar

symbols = [('()', 1), ('[]', 1), ('{}', 1), ("''", 1), ('``', 1)]
if os.path.exists('C:\\Data\\symbols'):
    try:
        symbfile = open('C:\\Data\\symbols', 'r')
        symbols = eval(symbfile.read().decode('base64'))
        symbfile.close()
    except:
        try:
            symbfile.close()
        except:
            pass

subsymbols = {
 u'()':
  [('()', 1),
  ('():', 1),
  ('(, , )', 1),
  ("('')", 2),
  ('(())', 2),
  ('([])', 2),
  ('({})', 2)],
 u'[]':
  [('[]', 1),
  ('[[]]', 2),
  ("[(u'', ((u'', ), (u'', ), (u'', ))),]", 4),
  ('[,]', 1),
  ('[][]', 1),
  ('[:]', 1),
  ("['']", 2)],
 u'{}':
  [('{}', 1),
  ('{: }', 1),
  ('{:, :, :, :}', 1),
  ("{'': , '': , '': , '': , '': ,}", 2)],
 u"''":
  [("''", 1),
  ('""', 1),
  ('``', 1),
  ("''''''", 3),
  ('""""""', 3)],
 }
statements = [
 ('____', 2),
 ('break', None),
 ('class :', 6),
 ('class ():', 6),
 ('class (object):', 6),
 ('continue', None),
 ('def ():', 4),
 ('def (self):', 4),
 ('def ____(self):', 6),
 ('def __init__(self):', 19),
 ('def __call__(self):', 19),
 ('del ', None),
 ('elif :', 5),
 ('else:', None),
 ('except:', None),
 ('finally:', None),
 ('for  in :', 4),
 ('for  in xrange(len()):', 4),
 ('from  import *', 5),
 ('from __future__ import generators', 33),
 ('global ',None),
 ('if :', 3),
 ("if __name__ == '__main__':", 26),
 ('import ', None),
 ('lambda :', 7),
 ('pass', None),
 ('print ', None),
 ('return', None),
 ('try:', None),
 ("u''", 2),
 ('while :', 6),
 ('# -*- coding: utf-8 -*-', 23),
 ('# -*- coding: CP1251 -*-', 24),
 ]

abbreviations_keys = [
 'abbrev',
 'coding',
 ]
abbreviations_values = [
 'This is <|> a simple abbreviation.',
 '# -*- coding: utf-8 -*-\n',
 ]


def passfunc():
    pass

try: enumerate
except NameError:
    def enumerate(seq):
        for (index, item) in zip(xrange(len(seq)), seq):
            yield (index, item)

def notice(note_, type='info'):
    note_ = _(note_)
    try:
        app.settings.main.notifications and ui.infopopup.show(note_)
    except (NameError, AttributeError):
        note_ and ui.note(note_, type)

def set_key_text(menu_key_text=None, exit_key_text=None):
    if menu_key_text:
        ui.app.menu_key_text = menu_key_text
    if exit_key_text:
        ui.app.exit_key_text = exit_key_text

def get_color(color, default=(200, 200, 200)):
    if isinstance(color, int): color = min(hex(color), 0xffffff)
    if ((color[:2] == u'0x') and len(color) <= 8 and not filter(lambda a: a not in u'abcdefABCDEF0123456789', color[2:])) or ((color.count(u',') == 2) and (color[0] == u'(') and (color[-1] == u')') and not filter(lambda a: not a.strip().isdigit(), color.replace(u'(', u'').replace(u')', u'').split(u','))):
        return min(eval(color), 0xffffff)
    else:
        notice('Bad color!')
        return default

def timeit(function, logging=False, clock=time.clock):
    def new(*args, **kwargs):
        start = clock()
        result = function(*args, **kwargs)
        stop = clock()
        if __debugmode__ and logging: notice('%.3f sec.' % (stop - start))
        return result
    return new


def ru(string):
    "ru(<string>) => <string>.decode('utf8')"
    return string.decode('utf')

import __builtin__
__builtin__.enumerate = enumerate
__builtin__.ru = ru
__builtin__.timeit = timeit


class _TokenColor:
    keyword = 0, 200, 0
    module = 100, 100, 100
    builtin = 200,100, 0
    number = 180, 180, 0
    string = 0, 180, 180
    name = 0, 0, 200
    operation = 240, 0, 0
    comment = 190, 0, 190
    bracket = 250, 0, 255
    percent = 0, 0, 0
    self_ = 66, 255, 0
    cls_ = 33, 210, 0
    def setColors(self, *settings):
        for token, color in zip(('keyword', 'module', 'builtin', 'number', 'string', 'name', 'operation', 'comment', 'bracket', 'percent', 'self_', 'cls_',), settings):
            try: setattr(self, token, eval(color))
            except: pass

TokenColor = _TokenColor()



class Highlighter:

    def __init__(self):
        pass



    def parse(self, programm, tokens, _tok_name=None, cur_pos=0, kws = __import__('keyword').kwlist, allmodules=tuple([n for n in sys.builtin_module_names if not n.startswith('__')] + [m[:m.rfind('.')] for m in reduce(lambda x, y: x.extend(y) or x, [e32posix.listdir(path) for path in sys.path], [])] + sys.modules.keys()), builtins = [ n for n in dir(__import__('__builtin__')) ], brackets = ('(', ')', '[', ']', '{', '}')):
        if (_tok_name is None):
            _tok_name = self._tok_name
        len_prog = len(programm)
        for (t_type, t_str, (br, bc), (er, ec), logl) in tokens:

            ttoken = _tok_name[t_type]
            for t in _tok_name:
                if (ttoken == t):
                    #ui.query(u'%d %d %d %d' % (br, er, bc, ec), 'query')
                    len_t = len(t_str)
                    last_pos = programm.find(t_str,  cur_pos, len_prog)
                    if (t == 'NAME'):
                        if (t_str in kws):
                            t = 'KWNAME'
                        elif (t_str in builtins):
                            t = 'BUILTIN'
                        elif (t_str in allmodules):
                            t = 'MODULE'
                        elif (t_str == 'self'):
                            t = 'SELF'
                        elif (t_str == 'cls'):
                            t = 'CLS'
                    elif (t == 'OP'):
                        if (t_str in brackets):
                            t = 'BRACKETS'
                        elif (t_str in ('%', ':')):
                            t = 'PERCENT'
                    yield (last_pos, len_t, t)
                    cur_pos = (last_pos + len_t)
                else:
                    continue



    def processing(self, programm = '', cur_pos=0, app = ui.app, StringIO = __import__('StringIO').StringIO, recursion_limit=[3]):
        if (len(programm) > 35000):
            ui.note(u'Too big size of source', 'error')
            return
        readline = StringIO(programm).readline
        Tokens = tokenize.generate_tokens(readline)
        try:
            lst_t = self.parse(programm, Tokens, cur_pos=cur_pos)
        except Exception, e:
            #print e;return
            if recursion_limit[0] > 0:
                recursion_limit[0] -= 1
                return self.highlighting(programm=programm[:-4], startpos=self.startpos)
            else: return
        recursion_limit[0] = 10
        return lst_t



    def highlighting(self, programm=None, startpos=0, inline=0, body='script', app=ui.app):
        global tokenize
        if not tokenize:
            import easytokenize as tokenize
            self._tok_name = tokenize.tok_name
        kaapython_app = globals()['app']

        (keyword, module, builtin, number, string, name, op, comment, bracket, percent, self_, cls_) = (TokenColor.keyword, TokenColor.module, TokenColor.builtin, TokenColor.number, TokenColor.string, TokenColor.name, TokenColor.operation, TokenColor.comment, TokenColor.bracket, TokenColor.percent, TokenColor.self_, TokenColor.cls_)
        self.startpos = startpos
        text = app.body
        if (programm is None):
            programm = (text.get().replace(u'\u2029', u'\n') + '\n\n\n')
        else: programm += '\n\n\n'
        
        fs = text.font[1]
        fonttheme = getattr(kaapython_app.settings.text.fontthemes, kaapython_app.settings.text.fontthemes.current_theme.lower())
        acolor = (body == 'script' and fonttheme.fontcolor) or kaapython_app.settings.python.shellfontcolor

        def _in(color, font, p, l):
            text.color = color
            #text.font = font
            text.apply(startpos + p, l)

        lst_t = self.processing(programm=programm)
        if lst_t is None:
            return
        not inline and notice('Processing text complete')
        for (p, l, t) in lst_t:
            if (t == 'KWNAME'):
                _in(keyword, (None,
                 fs,
                 1), p, l)
            elif (t == 'NUMBER'):
                _in(number, (None,
                 fs,
                 1), p, l)
            elif (t == 'NAME'):
                _in(name, (None,
                 fs,
                 1), p, l)
            elif (t == 'OP'):
                _in(op, (None,
                 fs,
                 1), p, l)
            elif (t == 'STRING'):
                _in(string, (None,
                 fs,
                 1), p, l)
            elif (t == 'BRACKETS'):
                _in(bracket, (None,
                 fs,
                 1), p, l)
            elif (t == 'COMMENT'):
                _in(comment, (None,
                 fs,
                 2), p, l)
            elif (t == 'MODULE'):
                _in(module, (None,
                 fs,
                 1), p, l)
            elif (t == 'BUILTIN'):
                _in(builtin, (None,
                 fs,
                 1), p, l)
            elif (t == 'SELF'):
                _in(self_, (None,
                 fs,
                 1), p, l)
            elif (t == 'CLS'):
                _in(cls_, (None,
                 fs,
                 1), p, l)
            elif (t == 'PERCENT'):
                _in(percent, (None,
                 fs,
                 1), p, l)

        text.color = acolor
        app.body = text
        not inline and notice('Highlighting complete')

    #highlighting = timeit(highlighting, logging=True)

    __call__ = highlighting


Code = Highlighter()


class GlobalWindowModifier(object):

    def __init__(self):
        self.shortcut_mode = 0
        self.shortcuts = {}
        self.shortcuts_1 = {}



    def open(self):
        self.apply_settings()



    def focus_changed(self, focus):
        if focus:
            app.windows_menu = ui.screen.get_windows_menu()
            app.windows_menu.sort()
            self.update_menu()
            if (self.typename in ('Text',)):
                set_key_text(_('Options'),
                  u'%s#%d' % (_('Exit'), self.shortcut_mode))



    def get_shortcuts(cls):
        menu = ui.Menu()
        menu.append(ui.MenuItem(_('New'), target=app.new_click))
        menu.append(ui.MenuItem(_('Open...'), target=app.open_click))
        menu.append(ui.MenuItem(_('Python Shell'), target=StdIOWrapper.shell))
        menu.append(ui.MenuItem(_('Run Script...'), target=app.runscript_click))
        menu.append(ui.MenuItem(_('Settings'), target=app.settings_click))
        menu.append(ui.MenuItem(_('Plugins'), target=app.plugins_click))
        menu.append(ui.MenuItem(_('Help'), target=app.help_click))
        menu.append(ui.MenuItem(_('Orientation'), target=app.orientation_click))
        menu.append(ui.MenuItem(_('Exit'), target=app.exit_click))
        menu.append(ui.MenuItem(_('File Menu'), method=cls.popup_file_menu))
        menu.append(ui.MenuItem(_('Do Nothing'), target=passfunc))
        menu.append(ui.MenuItem(_('Change shortcut mode'), method=cls.change_shortcut_mode))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

    def get_shortcuts_items(cls):
        menu = cls.get_shortcuts().copy()
        menu.sort()
        choices = []
        names = []
        for item in menu:
            try:
                target = item.target
            except AttributeError:
                try:
                    target = item.method
                except AttributeError:
                    continue
            name = target.__name__
            if (name in names):
                raise TypeError(('%s: shortcuts names conflict (%s and %s)' % (repr(name),
                 repr(dict(choices)[name]),
                 repr(item))))
            choices.append((name,
             item))
            names.append(name)

        return choices


    get_shortcuts_items = classmethod(get_shortcuts_items)



    def set_shortcut(self, key, item):
        shortcuts = (self.shortcuts, self.shortcuts_1,)[self.shortcut_mode]
        if (item is not None):
            if (key not in self.control_keys):
                self.control_keys += (key,)
            shortcuts[key] = item
        else:
            if (key is self.control_keys):
                keys = list(self.control_keys)
                keys.remove(key)
                self.control_keys = keys
            try:
                del shortcuts[key]
            except KeyError:
                pass



    def control_key_press(self, key):
        try:
            item = (self.shortcuts, self.shortcuts_1,)[self.shortcut_mode][key]
        except KeyError:
            return False
        try:
            target = item.target
        except AttributeError:
            pass
        else:
            target()
        try:
            target = item.method
        except AttributeError:
            pass
        else:
            target(self)
        return True



    def change_shortcut_mode(self):
            self.shortcut_mode = (1, 0,)[self.shortcut_mode]
            self.set_shortcuts()
            notice(_('shortcut mode [%d] enabled') % self.shortcut_mode, 'conf')
            ui.app.exit_key_text = (ui.app.exit_key_text.find(u'#') > 0) and ui.app.exit_key_text[:-1] + u'%d' % self.shortcut_mode or ui.app.exit_key_text + u'#%d' % self.shortcut_mode



    def popup_file_menu(self, _=[None, (u'.', u'a', u'd', u'g', u'j', u'm', u'p', u't', u'w', u',', u'b', u'e', u'h', u'k', u'n', u'q', u'u', u'x', u'0')]):
        null, first = _
        if (null is None) or id(null) != id(self.file_menu):
            null = _[0] = self.file_menu.copy()
            for n, i in enumerate(null):
                i.title = first[n] + ') ' + i.title
        item = null.popup(full_screen=True, search_field=True)
        if item:
            item.target()
        self.reset_control_key()



    def apply_settings(self):
        self.set_shortcuts()



    def set_shortcuts(self):
        items = dict(self.get_shortcuts_items())
        shortcuts = (self.shortcuts, self.shortcuts_1,)[self.shortcut_mode]
        for (key, val,) in shortcuts.items():
            if val:
                try:
                    item = items[val]
                except KeyError:
                    self.set_shortcut(key, None)
                else:
                    self.set_shortcut(key, items[val])
            else:
                self.set_shortcut(key, None)




    def update_settings(cls):
        try:
            ui.screen.rootwin.focus = True
        except AttributeError:
            pass
        try:
            app.set_app_system(app.settings.main.system_app)
        except NameError:
            pass
        for win in ui.screen.find_windows(GlobalWindowModifier):
            win.apply_settings()

        try:
            ui.screen.rootwin.focus = False
        except AttributeError:
            pass

        StdIOWrapper.no_singleton = app.settings.python.run_in_new_shellwindow

        if app.settings.python.include_python_api:
            if not PythonModifier.python_api:
                import zipfile
                api_filename = os.path.join(app.path, 'python_api.zip')
                if zipfile.is_zipfile(api_filename):
                    api_file = zipfile.ZipFile(api_filename, 'r', zipfile.ZIP_DEFLATED)
                    PythonModifier.python_api = api_file .read(api_file.namelist()[0]).decode('cp1251')

    update_settings = classmethod(update_settings)



class RootWindow(ui.RootWindow,
 GlobalWindowModifier):
    typename = 'Desktop'
    redraw_color = 0

    def __init__(self, **kwargs):
        ui.RootWindow.__init__(self, color=self.redraw_color, **kwargs)
        GlobalWindowModifier.__init__(self)
        self.no_popup_menu = False
        self.keys = [ui.EKeySelect]
        self.control_keys = (ui.EKeyBackspace,)
        self.text = (_('Version: %s  %s\nPython for S60: %s\nBased on Ped 2.30.5 beta') % (__version__,
         __versionname__,
         e32.pys60_version))
        self.old_stdio = (sys.stdin,
         sys.stdout,
         sys.stderr)
        sys.stdin = sys.stdout = sys.stderr = StdIOWrapper()



    def open(self, focus = True):
        set_key_text(_('Options'),
         _('Exit'))
        GlobalWindowModifier.open(self)
        ui.RootWindow.open(self, focus)



    def redraw_callback(self, rect):
        ui.RootWindow.redraw_callback(self, rect)
        set_key_text(_('Options'),
                  u'%s#%d' % (_('Exit'), self.shortcut_mode))
        if (len(ui.screen.windows) == 1):
            if app.settings.main.wallpaper:
                self.body.blit(app.wallpaper)
            else:
                white = 16777215
                canvas = ui.layout(ui.EMainPane)[0]
                self.body.polygon(((1, 1), (canvas[0] - 1, 1), (canvas[0] - 1, canvas[1] - 1),(1, canvas[1] - 1)), outline=white, fill=self.redraw_color, width=2)
                if (e32.pys60_version_info[:3] >= (1, 3, 22)):
                    font = ('dense', 14)
                else:
                    font = 'dense'
                space = 8
                m = self.body.measure_text(u'A', font=font)[0]
                h = (m[3] - m[1])
                x, y = 10, (10 + h)
                self.body.text((x - 2, y - 2), u'Kaapython - Python IDEtor', fill=0, font=font)
                self.body.text((x, y), unicode('Kaapython - (Ъ) Python IDEtor', 'utf8'), fill=white, font=font)
                y += space
                self.body.line((x - 1, y - 1, (canvas[0] - x), y - 1), outline=0)
                self.body.line((x, y, (canvas[0] - x), y), outline=white)
                for ln in unicode(self.text).split(u'\n'):
                    ln = ln.strip()
                    y += (space + h)
                    self.body.text((x - 2, y - 2), ln, fill=0, font=font)
                    self.body.text((x, y), ln, fill=white, font=font)




    def close(self):
        r = ui.RootWindow.close(self)
        if r:
            self.shutdown()



    def shutdown(self):
        (sys.stdin, sys.stdout, sys.stderr,) = self.old_stdio
        ui.app.set_exit()



    def key_press(self, key):
        if (key == ui.EKeySelect):
            if self.no_popup_menu:
                return 
            menu = ui.Menu(_(add_tabchar_to('File')))
            menu.append(ui.MenuItem((_('Open...'), u"open a file"), target=app.open_click))

            def make_target(klass):
                return lambda :app.new_file(klass)



            for klass, description in file_windows_types:
                menu.append(ui.MenuItem((_('New %s') % klass.typename, description), target=make_target(klass)))

            item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
            if item:
                target = item.target
                self.no_popup_menu = True

                def do():
                    target()
                    self.no_popup_menu = False


                ui.schedule(do)
        else:
            ui.RootWindow.key_press(self, key)

    def key_press(self, key):
        if (key == ui.EKeySelect):
            if self.no_popup_menu:
                return 
            menu = []
            menu.append((_('Open...'), u"open existing file", app.open_click))

            def make_target(klass):
                return lambda :app.new_file(klass)


            for klass, description in file_windows_types:
                menu.append((_('New %s') % klass.typename, description, make_target(klass)))

            item = ui.popup_menu([(x, y) for x, y, z in menu], _(add_tabchar_to('File')), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
            if item is not None:
                target = menu[item][2]
                self.no_popup_menu = True

                def do():
                    target()
                    self.no_popup_menu = False


                ui.schedule(do)
        else:
            ui.RootWindow.key_press(self, key)



    def set_shortcuts(self):
        GlobalWindowModifier.set_shortcuts(self)
        items = dict(self.get_shortcuts_items())
        shortcuts = (app.settings.main.shortcuts.mode_0, app.settings.main.shortcuts.mode_1,)[self.shortcut_mode]
        for (key, val,) in shortcuts.items():
            if val:
                try:
                    item = items[val]
                except KeyError:
                    self.set_shortcut(key, None)
                else:
                    self.set_shortcut(key, items[val])
            else:
                self.set_shortcut(key, None)
        set_key_text(_('Options'),
                  u'%s#%d' % (_('Exit'), self.shortcut_mode))



    def focus_changed(self, focus):
        GlobalWindowModifier.focus_changed(self, focus)
        ui.RootWindow.focus_changed(self, focus)



    def control_key_press(self, key):
        if (key == ui.EKeyBackspace):
            self.change_shortcut_mode()
            self.reset_control_key()
            return True
        elif GlobalWindowModifier.control_key_press(self, key):
            return True
        return ui.RootWindow.control_key_press(self, key)



class Window(ui.Window,
 GlobalWindowModifier):

    def __init__(self, **kwargs):
        ui.Window.__init__(self, **kwargs)
        GlobalWindowModifier.__init__(self)
        try:
            self.menu = ui.screen.rootwin.menu.copy()
        except AttributeError:
            pass



    def open(self, focus = True):
        GlobalWindowModifier.open(self)
        ui.Window.open(self, focus)



    def focus_changed(self, focus):
        GlobalWindowModifier.focus_changed(self, focus)
        ui.Window.focus_changed(self, focus)



    def control_key_press(self, key):
        if GlobalWindowModifier.control_key_press(self, key):
            return True
        return ui.Window.control_key_press(self, key)



class TextWindow(Window):

    def __init__(self, bodytype=None, **kwargs):
        fonttheme = getattr(app.settings.text.fontthemes, app.settings.text.fontthemes.current_theme.lower())
        Window.__init__(self, **kwargs)
        if (bodytype is None):
            self.body = ui.Text(move_callback=self.move_callback, edit_callback=self.edit_callback, skinned=fonttheme.skinned, scrollbar=True, word_wrap=fonttheme.word_wrap, t9=True)
        else:
            self.body = ui.Text()
            self.body.read_only = True
        self.size = size = fonttheme.screen_size
        self.bookmarks = []
        self.find_text = u''
        self.keys += (ui.EKeyEnter,
         ui.EKeySelect,
         ui.EKeyHome)
        self.control_keys += (ui.EKeyLeftArrow,
         ui.EKeyRightArrow,
         ui.EKeyUpArrow,
         ui.EKeyDownArrow,
         ui.EKeyEdit,
         ui.EKeyBackspace)
        self.file_menu = app.file_menu.copy()
        edit_menu = ui.Menu(_(add_tabchar_to('Edit')))
        edit_menu.append(ui.MenuItem(_('Find...'), target=self.find_click))
        edit_menu.append(ui.MenuItem(_('Find Previous'), target=self.findprev_click))
        edit_menu.append(ui.MenuItem(_('Find Next'), target=self.findnext_click))
        edit_menu.append(ui.MenuItem(_('Find All...'), target=self.findall_click))
        edit_menu.append(ui.MenuItem(_('Go to Line...'), target=self.gotoline_click))
        edit_menu.append(ui.MenuItem(_('Top'), target=self.move_beg_of_document))
        edit_menu.append(ui.MenuItem(_('Bottom'), target=self.move_end_of_document))
        edit_menu.append(ui.MenuItem(_('Replace Text'), target=self.replace_text))
        edit_menu.append(ui.MenuItem(_('Go to Bookmark...'), target=self.go_to_bookmark))
        edit_menu.append(ui.MenuItem(_('Add Bookmark'), target=self.add_bookmark))
        self.edit_menu = edit_menu
        edit_item = ui.MenuItem(_(add_tabchar_to('Edit')), target=ui.run_menu_item(edit_menu))
        try:
            file_item = self.menu.find(title=self.file_menu.title)[0]
        except IndexError:
            self.menu.insert(0, edit_item)
        else:
            self.menu.insert((self.menu.index(file_item) + 1), edit_item)
        full_screen_title = _('Full Screen')
        fullscreen_item = ui.MenuItem(full_screen_title, target=self.fullscreen_click)
        try:
            tools_menu = app.tools_menu
        except AttributeError:
            if not edit_menu.find(title=full_screen_title): edit_menu.append(fullscreen_item)
        else:
            if not tools_menu.find(title=full_screen_title): tools_menu.append(fullscreen_item)
        self.startpos_selection = None



    def enter_key_press(self):
        pass



    def edit_callback(self, pos, anchor):
        pass



    def go_to_bookmark(self):
        bookmarks = self.bookmarks
        if not bookmarks: return
        positions, titles = [], []
        for (pos, title) in bookmarks:
            positions.append(pos) or titles.append(title)
        bookmark = ui.selection_list(titles, True)
        if bookmark is None: return
        self.body.set_pos(positions[bookmark])



    def add_bookmark(self):
        pos = self.body.get_pos()
        ln, lpos, line = self.get_line_from_pos()
        line = line[pos - lpos:]
        self.bookmarks.append((pos, line.lstrip()))
        notice(_('Bookmarks++'))
        



    def key_press(self, key):
        if (key == ui.EKeySelect):
            self.body.add(u'\n')
            if (self.typename in ('Text',)):
                set_key_text(_('Options'), _('Exit'))
            ui.schedule(self.enter_key_press)
            self.body.set_case(2)
        elif (key == ui.EKeyEnter):
            ui.schedule(self.enter_key_press)
            self.body.set_case(2)
        elif (key == ui.EKeyHome):
            self.move_beg_of_line(immediate=False)
            self.body.set_case(2)
        else:
            Window.key_press(self, key)



    def control_key_press(self, key):
        if (key == ui.EKeyLeftArrow):
            self.move_beg_of_line(immediate=True)
            self.reset_control_key()
        elif (key == ui.EKeyRightArrow):
            self.move_end_of_line(immediate=True)
            self.reset_control_key()
        elif (key == ui.EKeyUpArrow):
            self.move_page_up()
            self.move_callback()
            return True
        elif (key == ui.EKeyDownArrow):
            self.move_page_down()
            self.move_callback()
            return True
        elif (key == ui.EKeyEdit):
            self.popup_edit_menu()
        elif (key == ui.EKeyBackspace):
            self.change_shortcut_mode()
            self.reset_control_key()
            return True
        else:
            return Window.control_key_press(self, key)
        return False



    def get_shortcuts(cls):
        menu = Window.get_shortcuts()
        menu.append(ui.MenuItem(_('Go to Bookmark...'), method=cls.go_to_bookmark))
        menu.append(ui.MenuItem(_('Add Bookmark'), method=cls.add_bookmark))
        menu.append(ui.MenuItem(_('Find...'), method=cls.find_click))
        menu.append(ui.MenuItem(_('Find Previous'), method=cls.findprev_click))
        menu.append(ui.MenuItem(_('Find Next'), method=cls.findnext_click))
        menu.append(ui.MenuItem(_('Find All...'), method=cls.findall_click))
        menu.append(ui.MenuItem(_('Go to Line...'), method=cls.gotoline_click))
        menu.append(ui.MenuItem(_('Top'), method=cls.move_beg_of_document))
        menu.append(ui.MenuItem(_('Bottom'), method=cls.move_end_of_document))
        menu.append(ui.MenuItem(_('Full Screen'), method=cls.fullscreen_click))
        menu.append(ui.MenuItem(_('Replace Text'), method=cls.replace_text))
        menu.append(ui.MenuItem(_('Edit Menu'), method=cls.popup_edit_menu))
        menu.append(ui.MenuItem(_('Set Selection'), method=cls.set_selection_text))
        menu.append(ui.MenuItem(_('Paste Text'), method=cls.paste_text))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

    def move_callback(self):
        pass


    def popup_edit_menu(self, _=[None, (u'.', u'a', u'd', u'g', u'j', u'm', u'p', u't', u'w', u',', u'b', u'e', u'h', u'k', u'n', u'q', u'u', u'x', u'0')]):
        null, first = _
        if (null is None) or id(null) != id(self.edit_menu):
            null = _[0] = self.edit_menu.copy()
            for n, i in enumerate(null):
                i.title = first[n] + ') ' + i.title
        item = null.popup(full_screen=True, search_field=True)
        if item:
            item.target()
        self.reset_control_key()



    def set_style(self, **kwargs):
        ofont = self.body.font
        try:
            (ofont, osize, oflags,) = ofont
            extended = True
        except:
            (osize, oflags) = (0, 0)
            extended = False
        do = False
        font = pop(kwargs, 'font', ofont)
        size = pop(kwargs, 'size', osize)
        if pop(kwargs, 'antialias', (oflags & 16)):
            flags = 16
        else:
            flags = 32

        style = pop(kwargs, 'style', None) or app.settings.text.fontthemes.light.fontstyle
        style_flags = 0
        parameters = zip((style.fontbold, style.fontitalic, style.fontunderline, style.fontstrikethrough), (ui.STYLE_BOLD, ui.STYLE_ITALIC, ui.STYLE_UNDERLINE, ui.STYLE_STRIKETHROUGH))
        for (bool, param) in parameters:
            if bool:
                style_flags |= param
        parameters1 = zip((style.fonthighlightstandard, style.fonthighlightrounded, style.fonthighlightshadow), (ui.HIGHLIGHT_STANDARD, ui.HIGHLIGHT_ROUNDED, ui.HIGHLIGHT_SHADOW))
        for (bool, param) in parameters1:
            if bool:
                style_flags |= param; break

        color = pop(kwargs, 'color', self.body.color)
        highlight_color = pop(kwargs, 'highlight_color', self.body.highlight_color)
        if extended:
            self.body.font = (font,
             size,
             flags)
        else:
            self.body.font = font
        self.body.style = style_flags
        self.body.color = color
        self.body.highlight_color = get_color(highlight_color)
        pos = self.body.get_pos()
        self.body.set_word_wrap(pop(kwargs, 'word_wrap'))
        self.size = pop(kwargs, 'screen_size', ui.sizNormal)
        self.body.apply()
        self.body.set_pos(pos)
        if kwargs:
            raise TypeError(('TextWindow.set_style() got an unexpected keyword argument(s): %s' % ', '.join([ repr(x) for x in kwargs.keys() ])))


    def apply_settings(self):
        hl = app.settings.python.highlighting
        TokenColor.setColors(hl.keyword, hl.module, hl.builtin, hl.number, hl.string, hl.name, hl.operation, hl.comment, hl.bracket, hl.percent, hl.self_, hl.cls_)
        fonttheme = getattr(app.settings.text.fontthemes, app.settings.text.fontthemes.current_theme.lower())
        self.set_style(font=fonttheme.fontname, size=fonttheme.fontsize, style=fonttheme.fontstyle, antialias=fonttheme.fontantialias, color=fonttheme.fontcolor, highlight_color=fonttheme.font_highlight_color, word_wrap=fonttheme.word_wrap, screen_size=fonttheme.screen_size)
        self.set_shortcuts()



    def set_shortcuts(self):
        Window.set_shortcuts(self)
        items = dict(self.get_shortcuts_items())
        shortcuts = (app.settings.text.shortcuts.mode_0, app.settings.text.shortcuts.mode_1,)[self.shortcut_mode]
        for (key, val,) in shortcuts.items():
            if val:
                try:
                    item = items[val]
                except KeyError:
                    self.set_shortcut(key, None)
                else:
                    self.set_shortcut(key, items[val])
            else:
                self.set_shortcut(key, None)



    def get_lines(self):
        lines = []
        pos = 0
        n = 1
        lst = self.body.get().splitlines()
        if (not lst):
            lst.append(u'')
        for line in lst:
            lines.append((n,
             pos,
             line))
            n += 1
            pos += (len(line) + 1)

        return lines



    def get_line_from_pos(self, pos = None, lines = None):
        if (pos is None):
            pos = self.body.get_pos()
        if (lines is None):
            lines = self.get_lines()
        for (ln, lpos, line,) in lines:
            if lpos <= pos <= (lpos + len(line)):
                break

        return (ln,
         lpos,
         line)



    def find_click(self):
        find_text = ui.query(_('Find:'), 'text', self.find_text, ok=_('Accept'), cancel=_('Decline'))
        if find_text:
            self.find_text = find_text
            self.findnext_click(False)
        self.reset_control_key()



    def findprev_click(self, skip = True):
        find_text = self.find_text.lower()
        if (not find_text):
            self.find_click()
            return
        i = self.body.get_pos()
        text = self.body.get().lower()
        while True:
            pos = i
            if (skip and (text[i - len(find_text):i] == find_text)):
                i -= len(find_text)
            i = text.rfind(find_text, 0, i)
            if i >= 0:
                self.body.set_pos(i)
                self.move_callback()
            elif (pos != 0):
                if ui.query(_('Not found, start from ending?'), 'query', ok=_('Accept'), cancel=_('Decline')):
                    i = -1
                    skip = False
                    continue
            else:
                ui.note(_('Not found'))
            break

        self.reset_control_key()



    def findnext_click(self, skip = True):
        find_text = self.find_text.lower()
        if (not find_text):
            self.find_click()
            return 
        text = self.body.get().lower()
        i = self.body.get_pos()
        while True:
            pos = i
            if (skip and (text[i:(i + len(find_text))] == find_text)):
                i += len(find_text)
            i = text.find(find_text, i)
            if (i >= 0):
                self.body.set_pos(i)
                self.move_callback()
            elif (pos != 0):
                if ui.query(_('Not found, start from beginning?'), 'query', ok=_('Accept'), cancel=_('Decline')):
                    i = 0
                    skip = False
                    continue
            else:
                ui.note(_('Not found'))
            break

        self.reset_control_key()



    def findall_click(self):
        find_text = ui.query(_('Find All:'), 'text', self.find_text, ok=_('Accept'), cancel=_('Decline'))
        if find_text:
            self.find_text = find_text
            find_text = find_text.lower()
            results = []
            for (ln, lpos, line,) in self.get_lines():
                pos = 0
                while 1:
                    pos = line.lower().find(find_text, pos)
                    if (pos < 0):
                        break
                    results.append((ln,
                     lpos,
                     line,
                     pos))
                    pos += len(find_text)


            if results:
                win = FindResultsWindow(title=(_('Find: %s') % find_text), results=results)
                line = win.modal(self)
                if line:
                    self.body.set_pos((line[1] + line[3]))
            else:
                ui.note(_('Not found'))
        self.reset_control_key()



    def gotoline_click(self):
        lines = self.get_lines()
        ln = self.get_line_from_pos(lines=lines)[0]
        ln = ui.query((_('Line (1-%d):') % len(lines)), 'number', ln, ok=_('Accept'), cancel=_('Decline'))
        if (ln is not None):
            if (ln < 1):
                ln = 1
            ln -= 1
            try:
                self.body.set_pos(lines[ln][1])
            except IndexError:
                self.body.set_pos(self.body.len())
        self.reset_control_key()



    def replace_text(self):
        import re
        (text, pos) = (self.body.get(), self.body.get_pos())
        text = text.replace(u'\u2029', u'\n')
        old_text = ui.query(_('Old text'), 'text', ok=_('Accept'), cancel=_('Decline'))
        if (old_text is None):
            return self.reset_control_key()
        pattern = re.compile(r'%s' % old_text)
        if (pattern.search(text) is None):
            ui.note(_('Not found'))
            return self.replace_text()
        new_text = ui.query(_('New text'), 'text', ok=_('Accept'), cancel=_('Decline'))
        if (new_text is None):
            return self.reset_control_key()
        newsource = pattern.sub(new_text, text)
        self.body.set(newsource.replace(u'\n', u'\u2029'))
        self.body.set_pos(pos)
        self.reset_control_key()



    def paste_text(self):
        if self.body.can_paste():
                self.body.paste()
        else:
            notice('Cannot paste', 'error')



    def set_selection_text(self):
        def len_(pos, anchor, text): return abs(pos - anchor)
        if (self.startpos_selection is None):
            self.startpos_selection = self.body.get_pos()
        else:
            (length, pos,) = (self.body.len(), self.body.get_pos(),)
            if ((self.startpos_selection == length) or (pos == length)):
                self.body.insert(length, u'\u2029')
            self.body.set_selection(pos, self.startpos_selection)
            self.startpos_selection = None
            if self.body.can_copy():
                self.body.copy()
                notice(_('Copied %d symbols') % len_(*self.body.get_selection()))
            else:
                notice('Cannot copy', 'error')



    def set_pos(self, pos, immediate = True):
        if immediate:
            self.body.set_pos(pos)
        else:
            ui.schedule(self.body.set_pos, pos)



    def move_beg_of_line(self, immediate = True, force = False):
        pos = self.body.get_pos()
        (lnum, offset, ln,) = self.get_line_from_pos(pos)
        if force:
            indent = 0
        else:
            try:
                indent = ln.index(ln.lstrip()[0])
            except:
                indent = 0
            if (indent == (pos - offset)):
                indent = 0

        if app.settings.text.cursors_step:
            if pos == (offset + indent):
                return self.set_pos(offset, immediate)
            text = self.body.get()
            apos = ((pos > (offset + indent)) and pos - 1) or ((pos == offset) and (offset - 1)) or offset
            word_pos = max(*map(lambda char: text.rfind(char, 0, apos), (u' ', u'\u2029', u'(', u'[', u'{')))
            self.set_pos(word_pos + 2, immediate)
            return ui.schedule(ui.screen._Screen__ekeyyes_handler)
        self.set_pos(offset + indent + 1, immediate)



    def move_end_of_line(self, immediate=True):
        (lnum, offset, ln) = self.get_line_from_pos()
        pos = self.body.get_pos()
        try:
            indent = ln.index(ln.lstrip()[0])
        except:
            indent = 0
        if (indent == (pos - offset)):
            indent = 0
        if app.settings.text.cursors_step:
            text = self.body.get()
            apos = ((pos > (offset + indent)) and pos) or ((pos == offset) and (indent > 0) and (offset + indent - 1)) or (offset + indent)
            candidates = filter(lambda x: x > -1, map(lambda char: text.find(char, apos), (u' ', u'\u2029', u'(', u'[', u'{')))
            if not candidates:
                word_pos = len(text)
            else:
                candidates.sort()
                word_pos = candidates[0]
            self.set_pos(word_pos , immediate)
            return ui.schedule(ui.screen._Screen__ekeyyes_handler)
        self.set_pos(offset + len(ln) - 1, immediate)



    def get_pagesize(self):
        sett = 'pagesize'
        if (self.orientation == ui.oriAutomatic):
            (w, h,) = ui.layout(ui.EApplicationWindow)[0]
            if (w > h):
                sett += 'land'
            else:
                sett += 'port'
        elif (self.orientation == ui.oriLandscape):
            sett += 'land'
        else:
            sett = 'port'
        if (self.size == ui.sizLarge):
            sett = (sett[:-4] + 'full')
        return app.settings.text[sett].get()



    def move_page_up(self):
        self.move_line_up(count=self.get_pagesize())



    def move_page_down(self):
        self.move_line_down(count=self.get_pagesize())



    def move_line_up(self, count = 1):
        lines = self.get_lines()
        pos = self.body.get_pos()
        (ln, lpos, line,) = self.get_line_from_pos(lines=lines, pos=pos)
        i = ((ln - 1) - count)
        if (i < 0):
            i = 0
        lpos = (pos - lpos)
        if (lpos > len(lines[i][2])):
            lpos = len(lines[i][2])
        self.set_pos((lines[i][1] + lpos))



    def move_line_down(self, count = 1):
        lines = self.get_lines()
        pos = self.body.get_pos()
        (ln, lpos, line,) = self.get_line_from_pos(lines=lines, pos=pos)
        i = ((ln - 1) + count)
        if (i >= len(lines)):
            i = -1
        lpos = (pos - lpos)
        if (lpos > len(lines[i][2])):
            lpos = len(lines[i][2])
        self.set_pos((lines[i][1] + lpos))



    def move_beg_of_document(self):
        self.set_pos(0)
        self.reset_control_key()



    def move_end_of_document(self):
        self.set_pos(self.body.len())
        self.reset_control_key()



    def reset_caret(self):
        self.body.set_pos(self.body.get_pos())



    def fullscreen_click(self):
        if (self.size == ui.sizNormal):
            self.size = ui.sizLarge
        elif (self.size == ui.sizLarge):
            self.size = ui.sizFull
        else:
            self.size = ui.sizNormal
        self.reset_control_key()



class FindResultsWindow(Window):
    typename = 'FindResults'

    def __init__(self, **kwargs):
        self.results = pop(kwargs, 'results')
        kwargs.setdefault('title', _('Find All'))
        Window.__init__(self, **kwargs)
        self.body = ui.Listbox([ ((_('Line %d, Column %d') % (x[0],
          x[3])),
         x[2]) for x in self.results ], self.select_click)
        self.menu = ui.Menu()
        self.menu.append(ui.MenuItem(_('Select'), target=self.select_click))
        self.menu.append(ui.MenuItem(_('Exit'), target=self.close))



    def select_click(self):
        self.modal_result = self.results[self.body.current()]
        self.close()



class TextFileWindow(TextWindow):
    typename = 'Text'
    type_ext = '.txt'
    session = ui.SettingsGroup()
    session.append('windows', ui.Setting('', []))

    def __init__(self, **kwargs):
        set_key_text(_('Options'),
         _('Exit'))
        try:
            self.path = pop(kwargs, 'path')
        except KeyError:
            self.path = None
            self.fixed_encoding = False
            self.encoding = 'utf8'
            TextWindow.__init__(self, **kwargs)
        else:
            (text, self.encoding) = self.load()
            self.fixed_encoding = True
            TextWindow.__init__(self, **kwargs)
            self.body.set(text)
            self.body.set_pos(0)
            self.title = os.path.split(self.path)[1].decode('utf8')
        self.autosave_timer = e32.Ao_timer()
        file_menu = ui.Menu()
        file_menu.append(ui.MenuItem(_('Save'), target=self.save))
        file_menu.append(ui.MenuItem(_('Save As...'), target=self.save_as))
        file_menu.append(ui.MenuItem(_('Save All'), target=self.save_all))
        file_menu.append(ui.MenuItem(_('Close'), target=self.close))
        file_menu.append(ui.MenuItem(_('Close All'), target=self.close_all))
        self.file_menu = app.file_menu.copy()
        self.file_menu.extend(file_menu)
        self.menu[self.menu.index(self.menu.find(title=_(add_tabchar_to('File')))[0])] = ui.MenuItem(_(add_tabchar_to('File')), target=ui.run_menu_item(self.file_menu))



    def apply_settings(self):
        TextWindow.apply_settings(self)
        try:
            if (not self.fixed_encoding):
                self.encoding = app.settings.file.encoding
            autosave = app.settings.file.autosave
            self.autosave_timer.cancel()
            if (autosave and (self.path is not None)):
                self.autosave_timer.after(autosave, self.autosave)
        except AttributeError:
            pass



    def can_close(self):
        if (not TextWindow.can_close(self)):
            return False
        text = self.body.get()
        if (self.path is None):
            if (not text):
                return True
        else:
            try:
                if (text == self.load()[0]):
                    return True
            except IOError:
                pass
        menu = ui.Menu(_('Changes'))
        menu.append(ui.MenuItem(_('Save'), value=True))
        menu.append(ui.MenuItem(_('Discard'), value=False))
        item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if item:
            if item.value:
                return self.save()
            else:
                return True
        return False



    def close(self):
        if TextWindow.close(self):
            self.autosave_timer.cancel()
            return True
        return False



    def get_shortcuts(cls):
        menu = TextWindow.get_shortcuts()
        menu.append(ui.MenuItem(_('Save'), method=cls.save_and_popup))
        menu.append(ui.MenuItem(_('Save As...'), method=cls.save_as))
        menu.append(ui.MenuItem(_('Save All'), method=cls.save_all))
        menu.append(ui.MenuItem(_('Close'), method=cls.close))
        menu.append(ui.MenuItem(_('Close All'), method=cls.close_all))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

    def save_and_popup(self):
        if self.save():
            notice('File saved', 'conf')
            return True
        return False



    def load(self):
        if (self.path is None):
            raise IOError('TextFileWindow: no path specified')
        f = file(self.path, 'r')
        text = f.read()
        f.close()
        if (text.startswith('\xff\xfe') or text.startswith('\xfe\xff')):
            enc = 'utf16'
            text = text.decode(enc)
        else:
            for enc in ['utf8',
             'latin1']:
                try:
                    text = text.decode(enc)
                    break
                except UnicodeError:
                    pass
            else:
                raise UnicodeError

        return (text.translate({13: None,
          10: 8233}),
         enc)



    def save(self):
        if (self.path is None):
            return self.save_as()
        autosave = app.settings.file.autosave
        self.autosave_timer.cancel()
        if autosave:
            self.autosave_timer.after(autosave, self.autosave)
        try:
            f = file(self.path, 'w')
            f.write(self.body.get().translate({8232: 8233, 160: 32}).replace(u'\u2029', u'\r\n').encode(self.encoding))
            f.close()
            return True
        except IOError:
            ui.note(_('Cannot save file'), 'error')
            return False



    def autosave(self):
        if self.save():
            notice('File saved')



    def save_as(self):
        path = self.path
        if (path is None):
            path = self.title.encode('utf8')
        win = ui.FileBrowserWindow(mode=ui.fbmSave, path=path, title=_('Save file'))
        path = win.modal(self)
        if (path is None):
            return False
        self.path = path
        self.title = os.path.split(path)[1].decode('utf8')
        ret = self.save()
        if (ret and (os.path.splitext(path)[-1].lower() != self.type_ext.lower())):
            pos = self.body.get_pos()
            self.close()
            win = app.load_file(path)
            if win:
                win.body.set_pos(pos)
        return ret



    def close_all(self):
        ui.screen.close_windows(TextFileWindow)



    def save_all(self):
        for win in ui.screen.find_windows(TextFileWindow):
            if (not win.save()):
                return 



    def store_session(cls):
        windows = cls.session.windows
        del windows[:]
        for win in ui.screen.find_windows(TextFileWindow):
            try:
                e32.ao_yield()
                text = win.body.get()
                encoding = win.encoding
                if (win.load()[0] == text):
                    text = None
                else:
                    raise IOError
            except IOError:
                pass
            if win.path:
                path = win.path
            else:
                path = win.title.encode('utf8')
            windows.insert(0, (path,
             text,
             encoding,
             win.body.get_pos(),
             win.bookmarks,
             win.size))
            from globalui import global_note as note
            note(win.title)

        try:
            if app.settings.file.use_multisessions:
                cls.session.filename = os.path.join(app.sessions_path, str(time.strftime('%X %x', time.localtime(time.time()))).replace(':', "'"))
                try:
                    cls.session.save()
                except IOError:
                    ui.note(_('Cannot update sessions file'), 'error')
        finally:
            cls.session.filename = os.path.join(app.sessions_path, 'session.bin')
        try:
            cls.session.save()
        except IOError:
            ui.note(_('Cannot update sessions file'), 'error')

    store_session = classmethod(store_session)

    def clear_session(cls):
        del cls.session.windows[:]
        cls.session.save()


    clear_session = classmethod(clear_session)

class AutocloseTextWindow(TextWindow):
    typename = 'AutocloseWindow'

    def focus_changed(self, focus):
        if (not focus):
            self.close()



class PythonModifier(object):
    py_namespace = {}
    translating_dict = {8232: 8233, 160: 32,
 1040:97, 1041:98, 1042:99, 1043:99, 1044:100, 1045:101, 1046:102, 1047:102, 1048:103, 1049:104, 1050:105, 1051:105, 1052:106, 1053:107, 1054:108, 1055:108, 1056:109, 1057:110, 1058:111, 1059:111, 1060:112, 1061:113, 1062:114, 1063:115, 1064:116, 1065:117, 1066:118, 1067:118, 1168:119, 1169:120, 1170:121, 1171:122,
 1072:97, 1073:98, 1074:99, 1075:99, 1076:100, 1077:101, 1078:102, 1079:102, 1080:103, 1081:104, 1082:105, 1083:105, 1084:106, 1085:107, 1086:108, 1087:108, 1088:109, 1089:110, 1090:111, 1091:111, 1092:112, 1093:113, 1094:114, 1095:115, 1096:116, 1097:117, 1098:118, 1099:118, 1100:119, 1101:120, 1102:121, 1103:122} # replace characters of russian alphabete to correct work python autocomplete
    python_api = u''

    def __init__(self):
        self.templates = [
         (_('(exp)'), 1, 4),
         (_('((exp))'), 2, 5),
         (_('[exp]'), 1, 4),
         (_('[exp:]'), 1, 4),
         (_('[:exp]'), 2, 5),
         (_('{exp:}'), 1, 4),
         (_('{:exp}'), 2, 5),
         (_("'exp'"), 1, 4),
         (_('"exp"'), 1, 4),
         ]
        edit_menu = self.edit_menu
        for (title, target) in ((_('Call Tip'), self.py_calltip), (_('Edit Autocomplete'), self.edit_autocomplete), (_('Code Highlighting'), Code.highlighting)):
            if not edit_menu.find(title=title):
                edit_menu.append(ui.MenuItem(title=title, target=target))
        ui.power_key_handler = self.apply_filter



    def py_reset_namespace(cls):
        import __main__
        cls.py_namespace.clear()
        cls.py_namespace.update(__main__.__dict__)
        cls.py_namespace.update(__main__.__builtins__.__dict__)
        cls.py_namespace['__name__'] = '__main__'


    py_reset_namespace = classmethod(py_reset_namespace)

    def _get_text(self):
        return (self.body.get(),
         self.body.get_pos())



    def _get_objects(self, exp):
        exp = exp.lower()
        
        try:
            index = abbreviations_keys.index(exp)
            abbrev = abbreviations_values[index]
            return {abbrev + '$': None}
        except ValueError: pass
        
        if (not exp) or not (filter(lambda char: (95 <= ord(char) <= 122) , exp)): return {} # from A to z
        def get_limits(limit, alpha=(u'abc2', u'def3', u'ghi4', u'jkl5', u'mno6', u'pqrs7', u'tuv8', u'wxyz9')):
            if len(limit) < 2: return (limit[0],)
            else: one, two = limit[:2]
            result, seqs = [], []
            for seq in alpha:
                if one in seq:
                   if seqs: seqs.insert(0, seq); break
                   else: seqs.insert(0, seq)
                if two in seq:
                   if seqs: seqs.append(seq); break
                   else: seqs.append(seq)
            for char0 in seqs[0][:-1]:
                for char1 in seqs[1]:
                    result.append(u'%s%s' % (char0, char1))
            return result

        i = exp.rfind('.')
        if (i > 0):
            (exp, limit,) = (exp[:i],
exp[(i + 1):])
        elif (i == 0):
            return {}
        else:
            (exp, limit,) = ('', exp)
        limit = limit.strip()
        try: limits = get_limits(limit)
        except IndexError: limits =(limit,)

        Names = {}
        tempindex = 0
        text = u'u\u2029%s' % self.body.get()
        length = len(text)
        count, find, rfind = text.count, text.find, text.rfind

        for N in xrange(count(u'=')):
            tempindex = find(u'=', tempindex + 1, length)
            if tempindex == -1: break
            index_name = max(
 rfind(u' ', 0, tempindex-1),
 rfind(u'\u2029', 0, tempindex),
 rfind(u',', 0, tempindex),
 rfind(u'(', 0, tempindex),
 rfind(u';', 0, tempindex),
 rfind(u'=', 0, tempindex),
 0) + 1
            candidat = text[index_name: tempindex].strip()
            if candidat.startswith(limit):
                Names[candidat.encode('utf8')] = 1
                continue
            for b in limits:
                if candidat.lower().startswith(b): Names[candidat.encode('utf8')] = 1

        defi = classi = 0
        for n in xrange(max(count(u'def '), count(u'class '))):
            if defi is not None:
                defi = find(u'def ', defi, length) + 4
                if defi == 3: defi = None; continue # 3 <==> -1 + 4
                defe = max(
  min(
    find(u'(', defi, length),
    find(u'\u2029', defi, length),
    find(u' ', defi, length),
    length),
  0
  )
                candidat = text[defi:defe].strip()
                if candidat.startswith(limit):
                    Names[candidat.encode('utf8')] = 1
                    continue
                for b in limits:
                    if candidat.lower().startswith(b): Names[candidat.encode('utf8')] = 1
            if classi is not None:
                classi = find(u'class ', classi, length) + 6
                if classi == 5: classi = None; continue
                classe = max(
  min(
    find(u'(', classi, length),
    find(u'\u2029', classi, length),
    find(u' ', classi, length),
    find(u':', classi, length),
    length),
  0
  )
                candidat = text[classi:classe].strip()
                if candidat.startswith(limit):
                    Names[candidat.encode('utf8')] = 1
                    continue
                for b in limits:
                    if candidat.lower().startswith(b): Names[candidat.encode('utf8')] = 1
            if defi is classi is None: break

        For = 0
        for n in xrange(count(u'for ')):
            For = find(u'for ', For, length) + 4
            if For == 3: continue
            In = find(u' in ', For, length)
            if In == -1: continue
            nextline = find(u'\u2029', For, length)
            endloop = find(u':', For, length)
            if (nextline < In > endloop): continue
            candidat = text[For:In].strip()
            for char in u'(),': candidat = candidat.replace(char, u' ')
            candidats = candidat.split()
            for name in candidats:
                if name.startswith(limit):
                    Names[name.encode('utf8')] = 1
                    continue
                for b in limits:
                    if name.lower().startswith(b): Names[name.encode('utf8')] = 1

        Import = 0
        for n in xrange(count(u'import ')):
            Import = find(u'import ', Import, length) + 7
            nextline = find(u'\u2029', Import, length)
            if nextline == - 1: continue
            if find(u';', Import, nextline) != -1:
                nextline = find(u';', Import, nextline)
            words = text[Import: nextline].strip().split(u',')
            for w in words:
                candidat = w.split(u' as ')[-1].strip()
                if candidat.startswith(limit):
                    Names[candidat.encode('utf8')] = 1
                    continue
                for b in limits:
                    if candidat.lower().startswith(b): Names[candidat.encode('utf8')] = 1

        Names = Names.keys()
        Names.sort(lambda a, b:-(a.lower() < b.lower()))

        if exp:
            namespace = sys.modules.copy()
            namespace.update(self.py_namespace)
            try:
                d = [x for x in eval(('dir(%s)' % exp), namespace) if x.startswith(limit)]
                return dict([(x, eval(('%s.%s' % (exp, x)), namespace)) for x in d ] + [(name, name) for name in Names])
            except:
                pass
        else:
            try:
                d = [x for x in eval('dir()', self.py_namespace) if x.startswith(limit)]
                return dict([(x, eval(x, self.py_namespace)) for x in d] + [(name, name) for name in Names])
            except:
                pass
        return {}



    def _get_object(self, exp):
        d = self._get_objects(exp)
        if (len(d) == 1) and d.keys()[0][-1]== '$': return d.popitem()[0]
        try:
            return d[exp[(exp.rfind('.') + 1):]]
        except:
            pass



    def _get_expression(self, text=None, pos=None, and_pos=False):
        if ((text is None) or (pos is None)):
            (ttext, tpos,) = self._get_text()
            if (text is None):
                text = ttext
            if (pos is None):
                pos = tpos
        begpos = pos
        brackets = {u'(': u')',
         u'[': u']',
         u'{': u'}'}
        brstack = []
        quote = u''
        pos -= 1
        lastc = lastnwc = ''
        while (pos >= 0):
            c = text[pos]
            if (c in u'"\''):
                if (not quote):
                    quote = c
                elif ((c == quote) and ((pos == 0) or (text[(pos - 1)] != u'\\'))):
                    quote = ''
            elif (not quote):
                if (c in brackets.values()):
                    if (lastnwc.isalnum() or (lastnwc in (u'', u'_'))):
                        break
                    brstack.append(c)
                elif (c in brackets.keys()):
                    if (not brstack):
                        break
                    if (brstack.pop() != brackets[c]):
                        break
                elif (not brstack):
                    if (c.isalnum() or (c in u'._')):
                        if lastc.isspace():
                            if ((lastnwc not in (u'', u'.')) or (c != u'.')):
                                break
                    elif (not c.isspace()):
                        break
            lastc = c
            if (not c.isspace()):
                lastnwc = c
            pos -= 1

        pos += 1
        try:
            if not and_pos: return text[pos:begpos].lstrip().translate(self.translating_dict).replace(u'\u2029', u'\n').encode('utf8')
            else: return (text[pos:begpos].lstrip().translate(self.translating_dict).replace(u'\u2029', u'\n').encode('utf8'), begpos)
        except UnicodeError:
            if not and_pos: return ''
            else: return ('', begpos)



    def _expression_to_title(self, exp):
        r = exp.replace('\n', ' ')
        title = ''
        while (title != r):
            title = r
            r = title.replace('  ', ' ')

        return title.strip().decode('utf8')



    def apply_filter(self):
        pos, anchor, text = self.body.get_selection()
        self.body.set_input_mode(ui.ENumericInputMode)
        filters = 'capitalize', 'center', 'encode', 'ljust', 'lower', 'lstrip', 'replace', 'rjust', 'rstrip', 'split', 'strip', 'swapcase', 'title', 'upper', 'zfill'
        preactions = False, (ui.query, _('Set width'), 'number', 0), (ui.query, _('Set encoding'), 'text', 'utf8'), (ui.query, _('Set width'), 'number', 0), False, False, (ui.multi_query, _('Replace'), _('To')), (ui.query, _('Set width'), 'number', 0), False, (ui.query, _('Separator'), 'text', ''), False, False, False, False, (ui.query, _('Set width'), 'number', 0),
        
        filter = ui.popup_menu(map(unicode, filters), _('Select filter:'), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if filter is None:
            return
        self.body.cut()
        preaction = preactions[filter]
        if preaction:
            arg = preaction[0](*preaction[1:])
            if arg is None:
                arg = arg[-1]
                text = getattr(text, filters[filter])(*arg)
        else:
            text = getattr(text, filters[filter])()
        
        self.body.add(text)
        ui.schedule(self.body.set_input_mode, ui.ETextInputMode)



    def py_get_indent(self, text, pos):
        pos -= 1
        i = (pos - 1)
        while (i >= 0):
            if (text[i] in (u'\u2028',
             u'\u2029')):
                break
            i -= 1

        i += 1
        strt = i
        while ((i < pos) and text[i].isspace()):
            i += 1

        ind = (i - strt)
        if (pos > 0):
            if (text[(pos - 1)] == u':'):
                ind += app.settings.python.indentsize
            else:
                level = 0
                while (i < pos):
                    if (text[i] in u'([{'):
                        level += 1
                    elif (text[i] in u')]}'):
                        level -= 1
                    i += 1

                if (level > 0):
                    ind += app.settings.python.indentsize
        lines_begin = text.rfind(u'\u2029', 0, pos)
        if text[lines_begin:pos].isspace() and text[text.rfind(u'\u2029', 0, lines_begin):pos].isspace():
            ind -= app.settings.python.indentsize
        
        return (u' ' * ind)



    def py_insert_indent(self):
        (text, pos) = self._get_text()
        indent = self.py_get_indent(text, pos)
        self.body.add(indent)



    def py_autocomplete(self, empty_list=True, defaults=[None]):

        def finalizer(in_template=False):
            if in_template:
                templates = self.templates
                tmpl = ui.popup_menu([i[0] for i in templates], _('%expression%'), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
                if tmpl is None: return
                else:
                    self.body.insert(cur_pos - len(exp), templates[tmpl][0][:templates[tmpl][1]])
                    self.body.add(templates[tmpl][0][templates[tmpl][2]:])
            else:
                ws = s = unicode(item.title, 'utf8', 'ignore')

                if s[-1] == '$':
                    s = s[:-1].replace('<|>', '')
                    pos = cur_pos - len(exp)
                    self.body.delete(max(0, pos), len(exp))
                    self.body.set_input_mode(ui.ENumericInputMode)
                    self.set_pos(pos)
                    self.body.add(s)
                    ui.schedule(self.body.set_input_mode, ui.ETextInputMode)
                    Code.highlighting(programm=s, startpos=max(0, pos), inline=1)
                    if (item.offset != -1):
                        self.set_pos(pos + item.offset)
                    return

                n = exp.split(u'.')[-1]
                if s.startswith(n):
                    s = s[len(n):]
                else:
                    if (ws in data):
                        self.body.delete(max(0, cur_pos - len(exp)), len(exp))
                        self.set_pos(cur_pos - len(exp))
                self.body.add(s)
            last_pos = self.body.get_pos()
            if hasattr(item, 'offset'):
                if (item.offset is not None):
                    Code.highlighting(programm=ws, startpos=(self.body.get_pos() - len(ws)), inline=1)
                    self.body.set_pos(((self.body.get_pos() - len(ws)) + item.offset))
            else:
                self.body.set_input_mode(ui.ENumericInputMode)
                self.set_pos(last_pos)
                ui.schedule(self.body.set_input_mode, ui.ETextInputMode)
                Code.highlighting(programm=ws, startpos=max(0, cur_pos - len(ws)), inline=1)


        exp, cur_pos = self._get_expression(and_pos=True)
        data = self._get_objects(exp).keys()
        if not empty_list and not data:
            return
        data.sort()

        if (len(data) == 1) and data[0][-1] == '$':
            item = ui.MenuItem(data[0], offset=data[0].find('<|>'))
            return finalizer()

        try: menu = ui.Menu(('%s*' % self._expression_to_title(data[0])))
        except IndexError: menu = ui.Menu(('%s*' % self._expression_to_title(exp)))
        menu.extend([ui.MenuItem(title) for title in data])
        menu.extend([ui.MenuItem(title, offset=off) for (title, off) in statements if title.startswith(exp)])
        if defaults[0]: menu.extend([item for item in defaults if item.title.startswith(exp)])
        else:
            defaults.remove(None)
            defaults.extend([ui.MenuItem(title, offset=len(title)) for title in ('__all__', '__builtins__', '__class__', '__delattr__', '__delitem__', '__delslice__', '__dict__', '__doc__', '__file__', '__getattribute__', '__getitem__', '__getslice__', '__hash__', '__init__', '__len__', '__module__', '__name__', '__new__', '__reduce__', '__repr__', '__setattr__', '__setitem__', '__setslice__', '__str__', '__weakref__', '_appuifw', '_uicontrolapi', 'activate_tab', 'add', 'allow_undo', 'ao_callgate', 'Ao_lock', 'ao_sleep', 'Ao_timer', 'ao_yield', 'app', 'apply', 'available_fonts', 'bind', 'can_copy', 'can_cut', 'can_paste', 'can_undo', 'Canvas', 'clear', 'clear_selection', 'clear_undo', 'color', 'Content_handler', 'copy', 'cut', 'delete', 'drive_list', 'e32', 'EAColumn', 'EApplicationWindow', 'EBatteryPane', 'EBColumn', 'ECColumn', 'EContextPane', 'EControlPane', 'EControlPaneBottom', 'EControlPaneTop', 'EDColumn', 'EEventKey', 'EEventKeyDown', 'EEventKeyUp', 'EFindPane', 'EHCenterVBottom', 'EHCenterVCenter', 'EHCenterVTop', 'EHLeftVBottom', 'EHLeftVCenter', 'EHLeftVTop', 'EHRightVBottom', 'EHRightVCenter', 'EHRightVTop', 'EIndicatorPane', 'EMainPane', 'ENaviPane', 'EScreen', 'ESignalPane', 'EStaconBottom', 'EStaconTop', 'EStatusPane', 'EStatusPaneBottom', 'EStatusPaneTop', 'ETitlePane', 'EUniversalIndicatorPane', 'EWallpaperPane', 'FFormAutoFormEdit', 'FFormAutoLabelEdit', 'FFormDoubleSpaced', 'FFormEditModeOnly', 'FFormViewModeOnly', 'file_copy', 'focus', 'font', 'Form', 'full_name', 'get', 'get_pos', 'get_selection', 'get_word_info', 'has_changed', 'highlight_color', 'HIGHLIGHT_ROUNDED', 'HIGHLIGHT_SHADOW', 'HIGHLIGHT_STANDARD', 'Icon', 'in_emulator', 'inactivity', 'is_ui_thread', 'indicator_text', 'InfoPopup', 'insert', 'layout', 'len', 'Listbox', 'menu_key_text', 'menu_key_handler', 'exit_key_text', 'exit_key_handler', 'init_menu', 'handle_menu_key', 'move', 'move_display', 'multi_query', 'multi_selection_list', 'note', 'paste', 'popup_menu', 'pos2xy', 'pys60_version', 'pys60_version_info', 'query', 'read_only', 'reset_inactivity', 's60_version_info', 'select_all', 'selection_list', 'set', 'set_home_time', 'set_allowed_cases', 'set_allowed_input_modes', 'set_case', 'set_exit', 'set_input_mode', 'set_limit', 'set_pos', 'set_selection', 'set_tabs', 'set_undo_buffer', 'set_word_wrap', 'start_exe', 'start_server', 'strerror', 'style', 'STYLE_BOLD', 'STYLE_ITALIC', 'STYLE_STRIKETHROUGH', 'STYLE_UNDERLINE', 'Text', 'uid', 'undo', 'xy2pos')])
        menu.sort()
        symbitems = [ui.MenuItem(title, offset=off) for (title, off,) in symbols]
        if exp:
            menu.extend(symbitems)
        else:
            menu[:] = (symbitems + menu)
        menu.extend([item for item in defaults if item.title.startswith(exp)])
        menu.extend([ui.MenuItem('doc', offset=None), ui.MenuItem('(expression)', offset=None)])
        item = menu.popup(full_screen=True, search_field=True)
        if (item is not None):
            key = unicode(item.title, 'utf8', 'ignore')
            if key == u'doc':
              if exp:
                f_pos = self.python_api.find(u'\r\n' + exp)
                if f_pos == - 1:
                    return
                last = f_pos
                while True:
                    nlast = self.python_api.find(u'\r\n' + exp, last + 1)
                    if nlast == -1:
                        break
                    else:
                        last = nlast
                new_line = self.python_api.find(u'\r\n', last + 1)
                api = self.python_api[f_pos + 1: new_line][:51200]
                help_for = HelpWindow(title=_('Help for %s') % exp, head=u'$', text=api)
                help_for.open()
              return
            elif key == u'(expression)':
                if exp:
                    return finalizer(in_template=True)
                return
            elif (key in subsymbols.keys()):
                menu = ui.Menu(self._expression_to_title(exp))
                menu.extend([ ui.MenuItem(title, offset=off) for (title, off,) in statements if title.startswith(exp) ])
                menu.sort()
                symbitems = [ ui.MenuItem(title, offset=off) for (title, off,) in subsymbols[key] ]
                if exp:
                    menu.extend(symbitems)
                else:
                    menu[:] = (symbitems + menu)
                item = menu.popup(full_screen=True, search_field=True)
                if (item is None):
                    return 

            finalizer()



    def edit_autocomplete():

        def with_save():
            try:
                save = open('C:\\Data\\symbols', 'w')
                save.write(str(symbols).encode('base64'))
                save.close()
                notice('Action complete', 'conf')
            except Exception, e:
                ui.note(_(e), 'conf')

        action = ui.popup_menu([_('Add'),
         _('Delete'),
         _('Change')], _('Select action:'), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if (action is None):
            return 
        all = [ ('%s'.decode('utf8') % s[0]) for s in symbols ]
        if (action == 0):
            edit_item = ui.query(u"('()', 1)", 'text', u"('', 0)", ok=_('Accept'), cancel=_('Decline'))
            if ((edit_item is None) or ((edit_item == u"('', )") or (len(filter(edit_item.count, (u'(',
             u')',
             u',',
             u"'"))) != 4))):
                return 
            elif (edit_item.startswith(u'(') and edit_item.endswith(u')')):
                select = ui.popup_menu([_('<- To start of list'),
                 _('To end of list ->'),
                 _('To pos. in list')], _('Where insert?'), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
                if (select == 0):
                    symbols.insert(0, eval(edit_item))
                elif (select == 1):
                    symbols.append(eval(edit_item))
                elif (select == 2):
                    pos = ui.popup_menu(all, _('Where insert?'), left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
                    if (pos is not None):
                        symbols.insert(pos, eval(edit_item))
            with_save()
            return 
        index_edit_item = ui.selection_list(all)
        if (index_edit_item is None):
            return 
        elif (action == 1):
            symbols.remove(symbols[index_edit_item])
        elif (action == 2):
            edit_item = ui.query(_('Change'), 'text', unicode(symbols[index_edit_item]), ok=_('Accept'), cancel=_('Decline'))
            if (edit_item is None):
                return 
            elif (edit_item.startswith(u'(') and edit_item.endswith(u')')):
                symbols[index_edit_item] = eval(edit_item)
        with_save()


    edit_autocomplete = staticmethod(edit_autocomplete)

    def py_calltip(self):
        stdhelp = _('Put cursor inside argument parenthesis')
        (text, pos,) = self._get_text()
        pos -= 1
        lev = 0
        while (pos >= 0):
            if (text[pos] == u'('):
                lev -= 1
                if (lev < 0):
                    break
            elif (text[pos] == u')'):
                lev += 1
            pos -= 1
        else:
            ui.note(stdhelp)
            return 

        while (pos >= 0):
            if (not text[pos].isspace()):
                break
            pos -= 1
        else:
            ui.note(stdhelp)
            return 

        exp = self._get_expression(text, pos)
        if exp:
            title = self._expression_to_title(exp)
            try:
                from globalui import global_msg_query
                win = None
            except ImportError:
                win = AutocloseTextWindow(title=(u'%s - %s' % (_('Call Tip'),
                 title)))
                menu = ui.Menu()
                menu.append(ui.MenuItem(_('Close'), target=win.close))
                win.menu = menu
            obj = self._get_object(exp)
            if (obj is not None):
                import types
                argoffset = 0
                arg_text = ''
                if (type(obj) in (types.ClassType,
                 types.TypeType)):

                    def find_init(obj):
                        try:
                            return obj.__init__.im_func
                        except AttributeError:
                            for base in obj.__bases__:
                                fob = find_init(base)
                                if (fob is not None):
                                    return None



                    fob = find_init(obj)
                    if (fob is None):
                        fob = lambda :None

                    else:
                        argoffset = 1
                elif (type(obj) == types.MethodType):
                    fob = obj.im_func
                    argoffset = 1
                else:
                    fob = obj
                if (type(fob) in (types.FunctionType,
                 types.LambdaType)):
                    try:
                        real_args = fob.func_code.co_varnames[argoffset:fob.func_code.co_argcount]
                        defaults = (fob.func_defaults or [])
                        defaults = list([ ('=%s' % repr(x)) for x in defaults ])
                        defaults = (([''] * (len(real_args) - len(defaults))) + defaults)
                        items = map(lambda arg, dflt:(arg + dflt)
, real_args, defaults)
                        if (fob.func_code.co_flags & 4):
                            items.append('...')
                        if (fob.func_code.co_flags & 8):
                            items.append('***')
                        arg_text = ('%s(%s)' % (title,
                        ', '.join(items)))
                    except:
                        pass
                doc = getattr(obj, '__doc__', '')
                if doc:
                    while (doc[:1] in ' \t\n'):
                        doc = doc[1:]

                    if (not arg_text):
                        arg_text = title
                    arg_text += ('\n\n' + doc.decode('utf8'))
                if arg_text:
                    try:
                        text = arg_text.decode('utf8')
                    except AttributeError:
                        text = arg_text
                    if win:
                        win.body.add((text + u'\n'))
                    else:
                        timer = e32.Ao_timer()

                        def timerhandler(timer):
                            global_msg_query(text, (u'%s - %s' % (_('Call Tip'),
                             title)))


                        timer.after(0.0, lambda :timerhandler(timer)
)
                else:
                    if win:
                        win.close()
                    ui.note((_('No additional info for "%s"') % title))
            else:
                if win:
                    win.close()
                ui.note((_('Unknown callable "%s"') % title))
            if (win and (not win.is_closed())):
                win.body.set_pos(0)
                win.open()
        else:
            ui.note(stdhelp)



    def py_calltip_scheduled(self):
        ui.schedule(self.py_calltip)



    def inline_code_highlight(self, deltapos=0, pos=None, sep=u'\u2029', inline=1):
        get = self.body.get
        pos = pos or (self.body.get_pos() - (deltapos or 0))
        startpos = get(0, pos).rfind(sep) + 1
        programm = get(startpos, pos - startpos)
        Code.highlighting(programm=programm, startpos=startpos, inline=inline)
        ui.app.body = self.body
        self.body.color = (self.typename == 'Python' and getattr(app.settings.text.fontthemes, app.settings.text.fontthemes.current_theme.lower()).fontcolor) or app.settings.python.shellfontcolor



    def get_shortcuts(cls):
        menu = ui.Menu()
        menu.append(ui.MenuItem(_('Call Tip'), method=cls.py_calltip_scheduled))
        menu.append(ui.MenuItem(_('Autocomplete'), method=cls.py_autocomplete))
        menu.append(ui.MenuItem(_('Edit Autocomplete'), target=cls.edit_autocomplete))
        menu.append(ui.MenuItem(_('Code Highlighting'), target=Code.highlighting))
        menu.append(ui.MenuItem(_('Highlight Line'), method=cls.inline_code_highlight))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

PythonModifier.py_reset_namespace()
class PythonCodeBrowserWindow(Window,
 ui.FilteredListboxModifier):
    typename = 'PythonCodeBrowser'

    def __init__(self, **kwargs):
        self.tree = pop(kwargs, 'tree')
        kwargs.setdefault('title', '__main__')
        Window.__init__(self, **kwargs)
        ui.FilteredListboxModifier.__init__(self, (_('(no match)'), u''))
        self.set_listbox(self.make_display_list(), self.click)
        self.menu = ui.Menu()
        self.menu.append(ui.MenuItem(_('Select'), target=self.select_click))
        self.menu.append(ui.MenuItem(_('Browse'), target=self.browse_click))
        self.menu.append(ui.MenuItem(_('Back'), target=self.back_click))
        self.menu.append(self.filter_menu_item)
        self.menu.append(ui.MenuItem(_('Exit'), target=self.close))
        self.keys += (ui.EKeyLeftArrow,
         ui.EKeyRightArrow)
        self.stack = []



    def make_display_list(self):
        lst = []
        for name in self.make_list():
            if self.tree[name][-1]:
                name += ' ->'
            lst.append(name)

        if (not lst):
            lst.append(_('(no data)'))
        return lst



    def _cmpfunc(self, a, b): return -(a.lower() < b.lower())



    def make_list(self):
        lst = self.tree.keys()
        lst.sort(self._cmpfunc
)
        return lst



    def key_press(self, key):
        if (key == ui.EKeyLeftArrow):
            self.back_click()
        elif (key == ui.EKeyRightArrow):
            self.browse_click()
        else:
            Window.key_press(self, key)
            ui.FilteredListboxModifier.key_press(self, key)



    def current_name(self):
        i = self.current()
        if (i < 0):
            return 
        lst = self.make_list()
        try:
            return lst[i]
        except IndexError:
            return 



    def click(self):
        name = self.current_name()
        if (name is None):
            return 
        try:
            newtree = self.tree[name][-1]
        except KeyError:
            return 
        menu = ui.Menu()
        menu.append(self.menu[0])
        if newtree:
            menu.append(self.menu[1])
        item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if (item is not None):
            item.target()



    def select_click(self):
        name = self.current_name()
        if (name is None):
            return 
        try:
            self.modal_result = self.tree[name][0]
        except KeyError:
            return 
        self.close()



    def back_click(self):
        oldtree = self.tree
        try:
            self.tree = self.stack.pop()
        except IndexError:
            return 
        pos = [ self.tree[name][-1] for name in self.make_list() ].index(oldtree)
        self.set_filter(None)
        self.filter_title = self.filter_title[:self.title.rindex(u'.')]
        self.set_list(self.make_display_list(), pos)



    def browse_click(self):
        name = self.current_name()
        if (name is None):
            return 
        try:
            newtree = self.tree[name][-1]
        except KeyError:
            return 
        if (not newtree):
            return 
        self.stack.append(self.tree)
        self.tree = newtree
        if name.endswith('()'):
            name = name[:-2]
        self.set_filter(None)
        self.filter_title += (u'.%s' % name)
        self.set_list(self.make_display_list(), 0)



class PythonFileWindow(TextFileWindow,
 PythonModifier):
    typename = 'Python'
    type_ext = '.py'

    def __init__(self, **kwargs):

        TextFileWindow.__init__(self, **kwargs)
        PythonModifier.__init__(self)
        self.control_keys += (ui.EKeySelect,)
        self.args = u''
        self.menu.insert(0, ui.MenuItem(_('Run'), target=self.run_click))
        edit_menu = self.edit_menu
        edit_menu.append(ui.MenuItem(_('Code Browser'), target=self.codebrowser_click))



    def edit_callback(self, pos, anchor):
        try:
            if anchor == 1:
                cur_sym = self.body.get(pos, 1)
                if cur_sym == u' ':
                    app.settings.python.enable_inline_highlight and self.inline_code_highlight(pos=pos, sep=u' ', inline=1)
                elif cur_sym == u'.' and app.settings.python.fasted_autocomplete:
                    prev_sym = self.body.get((pos and (pos - 1) or pos), 1)
                    if prev_sym not in u'.\u2029 ([{:' or prev_sym.isalnum() or prev_sym == u')':
                        self.body.set_input_mode(ui.ENumericInputMode)
                        self.body.set_input_mode(ui.ETextInputMode)
                        self.py_autocomplete(empty_list=False)
            self.move_callback()
        except:
            pass



    def enter_key_press(self):
        self.inline_code_highlight(deltapos=1)
        TextFileWindow.enter_key_press(self)
        self.py_insert_indent()
        ui.schedule(self.body.set_case, 2)



    def control_key_press(self, key):
        if (key == ui.EKeySelect) or (key == ui.EKeyEnter):
            self.py_autocomplete()
            self.reset_control_key()
            return False
        return TextFileWindow.control_key_press(self, key)



    def get_shortcuts(cls):
        menu = TextFileWindow.get_shortcuts()
        menu.extend(PythonModifier.get_shortcuts())
        menu.append(ui.MenuItem(_('Run'), method=cls.run_click))
        menu.append(ui.MenuItem(_('Code Browser'), method=cls.codebrowser_click))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

    def move_callback(self, localtime = time.localtime, strftime = time.strftime, time = time.time, ELowerCase=2):
        try:
            body = self.body
            text, alltext = body.get(0, body.get_pos()), body.get()
            lines = text.count(u'\u2029') + 1
            beg_line = text.rfind(u'\u2029') + 1
            """end_line = alltext.find(u'\u2029', beg_line)
            beg_prev_line = text.rfind(u'\u2029', 0, beg_line - 1) + 1
            beg_next_line = alltext.find(u'\u2029', end_line) + 1"""
            line = text[beg_line:]
            """prev_line = text[beg_prev_line:beg_line]
            next_line = alltext[beg_next_line:alltext.find(u'\u2029')]
            body.style = ui.HIGHLIGHT_STANDARD
            Code.highlighting(programm=prev_line, startpos=beg_prev_line, inline=1)
            Code.highlighting(programm=next_line, startpos=beg_next_line, inline=1)
            body.apply(beg_line, end_line - beg_line)"""
            indent = len(line) - len(line.lstrip())
            set_key_text(u'%2d)%5d' % (indent, lines), unicode(strftime('%X', localtime(time())) + '#%d' % self.shortcut_mode))
            #body.set_case(ELowerCase)
        except:
            pass



    def run_click(self):

        need_run_in_separate_process = app.settings.python.run_in_separate_process

        def endfunc(exitcode):
            lock = e32.Ao_lock()
            ui.app.exit_key_handler = lock.signal
            lock.wait()
            ui.app.exit_key_handler = self.close

        def run_code_in_separate_process(path=None):
            import time
            options = ['%s' % time.clock()]
            options.append(path)
            options = '\n'.join(options)
            file('D:\\k-shellin.txt', 'w').write(options)
            e32.start_exe(u'K-Shell_0xe9e58be4.exe', '', 1)

        def make_temp_script():
            dirpath = 'D:\\Kaapython.temp'
            if (not os.path.exists(dirpath)):
                try:
                    os.mkdir(dirpath)
                except OSError:
                    dirpath = 'D:\\'
            path = os.path.join(dirpath, self.title.encode('utf8'))
            try:
                f = file(path, 'w')
                f.write(sourcecode + '\r\n')
                f.close()
            except IOError, (errno, errstr):
                ui.note(unicode(errstr), 'error')
                return None
            return path

        TextFileWindow.store_session()
        sourcecode = self.body.get().replace(u'\u2029', u'\r\n').translate({8232: 8233,  160: 32}).encode(self.encoding)
        try:
            if (self.load()[0] == self.body.get()):
                path = self.path
            else:
                raise IOError
        except IOError:
            path = make_temp_script()
            if path is None: return
        if app.settings.python.askforargs:
            if not need_run_in_separate_process:
                menu = ui.Menu(_('Arguments'))
                if self.args:
                    menu.append(ui.MenuItem((_('Last: %s') % self.args), args=self.args))
                menu.append(ui.MenuItem(_('Edit...'), args=self.args, edit=True))
                menu.append(ui.MenuItem(_('No arguments'), args=u''))
                item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
                if (not item):
                    return 
                if getattr(item, 'edit', False):
                    args = ui.query(_('Arguments:'), 'text', item.args, ok=_('Accept'), cancel=_('Decline'))
                    if (not args):
                        return 
                    item.args = args
                self.args = item.args
                args = quote_split(self.args.encode('utf8'))
        else:
            self.args = u''
            args = []

        shell = StdIOWrapper.shell()
        if shell.is_busy():
            ui.note(_('Shell is busy!'),'error')#return 
        shell.restart()
        shell.enable_prompt(False)
        shell.lock(True)

        from linecache import checkcache
        checkcache()
        mysys = (list(sys.argv),
         list(sys.path),
         dict(sys.modules))
        sys.path.insert(0, os.path.split(path)[0])
        sys.argv = ([path] + args)
        modules = sys.modules.keys()
        
        try:
            if app.settings.python.use_debugpoints:
                sourcecode = self.body.get()
                for debugpoint in xrange(sourcecode.count('#:')):
                    pos = sourcecode.find('#:')
                    if pos == -1: break
                    indent = self.py_get_indent(sourcecode, pos)
                    sourcecode = (sourcecode[:pos] + u'\u2029' + indent + sourcecode[pos + 2:])
                sourcecode = sourcecode.translate({8232: 8233,  160: 32}).replace(u'\u2029', '\n').encode(self.encoding)
                if not need_run_in_separate_process:
                    exec sourcecode in self.py_namespace
                else:
                    path = make_temp_script()
                    if path is None: return
                    run_code_in_separate_process(path=path)
                
            else:
                if not need_run_in_separate_process:
                    execfile(path, self.py_namespace)
                else:
                    run_code_in_separate_process(path=path)
        except:
            (value, traceback_) = sys.exc_info()[1:]
            import traceback
            traceback.print_exc()
            e = traceback.extract_tb(traceback_)[-1]
            if (e[0] != path):
                s = ('(%s, line ' % os.path.split(path)[1])
                value = str(value)
                pos = value.find(s, 0)
                if (pos >= 0):
                    value = value[(pos + len(s)):]
                    self.goto_error(int(value[:value.index(')')]))
            else:
                self.goto_error(e[1], unicode(e[3]))
            del traceback_
        for m in sys.modules.keys():
            if (m not in modules):
                del sys.modules[m]

        (sys.argv, sys.path, sys.modules) = mysys
        shell.focus = True
        shell.lock(False)
        ui.screen.redraw()
        shell.enable_prompt(True)
        TextFileWindow.clear_session()

        def remove(name):
            if os.path.isdir(name):
                for item in os.listdir(name):
                    remove(os.path.join(name, item))

                os.rmdir(name)
            else:
                os.remove(name)


        remove('D:\\Kaapython.temp')



    def goto_error(self, lineno, text = None):
        (ln, pos, line,) = self.get_lines()[(lineno - 1)]
        if text:
            c = line.find(text)
            if (c > 0):
                pos += c
        self.body.set_pos(pos)



    def codebrowser_click(self):
        set_key_text(_('Options'),
         _('Exit'))
        name = os.path.splitext(self.title)[0]
        win = PythonCodeBrowserWindow(title=name, tree=self.parse_lines())
        pos = win.modal(self)
        if (pos is not None):
            self.body.set_pos(pos)



    def set_shortcuts(self):
        TextFileWindow.set_shortcuts(self)
        items = dict(self.get_shortcuts_items())
        shortcuts = (app.settings.python.fileshortcuts.mode_0, app.settings.python.fileshortcuts.mode_1,)[self.shortcut_mode]
        for (key, val,) in shortcuts.items():
            if val:
                try:
                    item = items[val]
                except KeyError:                     self.set_shortcut(key, None)
                else:
                    self.set_shortcut(key, items[val])
            else:
                self.set_shortcut(key, None)




    def parse_lines(self, lines = None):
        if (lines is None):
            lines = self.get_lines()
        flines = []
        idx = 0
        for (lnum, lpos, ln,) in lines:
            t = ln.strip()
            if (not t):
                continue
            ind = ln.find(t[0])
            flines.append((idx,
             ind,
             lpos,
             t))
            idx += 1

        end = {u'class': u'',
         u'def': u'()'}
        last = root = {}
        lev = [(0,
          root)]
        for (idx, ind, lpos, ln,) in flines:
            t = ln.split()
            if (ind < lev[-1][0]):
                if (idx > 0):
                    if (flines[(idx - 1)][-1][-1] in (u',',
                     u'\\')):
                        flines[idx] = (idx,
                         flines[(idx - 1)][1],
                         lpos,
                         ln)
                        continue
                    if (ind < flines[(idx - 1)][1]):
                        pln = flines[(idx - 1)][-1]
                        p = max(pln.find(u"'''"), pln.find(u'"""'))
                        if ((p >= 0) and (p == max(pln.rfind(u"'''"), pln.rfind(u'"""')))):
                            flines[idx] = (idx,
                             flines[(idx - 1)][1],
                             lpos,
                             ln)
                            continue
                try:
                    while (ind < lev[-1][0]):
                        lev.pop()

                except IndexError:
                    return 
            elif (ind > lev[-1][0]):
                lev.append((ind,
                 last))
            if (t[0] in end.keys()):
                tok = t[1].split(u'(')[0].split(u':')[0]
                name = (tok + end[t[0]])
                if (name in lev[-1][1]):
                    name = (u'%s:%d-%s' % (tok,
                     (lpos + ind),
                     end[t[0]]))
                last = {}
                lev[-1][1][name] = ((lpos + ind),
                 last)

        return root



class IOWindow(TextWindow):

    def __init__(self, **kwargs):
        TextWindow.__init__(self, **kwargs)
        self.control_keys += (ui.EKeyBackspace,)
        self.event = None
        self.locked = None
        self.write_buf = []

        def make_flusher(body, buf):

            def doflush():
                body.add(u''.join(buf))
                del buf[:]
                while (body.len() > 3000):
                    body.delete(0, 250)

                e32.ao_yield()


            return doflush


        self.do_flush = make_flusher(self.body, self.write_buf)
        self.flush_gate = e32.ao_callgate(self.do_flush)



    def control_key_press(self, key):
        if (key == ui.EKeyBackspace):
            if (self.locked == False):
                self.interrupt()
            self.reset_control_key()
            return True
        else:
            return TextWindow.control_key_press(self, key)



    def enter_key_press(self):
        if self.event:
            self.event.set()
            return True
        TextWindow.enter_key_press(self)
        return False



    def can_close(self):
        if self.event:
            self.input_aborted = True
            self.write('\n')
            self.event.set()
            return False
        if self.is_locked():
            if self.is_interrupted():
                if ui.query(_('Kill unresponding window by closing Kaapython?'), 'query', ok=_('Accept'), cancel=_('Decline')):
                    return True
            self.interrupt()
            return False
        return TextWindow.can_close(self)



    def close(self):
        r = TextWindow.close(self)
        if r:
            del self.flush_gate
            if self.is_interrupted():
                TextFileWindow.store_session()
                ui.screen.rootwin.shutdown()
        return r



    def lock(self, enable):
        if enable:
            self.locked = False
        else:
            self.locked = None



    def is_locked(self):
        return (self.locked is not None)



    def interrupt(self):
        self.locked = True
        notice('KeyboardInterrupt', 'error')



    def is_interrupted(self):
        return (self.locked == True)



    def readline(self, size = None):
        if (not e32.is_ui_thread()):
            raise IOError('IOWindow.readline() called from non-UI thread')
        self.input_aborted = False
        self.event = ui.Event()
        input_pos = self.body.get_pos()
        while (not self.event.isSet()):
            self.event.wait()
            if ((not self.input_aborted) and (self.body.get_pos() < input_pos)):
                ln = self.body.len()
                self.body.set_pos(ln)
                if (input_pos > ln):
                    input_pos = self.body.get_pos()
                continue
            break

        self.event = None
        if self.input_aborted:
            raise EOFError
        lst = self.body.get(input_pos).splitlines()
        if (not lst):
            lst.append(u'')
        text = (lst[0].encode('utf8', 'replace') + '\n')
        self.body.set_pos(self.body.len())
        if (size and (len(text) > size)):
            text = text[:size]
        return text



    def write(self, s):
        try:
            self.write_buf.append(unicode(s, 'latin1'))
        except UnicodeError:
            self.write_buf.append(s.decode('utf8'))
        except TypeError:
            self.write_buf.append(s)
        self.flush()



    def writelines(self, lines):
        self.write_buf += map(_unicode, lines)
        self.flush()



    def flush(self):
        if self.write_buf:
            if e32.is_ui_thread():
                self.do_flush()
            else:
                self.flush_gate()
        if self.is_interrupted():
            self.lock(True)
            raise KeyboardInterrupt



class PythonShellWindow(IOWindow, PythonModifier):
    typename = 'PythonShell'

    def __init__(self, id=None, **kwargs):
        self.shortcut_mode = 0
        set_key_text(_('Options'), u'%s#%d' % (_('Exit'), self.shortcut_mode))
        kwargs.setdefault('title', _('Python Shell') + (id and (' [%s]' % id) or ''))
        IOWindow.__init__(self, **kwargs)
        PythonModifier.__init__(self)
        self.control_keys += (ui.EKeyUpArrow,
         ui.EKeyDownArrow,
         ui.EKeySelect)
        self.menu.insert(0, ui.MenuItem(_('History'), target=self.history_click))
        self.file_menu.append(ui.MenuItem(_('Export To...'), target=self.export_click))
        self.edit_menu.append(ui.MenuItem(_('Clear'), target=self.clear_click))
        self.old_stdio = (sys.stdin,
         sys.stdout,
         sys.stderr)
        sys.stdin = sys.stdout = sys.stderr = self
        self.write(('Python %s on %s\nType "copyright", "credits" or "license" for more information.\nKaapython %s\n' % (sys.version,
         sys.platform,
         __version__)))
        self.prompt_enabled = True
        self.init_console()
        self.prompt()



    def init_console(self):
        from code import InteractiveConsole
        self.console = InteractiveConsole(locals=self.py_namespace)
        self.history = [(u'import btconsole; btconsole.main()',)]
        self.history_ptr = len(self.history)
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '> '



    def restart(self):
        PythonModifier.py_reset_namespace()
        try:
            del self.py_namespace['_']
        except KeyError:
            pass
        self.init_console()
        halfbar = ('=' * 5)
        self.move_end_of_document()
        self.write((((halfbar + ' RESTART ') + halfbar) + '\n'))
        self.prompt()



    def close(self):
        r = IOWindow.close(self)
        if r:
            sys.stdin, sys.stdout, sys.stderr = self.old_stdio
        return r



    def control_key_press(self, key):
        if (key in (ui.EKeyUpArrow,
         ui.EKeyDownArrow)):
            if (key == ui.EKeyUpArrow):
                if (self.history_ptr > 0):
                    self.history_ptr -= 1
                else:
                    ui.schedule(self.body.set_pos, self.body.get_pos())
                    return False
            elif (self.history_ptr < len(self.history)):
                self.history_ptr += 1
            else:
                ui.schedule(self.body.set_pos, self.body.get_pos())
                return False
            try:
                statement = self.history[self.history_ptr]
                try:
                    self.body.delete(self.prompt_pos)
                except SymbianError:
                    pass
                self.body.set_pos(self.prompt_pos)
                self.write('\n'.join(statement))
                ui.schedule(self.body.set_pos, self.body.get_pos())
            except IndexError:
                self.body.delete(self.prompt_pos)
                ui.schedule(self.body.set_pos, self.prompt_pos)
        elif (key == ui.EKeyBackspace):
          try:
            if (not self.is_locked()):
                pos = self.body.get_pos()
                if (pos >= self.prompt_pos):
                    if (pos == self.prompt_pos):
                        self.body.add(u' ')
                    if (self.body.len() > self.prompt_pos):

                        def clear():
                            self.body.delete(self.prompt_pos)
                            self.body.set_pos(self.prompt_pos)


                        ui.schedule(clear)
                        self.reset_control_key()
            else:
                return IOWindow.control_key_press(self, key)
          except: pass
        elif (key == ui.EKeySelect):
            self.py_autocomplete()
            self.reset_control_key()
        else:
            return IOWindow.control_key_press(self, key)
        return False



    def get_shortcuts(cls):
        menu = IOWindow.get_shortcuts()
        menu.extend(PythonModifier.get_shortcuts())
        menu.append(ui.MenuItem(_('Clear'), method=cls.clear_click))
        return menu


    get_shortcuts = classmethod(get_shortcuts)

    def calltip_click(self):
        ui.schedule(self.py_calltip)



    def enable_prompt(self, enable):
        enabled = self.prompt_enabled
        self.prompt_enabled = bool(enable)
        if ((not enabled) and enable):
            self.prompt()
        elif (enabled and (not enable)):
            self.write('\n')



    def prompt(self):
        if (not self.prompt_enabled):
            return 
        try:
            self.write(str(sys.ps1))
        except:
            pass
        self.prompt_pos = self.body.get_pos()
        self.statement = []



    def edit_callback(self, pos, anchor):
        pass



    def enter_key_press(self):
        self.inline_code_highlight(deltapos=1)
        if IOWindow.enter_key_press(self):
            return 
        if self.is_locked():
            return 
        pos = self.body.get_pos()
        if ((pos > 0) and (self.body.get((pos - 1), 1) in (u'\u2028', u'\u2029'))):
            self.body.delete((pos - 1), 1)
            pos -= 1
        if (pos < self.prompt_pos):
            self.body.set_pos(self.body.len())
            if (self.body.get_pos() < self.prompt_pos):
                self.write('\n')
                self.prompt()
                return 
            line = self.get_line_from_pos(pos=pos)[2]
            try:
                if line.startswith(str(sys.ps1)):
                    line = line[len(str(sys.ps1)):]
            except:
                pass
            self.write(line)
            return 
        if (len(self.body.get(pos).splitlines()) > 1):
            self.write('\n')
            self.py_insert_indent()
            return 
        self.body.set_pos(self.body.len())
        statement = self.body.get(self.prompt_pos).translate({160: 32}).splitlines()
        if (not statement):
            statement.append(u'')
        self.write('\n')
        statement = ([x for x in statement[:-1] if x.strip()] + statement[-1:])
        self.lock(True)
        try:
            self.console.resetbuffer()
            more = False
            for line in statement:
                if line.strip():
                    s = line
                else:
                    s = u''
                if (not self.console.push(s.encode('utf8'))):
                    break
            else:
                self.py_insert_indent()
                return 

            if (statement[0] and (self.history[-1] != tuple(statement))):
                self.history.append(tuple(statement))
            self.history_ptr = len(self.history)
            self.prompt()

        finally:
            self.lock(False)
        self.inline_code_highlight(deltapos=1)



    def apply_settings(self):
        fonttheme = _ = getattr(app.settings.text.fontthemes, app.settings.text.fontthemes.current_theme.lower())
        self.set_style(font=_.fontname, size=_.fontsize, style=_.fontstyle, antialias=_.fontantialias, color=_.fontcolor, highlight_color=_.font_highlight_color, word_wrap=_.word_wrap, screen_size=_.screen_size)
        self.set_shortcuts()



    def set_shortcuts(self):
        IOWindow.set_shortcuts(self)
        items = dict(self.get_shortcuts_items())
        shortcuts = (app.settings.python.shellshortcuts.mode_0, app.settings.python.shellshortcuts.mode_1,)[self.shortcut_mode]
        for (key, val,) in shortcuts.items():
            if val:
                try:
                    item = items[val]
                except KeyError:
                    self.set_shortcut(key, None)
                else:
                    self.set_shortcut(key, items[val])
            else:
                self.set_shortcut(key, None)




    def is_busy(self):
        if self.is_locked():
            ui.note((_('%s is busy') % self.title), 'error')
            return True
        return False



    def history_click(self):
        if self.is_busy():
            return 
        win = HistoryWindow(history=self.history, ptr=self.history_ptr)
        ptr = win.modal(self)
        if (ptr is not None):
            self.history_ptr = ptr
            statement = self.history[ptr]
            self.body.delete(self.prompt_pos)
            self.body.set_pos(self.prompt_pos)
            self.write('\n'.join(statement))



    def export_click(self):
        win = ui.FileBrowserWindow(mode=ui.fbmSave, path='PythonShell.txt', title=_('Export to'))
        path = win.modal(self)
        if (path is None):
            return 
        try:
            f = file(path, 'w')
            f.write(self.body.get().translate({8232: 8233,
             160: 32}).replace(u'\u2029', u'\r\n').encode(app.settings.file.encoding))
            f.close()
        except IOError:
            ui.note(_('Cannot export the output'), 'error')



    def clear_click(self):
        if ui.query(_('Clear the buffer?'), 'query', ok=_('Accept'), cancel=_('Decline')):
            self.body.clear()
            self.prompt()



    def move_callback(self):
        pass



    def move_beg_of_line(self, immediate = True, force = False):
        (ln, pos, line,) = self.get_line_from_pos()
        if pos <= self.prompt_pos <= (pos + len(line)):
            self.set_pos(self.prompt_pos + 1, immediate)
        else:
            IOWindow.move_beg_of_line(self, immediate, force)



class HistoryWindow(Window):
    typename = 'History'

    def __init__(self, **kwargs):
        self.history = pop(kwargs, 'history')
        ptr = pop(kwargs, 'ptr', 0)
        kwargs.setdefault('title', _('History'))
        Window.__init__(self, **kwargs)
        self.body = ui.Listbox([u''], self.select_click)
        self.body.set_list(['; '.join(filter(None, [y.strip() for y in x])).replace(':;', ':') for x in self.history], ptr)
        self.menu = ui.Menu()
        self.menu.append(ui.MenuItem(_('Select'), target=self.select_click))
        self.menu.append(ui.MenuItem(_('Exit'), target=self.close))



    def select_click(self):
        self.modal_result = self.body.current()
        self.close()



class HelpWindow(TextWindow):
    __module__ = __name__
    typename = 'HelpWindow'

    def __init__(self, **kwargs):
        text = pop(kwargs, 'text', None)
        path = pop(kwargs, 'path', None)
        head = pop(kwargs, 'head', u'')
        tail = pop(kwargs, 'tail', u'')
        kwargs.setdefault('title', _('Help'))
        TextWindow.__init__(self, bodytype=1, **kwargs)
        if (text is not None):
            try: text = unicode(text, 'utf-8', 'ignore')
            except TypeError: pass
        elif (path is not None):
            f = file(path, 'r')
            text = f.read().decode('utf8')
            f.close()
        else:
            raise TypeError("specify either 'text' or 'path' arguments")
        self.menu.insert(0, ui.MenuItem(_('Topic List'), target=self.topics_click))
        self.history = []
        self.topics = ui.Menu(_('Topic List'))
        stack = []
        lines = []
        text = ''.join((head, text, tail))
        offset = 0
        for ln in text.splitlines(True):
            if ln.startswith('$'):
                title = ln.lstrip('$')
                level = (len(ln) - len(title))
                title = title.strip()
                if (level > len(stack)):
                    stack.extend((['0'] * (level - len(stack))))
                else:
                    stack = stack[:level]
                stack[-1] = str((int(stack[-1]) + 1))
                chapter = u'.'.join(stack)
                chaptit = (u'%s. %s' % (chapter, title))
                self.topics.append(ui.MenuItem(chaptit, chapter=chapter, topic=title, pos=offset))
                ln = (u'%s\n' % chaptit)
            lines.append(ln)
            offset += len(ln)
            if ln.endswith('\r\n'):
                offset -= 1

        self.body.set(''.join(lines))
        self.body.set_pos(0)



    def add_to_history(self, pos = None):
        if (pos is None):
            pos = self.body.get_pos()
        if (not self.history):
            self.menu.insert(0, ui.MenuItem(_('Back'), target=self.back_click))
            self.update_menu()
        self.history.append(pos)



    def enter_key_press(self):
        pos = (self.body.get_pos() - 1)
        self.body.delete(pos, 1)
        (lnum, offset, ln,) = self.get_line_from_pos(pos)
        pos -= offset
        br1 = ln.rfind(u'[', 0, pos)
        br2 = ln.find(u']', pos)
        if ((br1 >= 0) and (br2 > 0)):
            link = ln[(br1 + 1):br2]
            items = self.topics.find(topic=link)
            if (not items):
                items = self.topics.find(chapter=link)
                if (not items):
                    items = self.topics.find(title=link)
            if items:
                self.add_to_history()
                self.body.set_pos(items[0].pos)



    def topics_click(self):
        item = self.topics.popup(search_field=True, left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if item:
            self.add_to_history()
            self.body.set_pos(item.pos)



    def back_click(self):
        try:
            pos = self.history.pop()
        except IndexError:
            pass
        else:
            self.body.set_pos(pos)
        if (not self.history):
            items = self.menu.find(title=_('Back'))
            if items:
                self.menu.remove(items[0])
                self.update_menu()



class StdIOWrapper(object):
    typename = 'StdIOWrapper'
    singleton = None
    no_singleton = False
    path = '...'

    def __init__(self):
        self.win = None
        StdIOWrapper.singleton = self



    def shell(cls):
        set_key_text(_('Options'),
         _('Back'))
        self = cls.singleton
        ui.app.screen = 'full'
        if not cls.no_singleton and (self.win and self.win.is_opened()):
            self.win.focus = True
            return self.win
        try:
            ui.screen.open_blank_window(title=_('Please wait...'), color=RootWindow.redraw_color)
            self.win = PythonShellWindow((cls.no_singleton and gensym()) or None)
            self.win.path = '...'
            self.win.open()
            return self.win
        except:
            import traceback
            ui.app.title = u'Fatal Error'
            ui.app.screen = 'normal'
            ui.app.focus = None
            ui.app.body = ui.Text()
            lock = e32.Ao_lock()
            ui.app.exit_key_handler = lock.signal
            ui.app.menu = [(u'Exit',
              lock.signal)]
            ui.app.body.set(unicode(''.join(traceback.format_exception(*sys.exc_info()))))
            lock.wait()
            ui.screen.redraw()
            raise 


    shell = classmethod(shell)

    def readline(self, size = None):
        return self.shell().readline(size)



    def write(self, s):
        return self.shell().write(s)



    def writelines(self, lines):
        return self.shell().writelines(lines)



class PluginsWindow(Window):
    typename = 'Plugin'

    def __init__(self, **kwargs):
        kwargs.setdefault('title', _('Plugins'))
        Window.__init__(self, **kwargs)
        self.plugins_path = os.path.join(app.path, 'plugins')
        self.body = ui.Listbox([(u'',
          u'')], self.select_click)
        self.body.bind(ui.EKeyBackspace, self.uninstall_click)
        self.menu_empty = ui.Menu()
        self.menu_empty.append(ui.MenuItem(_('Install...'), target=self.install_click))
        self.menu_empty.append(ui.MenuItem(_('Exit'), target=self.close))
        self.menu_plugins = ui.Menu()
        self.menu_plugins.append(ui.MenuItem(_('Install...'), target=self.install_click))
        self.menu_plugins.append(ui.MenuItem(_('Uninstall'), target=self.uninstall_click))
        self.menu_plugins.append(ui.MenuItem(_('Help'), target=self.help_click))
        self.menu_plugins.append(ui.MenuItem(_('Exit'), target=self.close))
        self.popup_menu_empty = ui.Menu()
        self.popup_menu_empty.append(ui.MenuItem(_('Install...'), target=self.install_click))
        self.popup_menu_plugins = ui.Menu()
        self.popup_menu_plugins.append(ui.MenuItem(_('Uninstall'), target=self.uninstall_click))
        self.popup_menu_plugins.append(ui.MenuItem(_('Help'), target=self.help_click))
        self.update()



    def update(self):
        plugins = []
        started = app.started_plugins.copy()
        if os.path.exists(self.plugins_path):
            for name in os.listdir(self.plugins_path):
                path = os.path.join(self.plugins_path, name)
                if (not os.path.isdir(path)):
                    continue
                try:
                    manifest = Manifest(os.path.join(path, 'manifest.txt'))
                except IOError:
                    continue
                plugins.append((path,
                 name,
                 manifest))
                if (started.get(name, None) == (manifest['name'],
                 manifest['version'])):
                    del started[name]

        for (name, info,) in started.items():
            plugins.append(('',
             name,
             {'name': info[0],
              'version': info[1]}))

        plugins.sort(lambda a, b:-((a[2]['name'].lower() + a[2]['version']) < (b[2]['name'].lower() + b[2]['version']))
)
        lst = []
        for (path, name, manifest,) in plugins:
            if (not path):
                descr = _('Uninstalled. Restart to stop.')
            elif (name in app.started_plugins):
                descr = _('Running.')
            else:
                descr = _('Installed. Restart Kaapython to run.')
            lst.append(((u'%s %s' % (manifest['name'],
              manifest['version'])),
             descr))

        if [ name for (path, name, manifest,) in plugins if path ]:
            self.menu = self.menu_plugins
            self.popup_menu = self.popup_menu_plugins
        else:
            self.menu = self.menu_empty
            self.popup_menu = self.popup_menu_empty
        if (not lst):
            lst.append((_('(no plugins)'),
             u''))
        self.body.set_list(lst, 0)
        self.plugins = plugins



    def select_click(self):
        item = self.popup_menu.popup(left_softkey_label=_('Accept'), right_softkey_label=_('Decline'))
        if item:
            item.target()



    def help_click(self):
        try:
            (path, name, manifest,) = self.plugins[self.body.current()]
            if (not path):
                raise IndexError
        except IndexError:
            ui.note(_('Not available'))
            return 
        bwin = ui.screen.open_blank_window(title=_('Please wait...'), color=RootWindow.redraw_color)
        path = os.path.join(path, 'help')
        helpfile = os.path.join(path, app.language.encode('utf8'))
        if (not os.path.exists(helpfile)):
            helpfile = os.path.join(path, 'English')
        try:
            win = HelpWindow(path=helpfile, title=(_('Help for %s') % manifest['name']), head=(((u'%s\n' + _('Version: %s')) + u'\n\n') % (manifest['name'],
             manifest['version'])))
            win.open()
        except IOError:
            ui.note(_('Cannot load help file'))
            bwin.close()



    def install_click(self):
        win = ui.FileBrowserWindow(title=_('Install plugin'), filter_ext='.zip')
        path = win.modal(self)
        if path:
            self.install(path)



    def uninstall_click(self):
        try:
            path = self.plugins[self.body.current()][0]
            if (not path):
                raise IndexError
        except IndexError:
            ui.note(_('Not available'))
        else:
            self.uninstall(path)



    def install(self, filename):
        import zipfile
        if (not zipfile.is_zipfile(filename)):
            ui.note(_('Not a plugin file'), 'error')
            return 
        z = zipfile.ZipFile(filename.replace('\\','/'))
        lst = [ x.lower() for x in z.namelist() ]
        if (('manifest.txt' not in lst) or (('__init__.py' not in lst) and ('__init__.pyc' not in lst))):
            ui.note(_('Not a plugin file'), 'error')
            return 
        dct = dict([ (x.lower(),
         x) for x in z.namelist() ])
        manifest = Manifest()
        manifest.parse(z.read(dct['manifest.txt']))
        for field in ('package',
         'name',
         'version',
         'kaapython-version-min',
         'kaapython-version-max'):
            if (field not in manifest):
                ui.note((_('%s field missing from manifest') % field.capitalize()))
                return 

        if (not ui.query((_('Install\n%s %s?') % (manifest['name'],
         manifest['version'])), 'query', ok=_('Accept'), cancel=_('Decline'))):
            return 
        kaapythonver = __version__.split()[0]
        if (kaapythonver < manifest['kaapython-version-min']):
            ui.note((_('Requires Kaapython in at least version %s. Your is %s.') % (manifest['kaapython-version-min'],
             kaapythonver)), 'error')
            return 
        if (kaapythonver > manifest['kaapython-version-max']):
            if (not ui.query((_('Supports Kaapython up to version %s. Your is %s. Continue?') % (manifest['kaapython-version-max'],
             kaapythonver)), 'query', ok=_('Accept'), cancel=_('Decline'))):
                return 
            manifest['kaapython-version-max'] = kaapythonver
        path = os.path.join(self.plugins_path, manifest['package'])
        if os.path.exists(path):
            try:
                old_manifest = Manifest(os.path.join(path, 'manifest.txt'))
            except IOError:
                pass
            else:
                if (not ui.query((_('Replace version %s with %s?') % (old_manifest['version'],
                 manifest['version'])), 'query', ok=_('Accept'), cancel=_('Decline'))):
                    return 
            self.uninstall(path, quiet=True)
        os.mkdir(path)

        def ensurepath(fullpath):
            (path, name,) = os.path.split(fullpath)
            if (path and (not os.path.isdir(path))):
                ensurepath(path)
            if (name and (not os.path.isdir(fullpath))):
                os.mkdir(fullpath)


        for f in z.infolist():
            p = os.path.join(path, f.filename.replace('/', '\\'))
            (pathpart, name,) = os.path.split(p)
            ensurepath(pathpart)
            if name:
                fh = file(p, 'wb')
                fh.write(z.read(f.filename))
                fh.close()

        z.close()
        manifest.save(os.path.join(path, 'manifest.txt'))
        self.update()
        ui.note((_('%s %s installed') % (manifest['name'],
         manifest['version'])), 'conf')
        ui.note(_('Restart Kaapython for the changes to take effect'))



    def uninstall(self, path, quiet = False):
        if (not quiet):
            try:
                manifest = Manifest(os.path.join(path, 'manifest.txt'))
            except IOError:
                manifest = None
            else:
                if (not ui.query((_('Uninstall\n%s %s?') % (manifest['name'],
                 manifest['version'])), 'query', ok=_('Accept'), cancel=_('Decline'))):
                    return 

        def deldir(path):
            for name in os.listdir(path):
                filename = os.path.join(path, name)
                if os.path.isdir(filename):
                    deldir(filename)
                else:
                    try:
                        os.remove(filename)
                    except OSError:
                        pass

            try:
                os.rmdir(path)
            except OSError:
                pass


        deldir(path)
        self.update()
        if (not quiet):
            if (manifest is not None):
                ui.note((_('%s %s uninstalled') % (manifest['name'],
                 manifest['version'])), 'conf')
            notice('Restart Kaapython for the changes to take effect')



class Application(object):
    typename = 'Application'

    def __init__(self):
        global py_import
        try:
            from envy import set_app_system
            self.set_app_system = set_app_system
        except ImportError:
            pass
        self.path = os.path.split(sys.argv[0])[0]
        self.sessions_path = os.path.join(self.path, 'sessions')
        if not os.path.exists(self.sessions_path):
            os.mkdir(self.sessions_path)
        self.wallpaper = Image.open(unicode(os.path.join(sys.path[0], 'wallpaper.jpg')))

        abbrevpath = os.path.join(self.path, 'abbrev.txt')
        if os.path.exists(abbrevpath):
            try:
                abbrevfile = open(abbrevpath, 'r')

                temp = []
                ignore_empty_line = True
                for line in abbrevfile:
                    line = line[:-2]
                    if (not line or line.startswith('#')) and ignore_empty_line: continue
                    if line == '=':
                        if temp: abbreviations_keys.append('\n'.join(temp))
                        del temp[:]
                        ignore_empty_line = False
                        continue
                    elif line == ';;;':
                        if temp: abbreviations_values.append('\n'.join(temp))
                        del temp[:]
                        ignore_empty_line = True
                        continue
                    else:
                        temp.append(line)
                
                abbrevfile.close()
            except:
                try: abbrevfile.close()
                except: pass


        path = os.path.join(self.path, 'lang\\kaapython')
        try:
            alllanguages = [x.decode('utf8') for x in os.listdir(path)]
        except OSError:
            alllanguages = []
        alllanguages.append(u'English')
        alllanguages.sort(lambda a, b:-(a.lower() < b.lower()))
        settings = ui.SettingsGroups(filename=os.path.join(self.path, 'settings.bin'))
        settings.append('main', ui.SettingsGroup())
        settings.main.append('language', ui.ChoiceSetting('Language', u'English', alllanguages))
        settings.try_to_load()
        self.language = settings.main.language.encode('utf8')
        if (self.language != 'English'):
            translator.try_to_load(os.path.join(path, self.language))
            path = os.path.join(self.path, 'lang\\ui')
            ui.translator.try_to_load(os.path.join(path, self.language))
        allfontthemes = [
            u'Light',
            u'Dark']
        defaultfonttheme = allfontthemes[0]
        allfonts = ui.available_text_fonts() + [
            u'annotation',
            u'title',
            u'legend',
            u'symbol',
            u'dense',
            u'normal']
        if (u'LatinBold12' in allfonts):
            defaultfont = u'LatinBold12'
        else:
            defaultfont = allfonts[0]
        allcolors = ((_('Black'), 0),
         (_('Red'), 10027008),
         (_('Green'), 34816),
         (_('Blue'), 153),
         (_('Purple'), 10027161),
         (_('Aqua'), 52479),
         (_('Olive'), 13158400),
         (_('Gray'), 8421504),
         (_('Yogurt'), 14443630),
         (_('Brick'), 16763904),
         (_('Navy'), 0x1e006e),
         (_('Silver'), 0xa0a0a0),
         (_('Lime'), 0x00ff00),
         (_('Teal'), 0x006666),
         (_('Maroon'), 0x5a0000),
         (_('Yellow'), 0xffff00),
         (_('Pink'), 16711884))
        settings = ui.SettingsGroups(filename=os.path.join(self.path, 'settings.bin'), title=_('Settings'))
        [settings.append(a, v) for a, v in (
         ('main', ui.SettingsGroup(_('Main'), _('Global settings'))),
         ('text', ui.SettingsGroup(_('Text'), _('Text windows settings'))),
         ('file', ui.SettingsGroup(_('File'), _('File windows settings'))),
         ('python', ui.SettingsGroup(_('Python'), _('Python settings'))),
         ('plugins', ui.SettingsGroup(_('Plugins'), _('Plugins settings'))),
        )]
        [settings.main.append(a, v) for a, v in (
         ('language', ui.ChoiceSetting(_('Language'), u'English', alllanguages)),
         ('wallpaper', ui.BoolSetting(_('Wallpaper'), False)),
         ('notifications', ui.BoolSetting(_('Notifications'), True)),
         ('system_app', ui.BoolSetting(_('System application'), True)),
         ('shortcuts', ui.SettingsGroup(_('Global shortcuts'))),
        )]
        [settings.main.shortcuts.append(a, v) for a, v in (
         ('mode_0', ShortcutsGroupSetting(_('Mode [%d]') % 0, RootWindow)),
         ('mode_1', ShortcutsGroupSetting(_('Mode [%d]') % 1, RootWindow)),
        )]

        settings.text.append('fontthemes', ui.SettingsGroup(_('Font themes'), _('set font theme')))
        fthemes = settings.text.fontthemes
        fthemes.append('current_theme', ui.ChoiceSetting(_('Current font theme:'), defaultfonttheme, allfontthemes))
        
        def add_new_fonttheme(name, description, size, antialias, style, skinned=False, word_wrap=True, screen_size=ui.sizNormal):
            theme = ui.SettingsGroup(_(name.capitalize()), description)
            theme.append('fontname', ui.ChoiceSetting(_('Font name'), defaultfont, allfonts))
            theme.append('fontsize', ui.IntegerSetting(_('Font size'), size))
            theme.append('fontantialias', ui.BoolSetting(_('Font anti-aliasing'), antialias))
            theme.append('fontstyle', ui.SettingsGroup(_('Font style'), _('Set font style')))
            theme.fontstyle.append('fontbold', ui.BoolSetting(_('Font bold'), style[0]))
            theme.fontstyle.append('fontitalic', ui.BoolSetting(_('Font italic'), style[1]))
            theme.fontstyle.append('fontunderline', ui.BoolSetting(_('Font underline'), style[2]))
            theme.fontstyle.append('fontstrikethrough', ui.BoolSetting(_('Font strikethrough'), style[3]))
            theme.fontstyle.append('fonthighlightstandard', ui.BoolSetting(_('Highlight standard'), style[4]))
            theme.fontstyle.append('fonthighlightrounded', ui.BoolSetting(_('Highlight rounded'), style[5]))
            theme.fontstyle.append('fonthighlightshadow', ui.BoolSetting(_('Highlight shadow'), style[6]))
            theme.append('fontcolor', ui.ChoiceValueSetting(_('Font color'), style[7], allcolors))
            theme.append('font_highlight_color', ui.StringSetting(_('Font highlight color'), style[8]))
            theme.append('skinned', ui.BoolSetting(_('Skinned body'), skinned))
            theme.append('word_wrap', ui.BoolSetting(_('Word wrap'), word_wrap))
            allscreens = ((_(ui.sizNormal), ui.sizNormal),
             (_(ui.sizLarge), ui.sizLarge),
             (_(ui.sizFull), ui.sizFull),
            )
            theme.append('screen_size', ui.ChoiceValueSetting(_('Screen size'), ui.sizNormal, allscreens))
            fthemes.append(name, theme)
        
        add_new_fonttheme('light', 'Dayly theme', size=13, antialias=True, style=(True, False, False, False, False, False, True, 0x5a0000, u'(255, 202, 255)'), word_wrap=True)
        add_new_fonttheme('dark', 'Nightly theme', size=15, antialias=True, style=(True, False, False, False, False, False, True, 0x00009a, u'(255, 255, 222)'), skinned=True, word_wrap=True)
        [settings.text.append(a, v) for a, v in (
         ('cursors_step', ui.BoolSetting(_('Step of Cursor'), False)),
         ('pagesizefull', ui.IntegerSetting(_('Page size (full screen)'), 11, vmin=1, vmax=64)),
         ('pagesizeport', ui.IntegerSetting(_('Page size (portrait)'), 8, vmin=1, vmax=64)),
         ('pagesizeland', ui.IntegerSetting(_('Page size (landscape)'), 9, vmin=1, vmax=64)),
         ('shortcuts', ui.SettingsGroup(_('Text shortcuts'))),
        )]
        [settings.text.shortcuts.append(a, v) for a, v in (
         ('mode_0', ShortcutsGroupSetting(_('Mode [%d]') % 0, TextWindow, True)),
         ('mode_1', ShortcutsGroupSetting(_('Mode [%d]') % 1, TextWindow, True)),
        )]

        [settings.file.append(a, v) for a, v in (
         ('encoding', ui.ChoiceSetting(_('Default encoding'), 'utf8', ('ascii',
         'latin-1',
         'utf8',
         'utf-16',
         'windows_1251',
         'cp866',
         'iso8859_5',
         'koi8-r',
         'koi8-u',
         'utf-7',
         'zlib',
         'zip',
         'hex',
         'base64',
         'unicodebigunmarked',
         'unicodelittleunmarked',
         ))),
         ('autosave', ui.ChoiceValueSetting(_('Autosave'), 0, ((_('Off'),
          0),
         ((_('%d sec') % 30),
          30),
         ((_('%d min') % 1),
          60),
         ((_('%d min') % 2),
          120),
         ((_('%d min') % 5),
          300),
         ((_('%d min') % 10),
          600)))),
         ('use_multisessions', ui.BoolSetting(_('Use multisessions'), False)),
         ('shortcuts', ui.SettingsGroup(_('Text file shortcuts'))),
        )]
        [settings.file.shortcuts.append(a, v) for a, v in (
         ('mode_0', ShortcutsGroupSetting(_('Mode [%d]') % 0, TextFileWindow, True)),
         ('mode_1', ShortcutsGroupSetting(_('Mode [%d]') % 1, TextFileWindow, True)),
        )]

        settings.python.append('highlighting', ui.SettingsGroup(_('Code Highlighting'), _('Edit highlighting')))
        [settings.python.highlighting.append(a, v) for a, v in (
         ('keyword', ui.StringSetting(_('keyword'), unicode(TokenColor.keyword))),
         ('module', ui.StringSetting(_('module'), unicode(TokenColor.module))),
         ('builtin', ui.StringSetting(_('builtin'), unicode(TokenColor.builtin))),
         ('number', ui.StringSetting(_('number'), unicode(TokenColor.number))),
         ('string', ui.StringSetting(_('string'), unicode(TokenColor.string))),
         ('name', ui.StringSetting(_('name'), unicode(TokenColor.name))),
         ('operation', ui.StringSetting(_('operation'), unicode(TokenColor.operation))),
         ('comment', ui.StringSetting(_('comment'), unicode(TokenColor.comment))),
         ('bracket', ui.StringSetting(_('bracket'), unicode(TokenColor.bracket))),
         ('percent', ui.StringSetting(_('percent'), unicode(TokenColor.percent))),
         ('self_', ui.StringSetting(_('self'), unicode(TokenColor.self_))),
         ('cls_', ui.StringSetting(_('cls'), unicode(TokenColor.cls_))),
        )]
        [settings.python.append(a, v) for a, v in (
         ('enable_inline_highlight', ui.BoolSetting(_('Inline highlighting'), True)),
         ('include_python_api', ui.BoolSetting(_('Include Python API'), False)),
         ('fasted_autocomplete', ui.BoolSetting(_('Fasted autocomplete'), False)),
         ('run_in_new_shellwindow', ui.BoolSetting(_('Run in new shellwindow'), False)),
         ('run_in_separate_process', ui.BoolSetting(_('Run in separate process'), False)),
         ('askforargs', ui.BoolSetting(_('Ask for arguments'), False)),
         ('use_debugpoints', ui.BoolSetting(_('Processing debugpoints'), False)),
         ('shellfontcolor', ui.ChoiceValueSetting(_('Shell font color'), 34816, allcolors)),
         ('indentsize', ui.IntegerSetting(_('Indentation size'), 4, vmin=1, vmax=8)),
         ('fileshortcuts', ui.SettingsGroup(_('Python file shortcuts'))),
        )]
        [settings.python.fileshortcuts.append(a, v) for a, v in (
         ('mode_0', ShortcutsGroupSetting(_('Mode [%d]') % 0, PythonFileWindow, True)),
         ('mode_1', ShortcutsGroupSetting(_('Mode [%d]') % 1, PythonFileWindow, True)),
        )]

        settings.python.append('shellshortcuts', ui.SettingsGroup(_('Python shell shortcuts')))
        [settings.python.shellshortcuts.append(a, v) for a, v in (
         ('mode_0', ShortcutsGroupSetting(_('Mode [%d]') % 0, PythonShellWindow, True)),
         ('mode_1', ShortcutsGroupSetting(_('Mode [%d]') % 1, PythonShellWindow, True)),
        )]

        self.settings = settings
        if (e32.s60_version_info >= (3, 0)):
            path = os.path.join(os.path.splitdrive(self.path)[0], '\\resource\\apps\\kaapython_file_browser_icons.mif')
        elif (e32.s60_version_info >= (2, 8)):
            path = os.path.join(self.path, 'kaapython_file_browser_icons.mif')
        else:
            path = None
        if ((path is None) or (not os.path.exists(path))):
            path = os.path.join(self.path, 'kaapython_file_browser_icons.mbm')
        ui.FileBrowserWindow.icons_path = path
        ui.FileBrowserWindow.settings_path = os.path.join(self.path, 'kaapython_file_browser_settings.bin')
        map(ui.FileBrowserWindow.add_link, ('c:\\data\\python', 'c:\\resource', 'c:\\projects', 'c:\\python', 'e:\\projects', 'e:\\python'))
        ui.FileBrowserWindow.add_link(os.path.join(self.path, 'templates'), _('Templates'))
        ui.FileBrowserWindow.add_link(abbrevpath, _('Abbreviations'))

        if (e32.s60_version_info < (3, 0)):
            if (not ui.FileBrowserWindow.add_link('E:\\System\\Apps\\Python', _('Python Shell'))):
                ui.FileBrowserWindow.add_link('C:\\System\\Apps\\Python', _('Python Shell'))
        TextFileWindow.session.set_filename(os.path.join(self.path, 'sessions\\session.bin'))
        self.browser_win = self.help_win = self.plugins_win = None
        self.unnamed_count = 1
        self.started_plugins = {}



        def kaapython_import(name, globals = None, locals = None, fromlist = None):
            mod = py_import(name, globals, locals, fromlist)
            try:
                path = mod.__file__.lower()
            except AttributeError:
                pass
            else:
                for win in ui.screen.find_windows(PythonFileWindow):
                    try:
                        if (win.path.lower() == path):
                            win.save()
                            return reload(mod)
                    except AttributeError:
                        pass

            return mod


        import __builtin__

        py_import = __builtin__.__import__
        __builtin__.__import__ = kaapython_import
        sys.exitfunc = lambda: (e32.ao_yield(), e32.ao_yield(), e32.ao_yield(), ui.schedule(.1, appswitch.switch_to_bg, u'Kaapython'), ui.schedule(3, TextFileWindow.store_session))



    def start(self):
        for path in ('C:\\Python\\lib', 'E:\\Python\\lib'):
            if os.path.exists(path):
                sys.path.append(path)

        self.settings.try_to_load()
        self.apply_settings()
        rootwin = RootWindow()
        rootwin.open()

        def schedule():
            file_menu = ui.Menu(_(add_tabchar_to('File')))
            file_menu.append(ui.MenuItem(_('New'), target=self.new_click))
            file_menu.append(ui.MenuItem(_('Open...'), target=self.open_click))
            self.file_menu = file_menu
            main_menu = ui.Menu(_('Options'))
            main_menu.append(ui.MenuItem(_(add_tabchar_to('File')), target=ui.run_menu_item(file_menu)))
            self.windows_menu = windows_menu = ui.Menu()
            main_menu.append(ui.MenuItem(_(add_tabchar_to('Windows')), target=lambda: len(ui.screen.windows) > 1 and ui.screen._Screen__selector()))
            python_menu = ui.Menu(_(add_tabchar_to('Python')))
            python_menu.append(ui.MenuItem(_('Python Shell'), target=StdIOWrapper.shell))
            python_menu.append(ui.MenuItem(_('Run Script...'), target=self.runscript_click))
            python_menu.append(ui.MenuItem(_('Compile Script...'), target=self.compilescript_click))
            python_menu.append(ui.MenuItem(_('Decompile Script...'), target=self.decompilescript_click))
            self.python_menu = python_menu
            main_menu.append(ui.MenuItem(_(add_tabchar_to('Python')), target=ui.run_menu_item(python_menu)))
            tools_menu = ui.Menu(_(add_tabchar_to('Tools')))
            tools_menu.append(ui.MenuItem(_('Settings'), target=self.settings_click))
            tools_menu.append(ui.MenuItem(_('Sessions'), target=self.sessions_click))
            tools_menu.append(ui.MenuItem(_('Plugins'), target=self.plugins_click))
            tools_menu.append(ui.MenuItem(_('Help'), target=self.help_click))
            tools_menu.append(ui.MenuItem(_('Orientation'), target=self.orientation_click))
            self.tools_menu = tools_menu
            main_menu.append(ui.MenuItem(_(add_tabchar_to('Tools')), target=ui.run_menu_item(tools_menu)))
            main_menu.append(ui.MenuItem(_('In this version...'), target=in_this_version))
            main_menu.append(ui.MenuItem(_('Exit'), target=self.exit_click))
            rootwin.menu = main_menu
            ui.schedule(self.start_plugins)
            self.restore_session()
            ui.menu_key_handler = TextWindow.set_selection_text
            ui.exit_key_handler = TextWindow.paste_text
            
            if len(ui.screen.windows) == 1:
                return ui.schedule(self.new_file, PythonFileWindow)

        return ui.schedule(schedule)



    def restore_session(self, session=None):
        session = (session or TextFileWindow.session)
        session.try_to_load()
        windows = session.windows
        if (windows and ui.query(_('Restore previous session?'), 'query', ok=_('Accept'), cancel=_('Decline'))):
            def load_window():
                    if (text is None):
                        win = self.load_file(path)
                        if win:
                            win.body.set_pos(pos)
                    else:
                        ext = os.path.splitext(path)[1].lower()
                        try:
                            klass = file_windows_types[[ x.type_ext.lower() for x, y in file_windows_types ].index(ext)][0]
                        except ValueError:
                            klass = TextFileWindow
                        ui.screen.open_blank_window(title=_('Please wait...'), color=RootWindow.redraw_color)
                        win = klass(title=os.path.split(path)[1].decode('utf8'))
                        if win:
                            win.body.set(text)
                            win.body.set_pos(pos)
                            win.encoding = encoding

                            if os.path.split(path)[0]:
                                win.path = path
                                win.fixed_encoding = True
                            else:
                                win.fixed_encoding = False
                            win.bookmarks.extend(bookmarks)
                            win.open()
                            try: win.size = size
                            except: pass
            try:
                for (path, text, encoding, pos, bookmarks, size) in windows:
                    load_window()
            except ValueError:
                for (path, text, encoding, pos, bookmarks,) in windows:
                    load_window()

        del windows[:]
        if session is not TextFileWindow.session:
            session.set_filename(TextFileWindow.session.filename)
            TextFileWindow.session = session
        try:
            TextFileWindow.session.filename = os.path.join(self.sessions_path, str(time.strftime('%X %x', time.localtime(time.time()))).replace(':', "'"))
            try:
                TextFileWindow.session.save()
            except IOError:
                ui.note(_('Cannot update sessions file'), 'error')
        finally:
            TextFileWindow.session.filename = os.path.join(self.sessions_path, 'session.bin')
        try:
                TextFileWindow.session.save()
        except IOError:
            ui.note(_('Cannot update sessions file'), 'error')


    def start_plugins(self):
        plugins_path = os.path.join(self.path, 'plugins')
        self.started_plugins = {}
        allkeys = self.settings.allkeys()
        for name in os.listdir(plugins_path):
            path = os.path.join(plugins_path, name)
            if (not os.path.isdir(path)):
                continue
            try:
                manifest = Manifest(os.path.join(path, 'manifest.txt'))
                kaapythonver = __version__.split()[0]
                if (manifest['kaapython-version-min'] > kaapythonver):
                    ui.note((_('%s plugin requires Kaapython in at least version %s. Your is %s. Skipping.') % (manifest['name'],
                     manifest['kaapython-version-min'],
                     kaapythonver)), 'error')
                    continue
                if (kaapythonver > manifest['kaapython-version-max']):
                    if (not ui.query((_('%s plugin supports Kaapython up to version %s. Your is %s. Run?') % (manifest['name'],
                     manifest['kaapython-version-max'],
                     kaapythonver)), 'query', ok=_('Accept'), cancel=_('Decline'))):
                        continue
                    manifest['kaapython-version-max'] = kaapythonver
                    manifest.save(os.path.join(path, 'manifest.txt'))
                __import__(('plugins.%s' % name))
                self.started_plugins[name] = (manifest['name'],
                 manifest['version'])
            except:
                from traceback import print_exc
                print_exc()
                ui.note((_('Starting "%s" plugin failed, skipping') % name.decode('utf8')), 'error')

        if (self.settings.allkeys() != allkeys):
            self.settings.try_to_load()
            self.apply_settings()
        ui.screen.redraw()



    def exit_click(self):
        if ui.screen.find_windows(TextFileWindow):
            menu = ui.Menu(_('Exit'))
            menu.append(ui.MenuItem(_('Store the session'), store=True))
            menu.append(ui.MenuItem(_('Close all files'), store=False))
            item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
            if (item is None):
                return
            TextFileWindow.store_session()
            sessions_path = self.sessions_path
            for s in os.listdir(sessions_path):
                path = os.path.join(sessions_path, s)
                if os.stat(path)[6] == 17:
                    os.remove(path)
            if item.store:
                ui.screen.rootwin.shutdown()
                return 
        ui.screen.rootwin.close()



    def new_file(self, klass):
        title = ('Unnamed%d%s' % (self.unnamed_count, klass.type_ext))
        self.unnamed_count += 1
        win = klass(title=title)
        win.open()
        return win



    def _select_session(self):
        def sorted(x, y):
            # 07'43'06 Fri Jan 14 2011
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            dataX = x.split(' ')
            dataY = y.split(' ')
            hourX, minutesX, secondsX = map(int, dataX[0].split("'"))
            yearX = dataX[-1]
            hourY, minutesY, secondsY = map(int, dataY[0].split("'"))
            yearY = dataY[-1]
            monthX = months.index(dataX[2])
            monthY = months.index(dataY[2])
            if yearY > yearX: return 1
            elif yearX > yearY: return -1
            if monthY > monthX: return 1
            elif monthX > monthY: return -1
            if dataY[3] > dataX[3]: return 1
            elif dataX[3] > dataY[3]: return -1
            if hourY > hourX: return 1
            elif hourX > hourY: return -1
            if minutesY > minutesX: return 1
            elif minutesX > minutesY: return -1
            if secondsY > secondsX: return 1
            elif secondsX > secondsY: return -1
            return 0

        sessions = os.listdir(self.sessions_path)
        sessions.remove('session.bin')
        sessions.sort(sorted)
        title = ui.app.title
        ui.app.title = _('Load session...')
        index = ui.selection_list(map(unicode, sessions), 1)
        ui.app.title = title
        if index is not None:
            path = sessions[index]
            session = ui.SettingsGroup()
            session.append('windows', ui.Setting('', []))
            session.set_filename(os.path.join(self.sessions_path, path))
            return path, session
        return None, None



    def sessions_click(self):
        path, session = self._select_session()
        if path is None: return
        self.restore_session(session)
        TextFileWindow.store_session()





    def settings_click(self):
        set_key_text(_('Options'),
         _('Exit'))
        if self.settings.edit():
            self.settings.save()
            self.apply_settings()



    def apply_settings(self):
        GlobalWindowModifier.update_settings()
        if (self.language != self.settings.main.language.encode('utf8')):
            ui.note(_('Restart Kaapython for the changes to take effect'))



    def plugins_click(self):
        if (self.plugins_win and self.plugins_win.is_opened()):
            self.plugins_win.focus = True
            return 
        self.plugins_win = PluginsWindow()
        self.plugins_win.open()



    def help_click(self):
        if (self.help_win and self.help_win.is_opened()):
            self.help_win.focus = True
            return 
        bwin = ui.screen.open_blank_window(title=_('Please wait...'), color=RootWindow.redraw_color)
        path = os.path.join(self.path, 'lang\\help')
        helpfile = os.path.join(path, self.language)
        if (not os.path.exists(helpfile)):
            helpfile = os.path.join(path, 'English')
        try:
            self.help_win = HelpWindow(path=helpfile, head=(u'Kaapython - Python IDE\nVersion: %s\n\nCopyright \xa9 2010\nVirtuos86\n<virtuos86@yandex.ru>\n\nCopyright \xa9 2007-2008\nArkadiusz Wahlig\n<arkadiusz.wahlig@gmail.com>\n\n' % __version__))
            self.help_win.open()
        except IOError:
            ui.note(_('Cannot load help file'), 'error')
            bwin.close()



    def new_click(self):
        menu = ui.Menu(_('New'))
        for klass, description in file_windows_types:
            menu.append(ui.MenuItem(klass.typename, klass=klass))

        item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if item:
            self.new_file(item.klass)



    def get_path_from_user(self, title):
        if self.browser_win:
            ui.note(_('File browser already in use'), 'error')
            return 
        set_key_text(_('Options'),
         _('Back'))
        self.browser_win = ui.FileBrowserWindow(title=_(title))
        path = self.browser_win.modal()
        self.browser_win = None
        return path



    def open_click(self):
        path = self.get_path_from_user('Open file')
        if (not path):
            return 
        self.load_file(path)



    def load_file(self, path):
        for win in ui.screen.find_windows(TextFileWindow):
            if (win.path == path):
                win.focus = True
                return 

        ext = os.path.splitext(path)[1].lower()
        try:
            klass = file_windows_types[[ x.type_ext.lower() for x, y in file_windows_types ].index(ext)][0]
        except ValueError:
            klass = TextFileWindow
        wwin = ui.screen.open_blank_window(title=_('Please wait...'), color=RootWindow.redraw_color)
        try:
            win = klass(path=path)
            win.open()
        except IOError:
            win = None
            ui.note((_('Cannot load %s file') % os.path.split(path)[1]), 'error')
            wwin.close()
        return win



    def compilescript_click(self):
        path = self.get_path_from_user('Compile Script...')
        if (not path):
            return
        from py_compile import compile
        compile(path)
        notice(_('Action complete!'))



    def decompilescript_click(self):
        global decompile
        path = self.get_path_from_user('Decompile Script...')
        if (not path):
            return
        if not decompile:
            from py_decompile import decompile as dec
            decompile = dec
        decompile(path)
        notice(_('Action complete!'))



    def runscript_click(self):
        if self.browser_win:
            ui.note(_('File browser already in use'), 'error')
            return 
        set_key_text(_('Options'), _('Back'))
        self.browser_win = ui.FileBrowserWindow(title=_('Run script'))
        path = self.browser_win.modal()
        self.browser_win = None
        if (not path):
            return 
        if self.settings.python.askforargs:
            menu = ui.Menu(_('Arguments'))
            menu.append(ui.MenuItem(_('Edit...')))
            menu.append(ui.MenuItem(_('No arguments')))
            item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
            if (not item):
                return
            if (item.name == 'edit'):
                args = ui.query(_('Arguments:'), 'text', ok=_('Accept'), cancel=_('Decline'))
                if (not args):
                    return 
            else:
                args = u''
            args = quote_split(args.encode('utf8'))
        else:
            args = []
        shell = StdIOWrapper.shell()
        if shell.is_busy():
            return 
        shell.restart()
        shell.enable_prompt(False)
        shell.lock(True)
        from linecache import checkcache
        checkcache()
        TextFileWindow.store_session()
        mysys = (list(sys.argv),
         list(sys.path))
        sys.path.insert(0, os.path.split(path)[0])
        sys.argv = ([path] + args)
        modules = sys.modules.keys()
        try:
            execfile(path, shell.py_namespace)

        finally:
            for m in sys.modules.keys():
                if (m not in modules):
                    del sys.modules[m]

            (sys.argv, sys.path,) = mysys
            TextFileWindow.clear_session()
            shell.focus = True
            shell.lock(False)
            ui.screen.redraw()
            shell.enable_prompt(True)




    def orientation_click(self):
        win = ui.screen.focused_window()
        ori = newori = win.orientation
        if (ori == ui.oriAutomatic):
            (w, h,) = ui.layout(ui.EApplicationWindow)[0]
            if (w > h):
                newori = ui.oriPortrait
            else:
                newori = ui.oriLandscape
        else:
            win.orientation = ui.oriAutomatic
            (w, h,) = ui.layout(ui.EApplicationWindow)[0]
            if (ori == ui.oriPortrait):
                if (w > h):
                    newori = ui.oriAutomatic
                else:
                    newori = ui.oriLandscape
            elif (ori == ui.oriLandscape):
                if (w > h):
                    newori = ui.oriPortrait
                else:
                    newori = ui.oriAutomatic
        if (newori != ori):
            for win in ui.screen.find_windows():
                win.orientation = newori
                if isinstance(win, TextWindow):
                    win.reset_caret()




class ShortcutsGroupSetting(ui.GroupSetting):

    def __init__(self, title, klass, none_item = False):
        ui.GroupSetting.__init__(self, title)
        self.klass = klass
        self.none_item = none_item
        self.info = _('(more options)')



    def set(self, value):
        self.value.clear()
        for (key, val,) in value.items():
            setting = self.get_new((_('Green-%s') % unichr(key)), val)
            if (setting is not None):
                self.value.append(key, setting)

        self.value.sort()
        self.original = self.value.items()



    def to_item(self, setting):
        if (setting is not None):
            return (unicode(setting.title), unicode(setting))
        else:
            return (_('(no shortcuts)'), u'')



    def get_new(self, title, value = ''):
        choices = [(item.title, name) for (name, item,) in self.klass.get_shortcuts_items()]
        if self.none_item:
            choices.insert(0, (_('(none)'), ''))
        return ui.ChoiceValueSetting(title, value, choices)



    def get_new_name(self):
        menu = ui.Menu(_('Choose key'))
        for ckey in '1234567890*#':
            menu.append(ui.MenuItem(ckey))

        menu.append(ui.MenuItem(_('Custom...')))
        item = menu.popup(left_softkey_label=_("Accept"), right_softkey_label=_("Decline"))
        if (item is not None):
            if (item is menu[-1]):
                ckey = u''
                while True:
                    ckey = ui.query(_('Choose key'), 'text', ckey, ok=_('Accept'), cancel=_('Decline'))
                    if (ckey is None):
                        return 
                    if (len(ckey) == 1):
                        break
                    ui.note(_('Enter one key only'))

            else:
                ckey = item.title
            ckey = ckey[0].lower()
            key = ord(ckey)
            return (key, (_('Green-%s') % ckey))



    def __str__(self):
        return str(self.info)



    def __unicode__(self):
        return unicode(self.info)



class Manifest(object):

    def __init__(self, filename = None):
        self.fields = {}
        if (filename is not None):
            self.load(filename)



    def parse(self, data):
        lines = data.decode('utf8').splitlines()
        lines.reverse()
        self.fields = {}
        while True:
            try:
                ln = lines.pop()
            except IndexError:
                break
            try:
                p = ln.index(u':')
            except ValueError:
                raise ValueError('mangled manifest file')
            name = ln[:p].strip().title()
            value = []
            vln = ln[(p + 1):].strip()
            while vln.endswith(u'\\'):
                value.append(vln[:-1].strip())
                try:
                    ln = lines.pop()
                except IndexError:
                    break
                vln = ln.strip()
            else:
                value.append(vln)

            if (name in self.fields):
                raise ValueError('manifest field defined twice')
            self.fields[name] = u'\r\n'.join(value)




    def dump(self):
        lines = []
        for (name, value,) in self.fields.items():
            lines.append((u'%s: %s\r\n' % (name.title(),
             '\\\r\n'.join(value.split('\n')))))

        return ''.join(lines).encode('utf8')



    def load(self, filename):
        f = open(filename, 'r')
        try:
            self.parse(f.read())

        finally:
            f.close()




    def save(self, filename):
        f = open(filename, 'w')
        try:
            f.write(self.dump())

        finally:
            f.close()




    def get(self, name, default = None):
        return self.fields.get(name.title(), default)



    def keys(self):
        return self.fields.keys()



    def items(self):
        return self.fields.items()



    def values(self):
        return self.fields.values()



    def clear(self):
        self.fields = {}



    def __getitem__(self, name):
        return self.fields[name.title()]



    def __setitem__(self, name, value):
        self.fields[name.title()] = value



    def __delitem__(self, name):
        del self.fields[name.title()]



    def __len__(self):
        return len(self.fields)



    def __contains__(self, name):
        return (name.title() in self.fields)




def quote_split(s):
    s += ' '
    ret = []
    for x in s.split('"'):
        if x:
            i = s.index(x)
        else:
            i = (s.index('""') + 1)
        try:
            if ((s[(i - 1)] == '"') and (s[(i + len(x))] == '"')):
                ret.append(x)
                s = (s[:(i - 1)] + s[((i + len(x)) + 1):])
                continue
        except IndexError:
            pass
        ret += x.split()
        s = (s[:i] + s[(i + len(x)):])

    return ret



def repattr(obj, name, value):
    """Sets an attribute of a class/object. Returns the old value.
    """
    old = getattr(obj, name)
    setattr(obj, name, value)
    return old



def get_plugin_translator(plugin_path):
    """Returns a new ui.Translator object for plugin specified
    by plugin_path argument. If a file is passed, the last
    path component is removed.
    """
    if os.path.isfile(plugin_path):
        plugin_path = os.path.split(plugin_path)[0]
    path = os.path.join(plugin_path, ('lang\\' + app.language))
    trans = ui.Translator()
    trans.try_to_load(path)
    return trans


translator = _ = ui.Translator()
file_windows_types = [(PythonFileWindow, u'create Python script (*.py)'),
 (TextFileWindow, u'create text file (*.txt)')]
app = Application()

def in_this_version():
    features = HelpWindow(title=_('In this version...'), head=u'New in this version:', text=__features__)
    features.open()
