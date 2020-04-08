import subprocess


class Arch:
    def __init__(self):
        self.after = {'vkbasalt': [False, self.vkbasalt]}
        self.yay()
        if not self.yay_package:
            raise "Yay not installed"

    # Arch
    def yay(self):
        self.yay_package = False
        packages = subprocess.getoutput("pacman --query").splitlines()
        for package in packages:
            if package.startswith("yay"):
                self.yay_package = True
                print("Yay found !")
                break
    @staticmethod
    def lutris():
        import enableMultilib
        print("Trying to enable multilib in pacman.conf\n")
        enableMultilib.pacmanConf()

        print("Returning wine & lutris packages\n")
        return [
            'gamemode-git', 'lib32-gamemode-git', 'lutris-git',
            'wine-staging', 'giflib', 'lib32-giflib', 'libpng',
            'lib32-libpng', 'libldap', 'lib32-libldap', 'gnutls',
            'lib32-gnutls', 'mpg123', 'lib32-mpg123', 'openal',
            'lib32-openal', 'v4l-utils', 'lib32-v4l-utils', 'libpulse',
            'lib32-libpulse', 'libgpg-error', 'lib32-libgpg-error',
            'alsa-plugins', 'lib32-alsa-plugins', 'alsa-lib', 'gtk3'
            'lib32-alsa-lib', 'libjpeg-turbo', 'lib32-libjpeg-turbo',
            'sqlite', 'lib32-sqlite', 'libxcomposite', 'lib32-gtk3',
            'libxinerama', 'lib32-libgcrypt', 'libgcrypt',
            'ncurses', 'lib32-ncurses', 'opencl-icd-loader',
            'libxslt', 'lib32-libxslt', 'libva', 'lib32-libva',
            'gst-plugins-base-libs', 'lib32-gst-plugins-base-libs',
            'lib32-vulkan-icd-loader', 'lib32-libxcomposite',
            'lib32-libxinerama', 'vulkan-icd-loader', 'lib32-opencl-icd-loader',
                ]
    @staticmethod
    def steam():
        print("Returning steam package.\n")
        return ['steam', 'steam-native-runtime', 'proton-ge-custom']

    def vkbasalt(self, build=False):
        if not build:
            print("downloading vkbasalt and installing necressary dependencies.\n")
            yield ['glslang', 'vulkan-tools', 'lib32-libx11', 'libx11']
            print("Downloading vkbasalt to ~/Programs")
            subprocess.Popen(('mkdir', '~/Programs'))
            subprocess.Popen((
                'wget',
                'https://github.com/DadSchoorse/vkbasalt/' +
                'releases/latest/download/vkbasalt.tar.gz',
                '-O', '~/Programs'
            ))
            self.after['vkbasalt'][0] = True
        else:
            # configuration https://www.youtube.com/watch?v=6p1SNBy4P74&t=638s
            print("Building and configuring it like Chris Titus Tech did.\n")
            subprocess.Popen((
                'tar', '-xzvf', '-C', '~/Programs', '&&',
                'rm', '~/Programs/vkbasalt.tar.gz'
                ))
            subprocess.Popen(('cd', '~/Programs/vkbasalt', '&&', 'make', 'install'))
            with open('~/Programs/vkbasalt/config', 'r') as config_file:
                config = config_file.readlines()
                for i, line in enumerate(config):
                    if line.startswith('effects ='):
                        config[i] = 'effects = smaa:smaa:cas'
                config_file.writelines(config)
    @staticmethod
    def gamemode():
        print("Returning gamemode packages")
        return ['gamemode-git', 'lib32-gamemode-git']

    def command(self, to_install):
        command = [
            'yay', '-S', '--redownloadall', '--sudoloop',
            '--nocleanmenu', '--nodiffmenu', '--noeditmenu'
            ]
        programs = {
            'lutris': Arch.lutris, 'steam': Arch.steam,
            'vkbasalt': self.vkbasalt, 'gamemode': Arch.gamemode
            }
        for program in to_install:
            program_packages = programs.get(program)()
            for package in program_packages:
                command.insert(2, package)
        return command
    
    def install(self, command):
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.stdin.write(b'y\n')
        for key in self.after:
            if self.after.get(key)[0]:
                self.after.get(key)[1](build=True)