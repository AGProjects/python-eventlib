__select = __import__('select')
for var in dir(__select):
    exec "%s = __select.%s" % (var, var)
from eventlib.api import select
#del poll
