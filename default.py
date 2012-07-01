try:

    if __name__ == '__main__':
    
        # *** DISABLE FOR RELEASES ***
        import sys, os
        sys.setdefaultencoding('utf-8')
        name = os.path.split(os.path.split(sys.argv[0])[0])[1]
        path = os.path.join('E:\\Python', name)
        if os.path.exists(path):
            sys.path.insert(0, path)
        from kaapython import app
        app.start()

except:

    import sys, traceback, appuifw

    tb = ''.join(traceback.format_exception(*sys.exc_info()))
    open('d:/kaapython.log', 'w').write(tb.encode('utf-8'));appuifw.note('')
    appuifw.app.title = u'Fatal Error'
    appuifw.app.screen = 'normal'
    appuifw.app.focus = None
    appuifw.app.body = appuifw.Text()
    appuifw.app.exit_key_handler = appuifw.app.set_exit
    appuifw.app.menu = [(u'Exit', appuifw.app.set_exit)]
    appuifw.app.body.set(unicode(tb))
