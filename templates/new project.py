import e32
import appuifw

# Thanks, Shrim! :)
def ru(t): return t.decode('utf-8')
def ur(t): return t.encode('utf-8')

def main():
    appuifw.app.body = 


lock = e32.Ao_lock()
appuifw.app.exit_key_handler = lock.signal
main()
lock.wait()


