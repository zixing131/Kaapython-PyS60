import appuifw

def save_hook(data):
    print data

model = [u'6600', u'6630', u'7610', u'N90', u'N70']


data = [(u'Mobile', 'text', u'Nokia'), (u'Model', 'combo', (model, 0)), (u'Amount', 'number', 5), (u'Date', 'date'), (u'Time', 'time')]


# set the view/edit mode of the form
flags = appuifw.FFormEditModeOnly


# creates the form
f = appuifw.Form(data, flags)
f.save_hook = save_hook
# make the form visible on the UI
appuifw.app.body.bind(8, save_hook)
f.execute()

#SETTINGS_TEMPLATE = re.compile(R'(?P<dict>{(?P<key>(?P<name>"[a-zA-z_0-9\.]+?"):)(?P<bool>true|false)|(?P<list>[(?P=name)])})')