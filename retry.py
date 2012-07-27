#coding: utf-8

# module created by fjsj - flaviojuvenal@gmail.com
# original repo: https://github.com/fjsj/retry_on_exceptions/

import time


def retry_on_exceptions(types, tries, sleep=0):
    class RetryException(Exception):  # Exception to activate retries
        pass

    def call_and_ignore_exceptions(types, fxn, *args, **kwargs):
        try:
            return fxn(*args, **kwargs)
        except Exception, exc:
            if any((isinstance(exc, exc_type) for exc_type in types)):
                raise RetryException()
            else:
                raise exc  # raise up unknown error

    def decorator(fxn):
        def f_retry(*args, **kwargs):
            local_tries = tries  # make mutable
            while local_tries > 1:
                try:
                    return call_and_ignore_exceptions(types,
                                                      fxn,
                                                      *args,
                                                      **kwargs)
                except RetryException:
                    local_tries -= 1
                    print "Retrying function %s" % fxn.__name__
                    time.sleep(sleep)

            print ("Last try... and I will raise up whatever"
                   " exception is raised")
            return fxn(*args, **kwargs)
        return f_retry
    return decorator


if __name__ == "__main__":
    current_try = 0

    @retry_on_exceptions(types=[Exception], tries=3, sleep=5)
    def test():
        global current_try
        current_try += 1
        if current_try == 1:
            return 1 / 0
        elif current_try == 2:
            return dict()['key']
        else:
            return "Got it on last try!"

    print test()
