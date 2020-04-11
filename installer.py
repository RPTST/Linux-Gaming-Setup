import subprocess


# Lutris
"""
Adds packages needed for games to
be played on Linux (wine + dependencies) and
Lutris of course
"""

# Steam
"""
Returns steam packages and
steam proton for made by GloriousEggroll
"""

# vkBasalt
"""
Vkbasalt is a program which makes gaming
gaming better and makes games look much better
"""

# Gamemode
"""
Returns packages for this awesome program made by
FeralGaming which adds some extra performance/fps
"""

#C reate install script
"""
Creates the install.sh script
to install all programs & required packages
"""


class All:
    def __init__():
        subprocess.Popen(
            ('mkdir', '~/Programs'),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            )

    @staticmethod
    def vkbasalt():
        # configuration https://www.youtube.com/watch?v=6p1SNBy4P74&t=638s
        print("downloading vkBasalt.tar.gz")
        subprocess.Popen((
            'wget',
            'https://github.com/DadSchoorse/vkbasalt/' +
            'releases/latest/download/vkbasalt.tar.gz',
            '-O', '~/Programs'
        ))
        print("Building and configuring it like Chris Titus Tech did.\n")
        subprocess.Popen((
            'tar', '-xzvf', '-C', '~/Programs', '&&',
            'rm', '~/Programs/vkbasalt.tar.gz'
            ))
        subprocess.Popen((
            'cd', '~/Programs/vkbasalt', '&&', 'make', 'install'
            ))
        with open('~/Programs/vkbasalt/config', 'r') as config_file:
            config = config_file.readlines()
            for i, line in enumerate(config):
                if line.startswith('effects ='):
                    config[i] = 'effects = smaa:smaa:cas'
            config_file.writelines(config)


class Arch:
    def __init__(self):
        self._commands = []
        self._packages = []
        self._after = {'vkbasalt': [False, All.vkbasalt]}
        self._ypackage = None
        self._yay()
        if not self._ypackage:
            raise Exception('Yay not found.')

    def _yay(self):
        """
        Checks if yay installed and if it is not
        the command to be installed will be added to the top
        if the install scirpt
        """
        self._ypackage = False
        packages = subprocess.getoutput("pacman --query").splitlines()
        for package in packages:
            if package.startswith("yay"):
                self._ypackage = True
                print("Yay found !")
                break

    def lutris(self, gpu_brand):
        self._commands.append([
            "python -c 'import enableMultilib" +
            ";enableMultilib.pacmanConf()'"])
        print("Trying to enable multilib in pacman.conf\n")

        print("Returning wine & lutris packages\n")
        lutris_packages = [
            'lutris-git', 'lib32-opencl-icd-loader',
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
            'lib32-libxinerama', 'vulkan-icd-loader',
            ]

        print("checking gpu.")
        print(f"Detected an {gpu_brand} gpu.")
        print(f"Returning packages for vulkan support on {gpu_brand} gpu")

        def amd_vulkan():
            """
            Returns Vulkan packages for Amd gpus
            """
            return [
                'lib32-mesa',
                'vulkan-radeon',
                'lib32-vulkan-radeon',
                'vulkan-icd-loader',
                'lib32-vulkan-icd-loader'
                ]

        def nvidia_vulkan():
            """
            Returns Vulkan packages for Nvidia gpus
            """
            return [
                'nvidia',
                'nvidia-utils',
                'lib32-nvidia-utils',
                'nvidia-settings',
                'vulkan-icd-loader',
                'lib32-vulkan-icd-loader'
                ]

        def intel_vulkan():
            """
            Returns packages Vulkan packages for Intel igpus
            """
            return [
                'sudo',
                'pacman',
                '-S',
                'lib32-mesa',
                'vulkan-intel',
                'lib32-vulkan-intel',
                'vulkan-icd-loader',
                'lib32-vulkan-icd-loader'
                ]
        vulkan = {
            'amd': amd_vulkan,
            'intel': intel_vulkan,
            'nvidia': nvidia_vulkan
            }
        for vulkan_package in vulkan.get(gpu_brand)():  # for vulkan support
            lutris_packages.append(vulkan_package)  # packages for gpu
            for package in lutris_packages:
                self._packages.append(package)

    def steam(self):
        print("Returning steam package.\n")
        for steam_package in [
                'steam-native-runtime',
                'proton-ge-custom', 'steam'
                ]:
            self._packages.append(steam_package)

    def vkbasalt(self, build=False):
        if not build:
            print(
                "Returning necressary dependencies" +
                "for vkBasalt to work."
                )
            for vkbasalt_package in [
                    'glslang', 'vulkan-tools',
                    'lib32-libx11', 'libx11'
                ]:
                self._packages.append(vkbasalt_package)
            print("Downloading vkbasalt to ~/Programs")
            self._after['vkbasalt'][0] = True

    def gamemode(self):
        print("Returning gamemode packages")
        for gamemode_package in ['gamemode-git', 'lib32-gamemode-git']:
            self._packages.append(gamemode_package)

    def _yay_install_cmd(self):
        """
        Creates the yay install command
        """

        command = [
            'yay', '-S', '--redownloadall', '--sudoloop',
            '--nocleanmenu', '--nodiffmenu', '--noeditmenu'
            ]
        for package in self._packages:
            command.insert(2, package)
        self._commands.append(command)

    def create_install_script(self):
        self._yay_install_cmd()
        with open('./install.sh', 'a') as script_file:
            script_file.write("echo 'Install script executed'\n")
            for command in self._commands:
                script_file.write(f"{' '.join(command)}\n")


class Ubuntu:
    def __init__(self, lts):
        self.lts = lts
        self._packages = []
        self.ppa = []
        self.after = {'vkbasalt': [False, All.vkbasalt]}

    def lutris(self):
        print("Adding lutris ppa")
        self.ppa.append('ppa:lutris-team/lutris')

    def steam(self):
        self._packages.append('steam-installer')
