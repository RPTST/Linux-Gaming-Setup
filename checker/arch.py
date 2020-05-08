import subprocess


class Arch:
    def __init__(self, package_class):
        self.query = None
        self.set_query()
        self.package_class = package_class

    def set_query(self):
        query = subprocess.Popen(
            (
                'pacman',
                '--query'
            ),
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).stdout.read().decode().splitlines()
        self.query = query.sort()