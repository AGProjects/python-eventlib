__select = __import__('select')
__ignore = ('poll', 'epoll', 'kqueue', 'kevent')
for var in (var for var in dir(__select) if var not in __ignore):
    exec "%s = __select.%s" % (var, var)
from eventlib.api import select
del __select, __ignore, var

