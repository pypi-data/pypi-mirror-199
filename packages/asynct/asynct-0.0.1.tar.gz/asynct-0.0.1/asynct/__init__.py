from threading import Thread

class ThreadWithReturn(Thread):
    def __init__(
            self,
            group: None = None,
            target = None,
            name: str | None = None,
            args: tuple = None,
            kwargs: dict[str, object] | None = None,
            daemon: bool | None = None
        ) -> None:
        if args is None: args = ()
        if kwargs is None: kwargs = ()
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self._returned = None

    def run(self) -> None:
        if self._target is None: return
        self._returned = self._target(*self._args, *self._kwargs)
    
    def join(self, timeout: float | None = None) -> object:
        super().join(timeout)
        return self._returned

class Asynct:
    def __init__(
        self,
        group: None = None,
        target = None,
        name: str | None = None,
        args: tuple = None,
        kwargs: dict[str, object] | None = None,
        daemon: bool | None = None
    ):
        self._thread = ThreadWithReturn(group, target, name, args, kwargs, daemon)
        self._thread.start()

    def await_it(self):
        return self._thread.join()
    
    def then(self, func):
        @make_asynct
        def func(): func(self.await_it())
        return func()
    

    @staticmethod
    def all(*asyncts):
        @make_asynct
        def func(*asyncts):
            if not asyncts: return
            finished = 0
            for asynct in asyncts:
                @asynct.then
                def then(_):
                    nonlocal finished
                    finished += 1
            while finished < len(asyncts): pass
        return func(*asyncts)
    
    @staticmethod
    def race(*asyncts):
        @make_asynct
        def func(*asyncts):
            if not asyncts: return
            finished = 0
            returned = None
            for asynct in asyncts:
                @asynct.then
                def then(result):
                    nonlocal finished
                    if finished == 0:
                        nonlocal returned
                        returned = result
                    finished += 1
            while finished < 1: pass
            return returned
        return func(*asyncts)

def make_asynct(func) -> Asynct:
    def wrapper(*args, **kwargs):
        return Asynct(target=func, args=args, kwargs=kwargs)
    return wrapper