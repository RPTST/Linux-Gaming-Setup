import subprocess


class Graphics_card:
    def __init__(self):
        self.glxinfo = subprocess.Popen(
            ('glxinfo', '-B'),
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE
            ).stdout.read().decode().splitlines()

    def vendor(self):
        vendors = ['amd', 'nvidia', 'intel']
        data = self.glxinfo

        def clean(line):
            return line.split(':')[1]

        def check(info):
            nonlocal vendors
            for vendor in vendors:
                if vendor in info:
                    return vendor
                elif vendor.upper() in info:
                    return vendor

        for line in data:
            if line.startswith(
                'OpenGL vendor string:') or line.startswith(
                    '    Device:'):
                info = clean(line)
                return check(info)

    def name(self):
        for line in self.glxinfo:
            if line.strip().startswith('OpenGL renderer string: '):
                name = line.split(': ')[1]
                if '/' in name:
                    name = name.split('/')[0]
                return name
            elif line.strip().startswith('Device: '):
                data = line.split('Device: ')[1]
                name = data.replace('AMD ', '').replace(' (TM)', '')
                return name.split(' (')[0].replace(' Graphics', '')
