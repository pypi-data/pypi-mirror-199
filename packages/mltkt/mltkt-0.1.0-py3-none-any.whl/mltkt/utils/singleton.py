class SingletonMixin:
    """
    inherit this class to make this subclass a singleton
    Usage:
        >>> class A(SingletonMixin): pass
        >>> class B(SingletonMixin): pass
        >>> a1, a2 = A(), A()
        >>> b1, b2 = B(), B()
        >>> assert a1 is a2
        >>> assert b1 is b2
        >>> assert not b1 is a1
    """
    _instance_dict = {}

    def __new__(cls, *args, **kwargs):
        key = str(hash(cls))
        if key not in SingletonMixin._instance_dict:
            SingletonMixin._instance_dict[key] = super().__new__(cls, *args, **kwargs)
        return SingletonMixin._instance_dict[key]
