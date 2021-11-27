import redis


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Connection:
    def __init__(self):
        self._r = None
        self.set_url("redis://:p975d2dba3a5c75f5d5fc51a412f07722e4be526860ae94609067b37cd08adb7d@ec2-52-203-205-178.compute-1.amazonaws.com:15969")

    def set_url(self, url):
        self._r = redis.from_url(url)


    def get(self, code):
        resp = self._r.get(code)

        if resp:
            resp = str(resp.decode("UTF-8"))

        return resp

    def set(self, code, value):
        return self._r.set(code, value)
