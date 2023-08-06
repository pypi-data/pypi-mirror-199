# This file is placed in the Public Domain.


"locks"


import _thread


from functools import wraps


disklock = _thread.allocate_lock()


def locked(thislock):

    def lockeddec(func, *args, **kwargs):

        @wraps(func)
        def lockedfunc(*args, **kwargs):
            thislock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                thislock.release()
            return res

        return lockedfunc

    return lockeddec
