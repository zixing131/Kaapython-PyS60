# Почитай комментарии, потом удали их, компилируй файл и пользуйся.
import kaapython
import ui
import os

# Сохраняем дефолтный метод, вызываемый при нажатии джойстика вправо в файловом браузер Kaapython.
default_enter_click = ui.FileBrowserWindow.enter_click


## Определяем новый обработчик.
## Идея такова: добавляем экземплярам файл.браузера новый атрибут "open_mode".
## Если open_mode не равен 'get_path' (это произвольный флаг, можно хоть "абракадабра" выбрать), то вызывается сохраненный выше дефолтный обработчик.
## В противном случае вызовется функция для получения пути к файлу/папке. Ей мы передаем ссылку на экземпляр файл.браузера, чтобы она могла с ним работать почти как родной метод.
## Кстати, enter_click_wrapper тоже косит под метод, хотя на самом деле обычная функция.
ui.FileBrowserWindow.open_mode = None
def enter_click_wrapper(self):
    if self.open_mode != 'get_path':
        default_enter_click(self)
    else:
        get_path(self)

# Заменяем дефолтный обработчик на новый. 
ui.FileBrowserWindow.enter_click = enter_click_wrapper


# Получаем путь к файлу/папке, так же как и в powlite_fm, выбирая необходимое нам нажатием джойстика вправо.
def get_path(self):
    i = self.current()
    if i < 0:
        return 
    item = self.lst[i]
    if item[0] == self.DRIVE:
        self.path = '%s\\' % item[3]
    elif item[0] in (self.FILE, self.DIR):
        self.path = os.path.join(self.path, item[3])
    self.close()


# Функция, которую и нужно будет вешать на шорткат через диалог.
def shortcut():
    try:
        ui.FileBrowserWindow.open_mode = 'get_path'
        browser_win = ui.FileBrowserWindow(title=_("Get path to file/dir"))
        browser_win.modal()
    finally: ui.FileBrowserWindow.open_mode = None
    # вот и путь к файлу
    path = browser_win.path
    # делаем с ним, что хотим:
    # отображаем в уведомлении;
    kaapython.notice(path)
    # копируем в буфер обмена
    import clipboard # импорт модуля можно, конечно, вынести из функции в начало плагина, в секцию импорта
    clipboard.Set(path)


# Надо добавить элемент с шорткатом в список функций доступных для назначения на шорткаты через соответствующий раздел Настроек. После этого мы можем вых.
# Кстати, сейчас функция get_shortcuts маскируется под метод класса. Чуть ниже мы её сделаем настоящим методом класса.
def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('Get path to file/dir'), target=shortcut))
    return menu



_ = kaapython.get_plugin_translator(__file__)
old_get_shortcuts = kaapython.repattr(kaapython.PythonFileWindow, 'get_shortcuts', classmethod(get_shortcuts))

