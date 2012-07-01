import time

def getattr_(obj, name, default_thunk):
    "Similar to .setdefault in dictionaries."
    try:
        return getattr(obj, name)
    except AttributeError: 
         default = default_thunk()
         setattr(obj, name, default)
         return default


def memoize(func):
    """Create decorating function that is a callable instance of some class"""
    def new(*args, **kwargs):
        dic = getattr_(func, "memoize_dic", dict) 
        # memoize_dic is created at the first call
        mutable_args = [(name, obj) for (name, obj) in kwargs.iteritems() for mutable_type in (list, dict) if issubclass(obj.__class__, mutable_type)]
        if mutable_args:
            raise TypeError('\n You use mutable argument(s):\n' + '\n'.join(map(lambda i: '    %s = %s' % i, tuple(mutable_args))) +"\nCannot guarantee correct evaluating of the memoized function.")
        arguments = (args, tuple(kwargs.iteritems()))
        if arguments in dic:
            return dic[arguments]
        else:
            result = func(*args, **kwargs)
            dic[arguments] = result
            return result
    return type(func.func_name, (), {'__call__': staticmethod(new)})()


def profile(f, *args, **kw):
    def new(*args, **kw):
        t = time.clock
        begin = t()
        f(*args, **kw)
        print t() - begin
    return type(func.func_name, (), {'__call__': staticmethod(new)})()



if __name__ == '__main__':
    def heavy_computation(time_interval):
        time.sleep(time_interval)
        return "done by %d sec" % time_interval
    heavy_computation = memoize(heavy_computation)
    print heavy_computation(5) # the first time it will take 5 seconds
    print heavy_computation(5) # the second time it will be instantaneous

