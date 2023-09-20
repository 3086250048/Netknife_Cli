class test:
    def __init__(self) -> None:
        self._a=None
        self._b=None

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self,value):
        if not value :print('error')
        self._a=value

t=test()
print(setattr(t,'a',''))
