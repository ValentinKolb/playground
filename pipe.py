from typing import Callable


class pipe:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __add__(self, other):
        ...

    def __or__(self, other):
        # print(f'__or__: {other=}')

        if isinstance(other, pipe) and len(other.args) == 1 and isinstance(other.args[0], Callable):
            return other(*self.args, **self.kwargs)
        elif isinstance(other, pipe):
            return pipe(*self.args, *other.args, **{**self.kwargs, **other.kwargs})
        elif isinstance(other, Callable):
            return other(*self.args, **self.kwargs)

        else:
            raise TypeError(f"unsupported operand type(s) for |: '{type(other)}' and '{type(self)}'")

    def __ror__(self, other):
        # print(f'__ror__: {other=}')

        if len(self.args) == 1 and isinstance(self.args[0], Callable):
            return self(other)
        elif isinstance(other, pipe):
            return pipe((*other.args, *self.args), {**other.kwargs, **self.kwargs})
        else:
            return pipe(other)

    def __call__(self, *args, **kwargs):
        func = self.args[0]
        assert isinstance(func, Callable)
        return pipe(func(*args, **kwargs))


if __name__ == '__main__':
    [i for i in range(100)] | pipe(sum) | print

    # pipe(1, foo=1) | pipe(2, bar=2) | (lambda *args, **kwargs: pipe(str(args) + " " + str(kwargs))) | print
