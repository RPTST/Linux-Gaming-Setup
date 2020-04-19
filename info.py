import os
import subprocess

import distro

__all__ = ('Distribution', 'Hardware')


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


class Hardware:
    __slots__ = ('__weakref__',)

    GPU_VENDORS = ("AMD", "INTEL", "NVIDIA")

    def __init__(self):
        pass

    @staticmethod
    def clean(text):
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
                Hardware.clean(line.split(": ")[1])
                for line in file
                if line.startswith("model name\t")
            )

    @staticmethod
    def gpu():
        with subprocess.Popen(
                ("glxinfo", "-B"),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                universal_newlines=True,
                env={**os.environ, "LC_ALL": "C"},
        ) as popen:
            for line in popen.stdout:
                line = line.strip()
                if line.startswith("Device: "):
                    words = line.split(" ")
                    for element in words:
                        if element in Hardware.GPU_VENDORS:
                            return element
                elif line.startswith("OpenGL vendor string: "):
                    line = line.upper()
                    for vendor in Hardware.GPU_VENDORS:
                        if vendor in line:
                            return vendor
        return None
