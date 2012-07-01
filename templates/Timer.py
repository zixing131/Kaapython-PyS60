class Timer:
    
    def __init__(self, title, doc, interval, target, start=False):
        from e32 import Ao_timer
        self.title = title
        self.doc = doc
        self.interval = interval
        self.target = target
        self.core = Ao_timer()
        self.runned = False
        if start: return ao_sleep(0, self.start)
    
    def start(self, recursion=False):
        """Запускает таймер.
        recursion=True - запускает таймер в бесконечный цикл.
        """
        self.core.cancel()
        self.runned = True
        if recursion:
            self.core.after(self.interval, lambda: (self.target(), self.start(True)))
        else:
            self.core.after(self.interval, lambda: (self.target(), self.stop()))
    
    def stop(self):
        self.core.cancel()
        self.runned = False

if __name__ == '__main__':
    from appuifw import note
    timer = Timer(
        title=u'timer',
        doc=u'I will be show from time to time notification.',
        interval=50, # seconds
        target=lambda: note(u'Timer works.'))
    timer.start(recursion=True)

