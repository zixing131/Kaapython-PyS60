import kaapython, ui
from time import localtime
from smtplib import SMTP
import socket


connect = point = None
filename = __file__ + '.data'
try:
    file = open(filename)
    log, pas, fromaddr, toaddr = [l.decode('base64') for l in file.readlines()]
    file.close()
except (IOError, ValueError,):
    log = pas = fromaddr = toaddr = None


def get_data():
    global log, pas, fromaddr, toaddr
    log_ = pas_ = fromaddr_ = toaddr_ = None
    if log is None or ui.query(_('Set or change the login?'), 'query') == 1:
        while not log_:
            log_ = ui.query(_('Your login:'), 'text', u'')
    if pas is None or ui.query(_('Set or change the password?'), 'query') == 1:
        while not pas_:
            pas_ = ui.query(_('Password:'), 'code', u'')
    if fromaddr is None or ui.query(_('Set or change the address of the sender?'), 'query') == 1:
        while not fromaddr_:
            fromaddr_ = ui.query(_('From address:'), 'text', u"name@server.")
    if toaddr is None or ui.query(_('Set or change the address of the recipient?'), 'query') == 1:
        while not toaddr_:
            toaddr_ = ui.query(_('To address:'), 'text', fromaddr_)
        log, pas, fromaddr, toaddr = log_, pas_, fromaddr_, toaddr_
        try:
            open(filename, 'w').writelines([i.encode('base64') for i in log, pas, fromaddr, toaddr])
        except IOError: pass
    return log, pas, fromaddr, toaddr


def send():
    global connect, fromaddr, toaddr, point, log, pas
    if point is None:
        # PIC<P"PuC,PŸPuC, :'-(
        #select = socket.select_access_point()
        #point = socket.access_point(select)
        #socket.set_default_access_point(point)
        pass
    if not connect:
        log, pas, fromaddr, toaddr = get_data()
        recipient = toaddr.split('@')[0]
    cur_time = '%s.0%s.%s | %s:%s:%s' % localtime()[:6]
    text_message = ui.app.body.get()
    apptitle = ui.app.title
    message = u"""From: %s <%s>
To: %s <%s>
Subject: Backup of file <%s> in %s
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: 8bit


<pre>%s</pre>
"""
    if not connect:
        connect = SMTP('smtp.%s:25' % toaddr.split(u'@')[-1])
    #connect.set_debuglevel(1)
    try:
        connect.login(log, pas)
        connect.sendmail(fromaddr, toaddr, (message % (log, fromaddr, recipient, toaddr, apptitle, cur_time, text_message)).replace(u'\u2029', '<br>').encode('utf-8'))
    except:
        if ui.query(_('Action failed. Try again?')) == 1: return send()
    else:
        connect.quit()
        connect = None
        ui.infopopup.show(_('Action complete!'))


def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('Send buffer to email'), target=send))
    return menu


old_get_shortcuts = kaapython.repattr(kaapython.TextWindow, 'get_shortcuts', classmethod(get_shortcuts))
_ = kaapython.get_plugin_translator(__file__)
 