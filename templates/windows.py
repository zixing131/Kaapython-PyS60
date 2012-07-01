import appuifw2 as ui



class View(ui.View):
    
    from key_codes import EKeyYes, EKeySelect
    all = []

    def __init__(self, title):
        ui.View.__init__(self)
        self.title = u'%s' % title
        self.body = ui.Text()
        self.exit_key_handler = self.close
        cls = self.__class__
        self.body.bind(cls.EKeyYes, self.switch2next)
        self.body.bind(cls.EKeySelect, lambda: self.body.add(u'\u2029'))
        cls.all.append(self)

    def switch2next(self):
        all = self.__class__.all
        index = all.index(self)
        if index < len(all) - 1:
            ui.app.view = all[index + 1]
        else:
            ui.app.view = all[0]
        self.body.read_only = False

one = View('one')
two = View(u'two')
ui.app.view = one
one.wait_for_close()

