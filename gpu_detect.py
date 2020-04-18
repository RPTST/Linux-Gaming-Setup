import subprocess

__all__ = ('GraphicsCard',)


class GraphicsCard:
    __slots__ = ('glxinfo', '_vendor', '_name', '__weakref__')

    VENDORS = ('amd', 'nvidia', 'intel')

    @property
    def vendor(self):
        if self._vendor is None:
            self._vendor = self._get_vendor()
        return self._vendor

    @property
    def name(self):
        if self._name is None:
            self._name = self._get_name()
        return self._name

    def __init__(self):
        with subprocess.Popen(
                ('glxinfo', '-B'),
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                universal_newlines=True,
        ) as popen:
            self.glxinfo = popen.stdout.readlines()
        self._vendor = None
        self._name = None

    def _get_vendor(self):
        def check(info):
            for vendor in GraphicsCard.VENDORS:
                if vendor in info or vendor.upper() in info:
                    return vendor
            return None

        for line in self.glxinfo:
            if line.startswith(('OpenGL vendor string:', '    Device:')):
                return check(line.split(':')[1])

    def _get_name(self):
        for line in self.glxinfo:
            line = line.strip()
            if line.startswith('OpenGL renderer string: '):
                name = line.split(': ')[1]
                if '/' in name:
                    name = name.split('/')[0]
                return name
            if line.startswith('Device: '):
                data = line.split('Device: ')[1]
                name = data.replace('AMD ', '').replace(' (TM)', '')
                return name.split(' (')[0].replace(' Graphics', '')
        return None
