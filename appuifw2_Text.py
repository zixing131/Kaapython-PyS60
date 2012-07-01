# This section of the module "appuifw2.py" is needed to save RAM memory.

import e32
import appuifw
from appuifw import *
if (e32.s60_version_info >= (3,
 0)):
    import imp
    _appuifw2 = imp.load_dynamic('_appuifw2', '%s:\\sys\\bin\\_appuifw2.pyd' % appuifw.__file__[0])
    del imp
else:
    import _appuifw2


EAknSoftkeyOk = -2
EAknSoftkeyBack = 3001
EAknSoftkeyCancel = -1

_popup_menu= popup_menu

def popup_menu(data, title=None, left_softkey_label=None, right_softkey_label=None):
    if ((left_softkey_label is not None) or (right_softkey_label is not None)):

        def set_ok_cancel(ok, cancel):
            if (not abort):
                if (ok is not None):
                    try:
                        _appuifw2.command_text(EAknSoftkeyOk, ok)
                    except SymbianError:
                        pass
                if (cancel is not None):
                    try:
                        _appuifw2.command_text(EAknSoftkeyBack, cancel)
                    except SymbianError:
                        pass


        abort = False
        e32.ao_sleep(0, lambda: set_ok_cancel(left_softkey_label, right_softkey_label))
    try:
        if title is not None:
            return _popup_menu(data, title)
        else:
            return _popup_menu(data)
    finally:
        abort = True


_query = query

def query(label, type, initial_value=None, ok=None, cancel=None):
    if ((ok is not None) or (cancel is not None)):

        def set_ok_cancel(ok, cancel):
            if (not abort):
                if (ok is not None):
                    try:
                        _appuifw2.command_text(EAknSoftkeyOk, ok)
                    except SymbianError:
                        pass
                if (cancel is not None):
                    try:
                        _appuifw2.command_text(EAknSoftkeyCancel, cancel)
                    except SymbianError:
                        pass


        abort = False
        e32.ao_sleep(0, lambda: set_ok_cancel(ok, cancel))
    try:
        return _query(label, type, initial_value)

    finally:
        abort = True




class Text(object):
    __module__ = __name__

    def __init__(self, text = u'', move_callback = None, edit_callback = None, skinned = False, scrollbar = False, word_wrap = True, t9 = True, indicator = True, fixed_case = False, flags = 37128, editor_flags = 0):
        if (not word_wrap):
            flags |= 32
        self._uicontrolapi = _appuifw2.Text2_create(flags, scrollbar, skinned, move_callback, edit_callback)
        if text:
            self.set(text)
            self.set_pos(0)
        if (not t9):
            editor_flags |= 2
        if (not indicator):
            editor_flags |= 4
        if fixed_case:
            editor_flags |= 1
        if editor_flags:
            _appuifw2.Text2_set_editor_flags(self._uicontrolapi, editor_flags)



    def add(self, text):
        _appuifw2.Text2_add_text(self._uicontrolapi, text)



    def insert(self, pos, text):
        _appuifw2.Text2_insert_text(self._uicontrolapi, pos, text)



    def bind(self, event_code, callback):
        _appuifw2.bind(self._uicontrolapi, event_code, callback)



    def clear(self):
        _appuifw2.Text2_clear_text(self._uicontrolapi)



    def delete(self, pos = 0, length = -1):
        _appuifw2.Text2_delete_text(self._uicontrolapi, pos, length)



    def apply(self, pos = 0, length = -1):
        _appuifw2.Text2_apply(self._uicontrolapi, pos, length)



    def get_pos(self):
        return _appuifw2.Text2_get_pos(self._uicontrolapi)



    def set_pos(self, cursor_pos, select = False):
        _appuifw2.Text2_set_pos(self._uicontrolapi, cursor_pos, select)



    def len(self):
        return _appuifw2.Text2_text_length(self._uicontrolapi)



    def get(self, pos = 0, length = -1):
        return _appuifw2.Text2_get_text(self._uicontrolapi, pos, length)



    def set(self, text):
        _appuifw2.Text2_set_text(self._uicontrolapi, text)



    def __len__(self):
        return _appuifw2.Text2_text_length(self._uicontrolapi)



    def __getitem__(self, i):
        return _appuifw2.Text2_get_text(self._uicontrolapi, i, 1)



    def __setitem__(self, i, value):
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, len(value))
        _appuifw2.Text2_insert_text(self._uicontrolapi, i, value)



    def __delitem__(self, i):
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, 1)



    def __getslice__(self, i, j):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        return _appuifw2.Text2_get_text(self._uicontrolapi, i, (j - i))



    def __setslice__(self, i, j, value):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        _appuifw2.Text2_delete_text(self._uicontrolapi, i, (j - i))
        _appuifw2.Text2_insert_text(self._uicontrolapi, i, value)



    def __delslice__(self, i, j):
        ln = len(self)
        i = min(ln, max(0, i))
        j = min(ln, max(i, j))
        return _appuifw2.Text2_delete_text(self._uicontrolapi, i, (j - i))



    def get_selection(self):
        (pos, anchor,) = _appuifw2.Text2_get_selection(self._uicontrolapi)
        i = min(pos, anchor)
        j = max(pos, anchor)
        return (pos,
         anchor,
         _appuifw2.Text2_get_text(self._uicontrolapi, i, (j - i)))



    def set_selection(self, pos, anchor):
        _appuifw2.Text2_set_selection(self._uicontrolapi, pos, anchor)



    def set_word_wrap(self, word_wrap):
        _appuifw2.Text2_set_word_wrap(self._uicontrolapi, word_wrap)



    def set_limit(self, limit):
        _appuifw2.Text2_set_limit(self._uicontrolapi, limit)



    def get_word_info(self, pos = -1):
        return _appuifw2.Text2_get_word_info(self._uicontrolapi, pos)



    def set_case(self, case):
        _appuifw2.Text2_set_case(self._uicontrolapi, case)



    def set_allowed_cases(self, cases):
        _appuifw2.Text2_set_allowed_cases(self._uicontrolapi, cases)



    def set_input_mode(self, mode):
        _appuifw2.Text2_set_input_mode(self._uicontrolapi, mode)



    def set_allowed_input_modes(self, modes):
        _appuifw2.Text2_set_allowed_input_modes(self._uicontrolapi, modes)



    def set_undo_buffer(self, pos = 0, length = -1):
        return _appuifw2.Text2_set_undo_buffer(self._uicontrolapi, pos, length)



    def move(self, direction, select = False):
        _appuifw2.Text2_move(self._uicontrolapi, direction, select)



    def move_display(self, direction):
        _appuifw2.Text2_move_display(self._uicontrolapi, direction)



    def xy2pos(self, coords):
        return _appuifw2.Text2_xy2pos(self._uicontrolapi, coords)



    def pos2xy(self, pos):
        return _appuifw2.Text2_pos2xy(self._uicontrolapi, pos)


    for name in ('color',
     'focus',
     'font',
     'highlight_color',
     'style',
     'read_only',
     'has_changed',
     'allow_undo',
     'indicator_text'):
        exec ('%s = property(lambda self: _appuifw2.Text2_get_%s(self._uicontrolapi),lambda self, value: _appuifw2.Text2_set_%s(self._uicontrolapi, value))' % (name,
         name,
         name))

    for name in ('clear',
     'select_all',
     'clear_selection',
     'undo',
     'clear_undo',
     'can_undo',
     'can_cut',
     'cut',
     'can_copy',
     'copy',
     'can_paste',
     'paste'):
        exec ('%s = lambda self: _appuifw2.Text2_%s(self._uicontrolapi)' % (name,
         name))

    del name
