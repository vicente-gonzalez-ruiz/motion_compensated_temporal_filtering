import logging
from termcolor import colored

class ColorLog(object):

    colormap = dict(
        debug=dict(color='grey', attrs=['bold']),
        info=dict(color='green'),
        warn=dict(color='yellow', attrs=['bold']),
        warning=dict(color='yellow', attrs=['bold']),
        error=dict(color='red'),
        critical=dict(color='red', attrs=['bold']),
    )

    def __init__(self, logger):
        self._log = logger

    def __getattr__(self, name):
        if name in ['debug', 'info', 'warn', 'warning', 'error', 'critical']:
            return lambda s, *args: getattr(self._log, name)(
                colored(s, **self.colormap[name]), *args)

        return getattr(self._log, name)

logging.basicConfig()
#log = logging.getLogger("shell")
#log.setLevel('INFO')
log = ColorLog(logging.getLogger(__name__))
#log = ColorLog(logging.getLogger('joer'))

#logging.basicConfig()
#log = logging.getLogger(__name__)
log.setLevel('INFO')
#stdout = logging.StreamHandler()
#stdout.setLevel(logging.INFO)
#log.addHandler(stdout)
