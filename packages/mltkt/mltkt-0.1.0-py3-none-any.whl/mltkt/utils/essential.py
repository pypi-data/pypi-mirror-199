import sys

# https://stackoverflow.com/a/41895257
def export(fn):
    """Use a decorator to avoid retyping function/class names.

    * Based on an idea by Duncan Booth:
      http://groups.google.com/group/comp.lang.python/msg/11cbb03e09611b8a
    * Improved via a suggestion by Dave Angel:
      http://groups.google.com/group/comp.lang.python/msg/3d400fb22d8a42e1
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        name = fn.__name__
        all_ = mod.__all__
        if name not in all_:
            all_.append(name)
    else:
        mod.__all__ = [fn.__name__]
    return fn

def static_var(**kwargs):
    def decorate(fn):
        for var_name, var_val in kwargs.items():
            setattr(fn, var_name, var_val)
        return fn
    return decorate
