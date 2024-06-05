def _load_ipython_extension():
    try:
        from IPython import get_ipython
        if get_ipython():
            from . import ipython_extension
    except ImportError:
        pass

_load_ipython_extension()
