import os
import subprocess
import distro

__all__ = ('Distribution', 'GraphicsCard', 'Processor')


class Distribution:
    __slots__ = ('_distro', '_distro_info', '__weakref__')

    @property
    def distro(self):
        if self._distro is None:
            self._distro = self._get_distro()
        return self._distro

    def __init__(self):
        self._distro = None
        self._distro_info = list(distro.linux_distribution())

    def _get_distro(self):
        return {"based": distro.like(), "distribution": self._distro_info[2],
                "distro_version": self._distro_info[1]}


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
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env={**os.environ, 'LC_ALL': 'C'},
                universal_newlines=True,
        ) as popen:
            self.glxinfo = popen.stdout.readlines()
        self._vendor = None
        self._name = None

    def _get_vendor(self):
        def check(info):
            for vendor in GraphicsCard.VENDORS:
                if vendor in info.lower():
                    return vendor
            return 'Unknown'

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
        return 'Unknown'


class Processor:
    @staticmethod
    def _clean(text):
        if text.startswith("Intel"):
            text = text.split(" CPU @")[0]
            return text.replace("(R)", "").replace("(TM)", "")
        if text.startswith("AMD"):
            words = text.split(" ")
            words = words[:-2]
            return " ".join(words)
        print("Cpu not found or supported")
        return None

    @staticmethod
    def cpu():
        cpu_path = "/proc/cpuinfo"
        with open(cpu_path, "r") as file:
            return next(
                Processor._clean(line.split(": ")[1])
                for line in file
                if line.startswith("model name\t")
            )