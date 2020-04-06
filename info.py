import os
import distro
import glob
import subprocess


class Distribution:
    def __init__(self):
        self.distro = {}
        self.distro_info = list(distro.linux_distribution())

    def distro_checker(self):
        self.distro["based"] = distro.like()
        self.distro["distribution"] = self.distro_info[2]
        self.distro["distro_version"] = self.distro_info[1]
        return self.distro


class Hardware:
    def __init__(self):
        pass

    # dont remember why
    @staticmethod
    def clean(text):
        if text.startswith("Intel"):
            text = text.split(" CPU @")[0]
            return text.replace("(R)", "").replace("(TM)", "")
        elif text.startswith("AMD"):
            splitted = text.split(" ")
            for i in range(2):
                splitted.pop(-1)
            return " ".join(splitted)
        else:
            print("Cpu not found or supported")

    def cpu(self):
        cpu_path = "/proc/cpuinfo"
        with open(cpu_path, "r") as FileObj:
            return next(
                Hardware.clean(line.split(": ")[1])
                for line in FileObj
                if line.startswith("model name\t")
            )

    @staticmethod
    def gpu():
        companys = ["AMD", "INTEL", "NVIDIA"]
        with subprocess.Popen(
            ("glxinfo", "-B"),
            bufsize=1,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            shell=False,
            universal_newlines=True,
            env={**os.environ, "LC_ALL": "C"},
        ) as popen:
            for line in popen.stdout:
                if line.strip().startswith("Device"):
                    splitted = line.split(" ")
                    for element in splitted:
                        for element in companys:
                            return element