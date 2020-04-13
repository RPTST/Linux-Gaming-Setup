import subprocess
import os
import sys
import distro


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

# Create ainstall script
"""
Creates an install script
to install selected programs & required packages
"""


class All:
    """Installer where distro doesnt matter"""
    def __init__(self):
        self.current_folder = f'{os.path.dirname(os.path.abspath(__file__))}/'
        self.programs_folder = f'/home/{os.getlogin()}/Programs'

        subprocess.Popen(
            (
                'mkdir', f'{self.current_folder}tmp'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()
        subprocess.Popen(
            (
                'mkdir', f'/home/{os.getlogin()}/Programs'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

    def vkbasalt(self):
        # configuration https://youtu.be/6p1SNBy4P74?t=875

        print("downloading vkBasalt.tar.gz")
        subprocess.Popen(
            (
                'wget',
                'https://github.com/DadSchoorse/vkbasalt/' +
                'releases/latest/download/vkbasalt.tar.gz',
                '-P', f'{self.current_folder}tmp/'),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

        print("Extracting the package to ./tmp & removing .tar.gz fle")
        subprocess.Popen(
            (

                'file-roller',
                f'--extract-to={self.programs_folder}',
                f'{self.current_folder}tmp/vkbasalt.tar.gz'),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

        print("Building and configuring it like Chris Titus Tech did.\n")
        subprocess.Popen(
            (
                'make', f'{self.programs_folder}tmp/vkBasalt',
                'install'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()
        with open(
                f'/home/{os.getlogin()}/.local/share/vkBasalt/vkBasalt.conf',
                'r+') as config_file:
            config = config_file.readlines()
            for i, line in enumerate(config):
                if line.startswith('effects ='):
                    config[i] = 'effects = smaa:smaa:cas'
            config_file.writelines(config)
            config_file.close()

        print("Removing folder ./tmp")
        subprocess.Popen(
            (
                'rm', '-r', f'{self.current_folder}tmp/'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

    def gamemode(self):
        gamemode_path = f'{self.programs_folder}/Gamemode'
        link = 'https://github.com/FeralInteractive/gamemode.git'

        print("Cloning Gamemode.")
        subprocess.Popen(
            (
                'cd', gamemode_path, '&&',
                'git', 'clone', link, '&&',
                'release=$( git tag | tail -1)', '&&',
                'git', 'checkout', '$release;'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
            ).wait()

        print("Building gamemode.")
        subprocess.Popen(
            (
                f'.{gamemode_path}/bootstrap.sh'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()


class Arch:
    """Installer for Arch based distros"""
    def __init__(self):
        self._commands = []
        self._packages = []
        self._after = {'vkbasalt': [False, All]}
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
                'sudo', 'pacman',
                '-S', 'lib32-mesa',
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

    def vkbasalt(self):
        print(
            "Returning necressary dependencies " +
            "for vkBasalt to work."
            )
        for vkbasalt_package in [
                'glslang', 'vulkan-tools',
                'lib32-libx11', 'libx11'
                ]:
            self._packages.append(vkbasalt_package)
        self._after['vkbasalt'][0] = True

    def gamemode(self):
        print("Returning gamemode packages")
        for gamemode_package in [
                'gamemode-git', 'lib32-gamemode-git',
                'meson', 'systemd-devel',
                'pkg-config git', 'dbus-devel'
                ]:
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

    def last(self):
        for key, value in self._after.items():
            if value[0]:
                class_obj = value[1]()
                getattr(class_obj, key)()


class Ubuntu:
    """Installer for Ubuntu based distros"""
    def __init__(self, lts):
        self.lts = lts
        self._packages = []
        self.ppa = []
        self._after = {'vkbasalt': [False, All]}

    def lutris(self):
        print("Adding lutris ppa")
        self.ppa.append('ppa:lutris-team/lutris')

    def steam(self):
        self._packages.append('steam-installer')


class Fedora:
    def __init__(self):
        self._packages = []
        self._commands = []
        self._fedora_ver = list(distro.linux_distribution())[1]
        self._after = {'vkbasalt': [False, All]}

    def lutris(self):
        print("Returning packages needed for lutris app.")
        if self._fedora_ver == '31':
            command = (
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/31/winehq.repo'
                )
            subprocess.Popen(
                tuple(
                    command.split()
                    ),
                stdout=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                ).wait()
            for package in (
                    'winehq-staging', 'vulkan-loader', 'vulkan-loader.i686',
                    'winetricks', 'lutris'):
                self._packages.append(package)

        elif self._fedora_ver == '30':
            for command in (
                    'dnf config-manager --add-repo' +
                    'https://dl.winehq.org/wine-builds/fedora/30/winehq.repo'):
                subprocess.Popen(
                    tuple(
                        command.split()
                        ),
                    stdout=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                    ).wait()
            for package in (
                    'winehq-staging', 'vulkan-loader', 'vulkan-loader.i686',
                    'winetricks', 'lutris'):
                self._packages.append(package)

        else:
            print(
                "Older version of Fedora than Fedora 30 or 31 detected.\n",
                "Please refer to https://wiki.winehq.org/Fedora")
            sys.exit()

    def steam(self):
        print("Adding the steam package")
        self._packages.append('steam')
        for command in (
                'dnf install -y fedora-workstation-repositories',
                'dnf install -y steam --enablerepo=rpmfusion-nonfree-steam'):
            subprocess.Popen(
                tuple(
                    command.split()
                    ),
                stdout=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                ).wait()

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True
        for package in (
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel.i686', 'libstdc++-devel.i686',
                'spirv-tools', 'libX11-devel.i686'):
            self._packages.append(package)

    def gamemode(self):
        for package in (
                'meson', 'systemd-devel',
                'pkg-config', 'git dbus-devel'):
            self._packages.append(package)
