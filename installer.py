import subprocess
import os
import shutil
import distro
import multi


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
    """
    Installer where distro doesnt matter
    """
    __slots__ = (
        'current_folder',
        'programs_folder',
        'proton_ge_aurl'
        )

    def __init__(self):
        self.current_folder = f'{os.path.dirname(os.path.abspath(__file__))}/'
        self.programs_folder = os.path.expanduser('~/Programs')
        self.create_folder(self.programs_folder)
        self.create_folder(self.programs_folder + '/tmp')

    def vkbasalt_all(self):
        download_link = (
            "https://github.com/DadSchoorse/vkbasalt/" +
            "releases/latest/download/vkbasalt.tar.gz"
            )
        print("downloading vkBasalt.tar.gz and extracting it to ~/Programs")
        multi.download_extract(download_link, self.programs_folder)

        print("Building and configuring it like Chris Titus Tech did.\n")
        subprocess.Popen(
            (
                'make' f'{self.programs_folder}tmp/vkBasalt',
                '&&',
                'make', f'{self.programs_folder}tmp/vkBasalt',
                'install'
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

        with open(
                f'/home/{os.getlogin()}/.local/share/vkBasalt/vkBasalt.conf',
                'r+'
                ) as config_file:
            config = config_file.readlines()
            for i, line in enumerate(config):
                if line.startswith('effects ='):
                    config[i] = 'effects = smaa:smaa:cas'
            config_file.writelines(config)
            config_file.close()

        print("Removing folder ./tmp")
        shutil.rmtree(f'{self.current_folder}/tmp/vkBasalt')

    def gamemode_all(self, last_arg):
        gamemode_path = f'{self.programs_folder}/Gamemode'
        link = 'https://github.com/FeralInteractive/gamemode.git'

        print("Cloning Gamemode.")
        multi.get_release_data(link, 'first', 1)
        print("Building gamemode.")
        subprocess.Popen(
            (
                f'.{gamemode_path}/bootstrap.sh',
                last_arg
                ),
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            ).wait()

    @staticmethod
    def proton_ge_all(links):
        proton_path = os.path.expanduser(
            '~/.local/share/Steam/compatibilitytools.d'
            )
        for link in links:
            multi.download_extract(link, proton_path)

    def last_all(self):
        for key, value in self._after.items():
            if value[0]:
                self = value[1]()
                getattr(self, key)(value[2])

    @staticmethod
    def create_install_cmd_all(command, insert_int, packages):
        """
        Creates the install command
        """
        for package in packages:
            command.insert(insert_int, package)
        return ' '.join(command)

    @staticmethod
    def create_install_script_all(create_icmd, _packages, _top_commands):
        """
        Creates the install.sh file
        """
        install_cmd = All.create_install_cmd_all(
            create_icmd[0],
            create_icmd[1],
            _packages
            )
        with open('./install.sh', 'a') as script_file:
            script_file.write("echo 'Install script executed'\n")
            if _top_commands:
                script_file.write("echo 'Top command/s executed'\n")
                for _top_cmd in _top_commands:
                    script_file.write(_top_cmd + '\n')
            if create_icmd[1]:
                script_file.write("echo 'Packages are being downloaded'\n")
                script_file.write(install_cmd + '\n')

    @staticmethod
    def create_folder(path):
        try:
            os.mkdir(os.path.expanduser(path))
            print("Folder created at this path:" + path)

        except FileExistsError:
            print(f"It seems that the {path} folder has already been created.")


class Arch(All):
    """
    Arch based install class
    """
    __slots__ = (
        'gpu_vendor',
        '_top_commands',
        '_packages',
        '_after',
        '_ypackage',
        )

    def __init__(self):
        self.gpu_vendor = None
        self._top_commands = []
        self._packages = []
        self._after = {'vkbasalt': [False, All]}
        self._ypackage = None
        self._yay()
        if not self._ypackage:
            raise Exception('Yay not found.')
        super().__init__()

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

    def lutris(self):
        if not self.gpu_vendor:
            print(self.gpu_vendor)
            raise SystemError("self.gpu_vendor is set to None ! report this")
        self._top_commands.append(
            "python -c 'import enableMultilib" +
            ";enableMultilib.pacmanConf()'")
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
        print(f"Returning packages for vulkan support on {self.gpu_vendor} gpu")

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
        for vulkan_package in vulkan.get(self.gpu_vendor)():  # for vulkan support
            lutris_packages.append(vulkan_package)  # packages for gpu
            for package in lutris_packages:
                self._packages.append(package)

    def steam(self):
        print("Returning steam package.\n")
        for steam_package in [
                'steam-native-runtime', 'steam'
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

    def create_install_script(self):
        command = [
            'yay', '-S', '--redownloadall', '--sudoloop',
            '--nocleanmenu', '--nodiffmenu', '--noeditmenu'
            ]
        All.create_install_script_all(
            [command, 2], self._packages, self._top_commands
            )


class Fedora(All):
    """
    Fedora install class
    """
    __slots__ = (
        '_packages',
        '_top_commands',
        '_fedora_ver',
        '_after'
        )

    def __init__(self):
        self._packages = []
        self._top_commands = []
        self._fedora_ver = float(distro.version())
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All]
            }
        super().__init__()

    def lutris(self):
        print("Returning packages needed for lutris app.")
        if self._fedora_ver == '31':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/31/winehq.repo'
                )
            for package in (
                    'winehq-staging', 'vulkan-loader', 'vulkan-loader.i686',
                    'winetricks', 'lutris'):
                self._packages.append(package)

        elif self._fedora_ver == '30':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/30/winehq.repo'
                )
            for package in (
                    'winehq-staging', 'vulkan-loader', 'vulkan-loader.i686',
                    'winetricks', 'lutris'):
                self._packages.append(package)

        else:
            print(
                "\n#########################################################"
                "\nOlder version of Fedora than Fedora 30 or 31 detected.",
                "\nPlease refer to https://wiki.winehq.org/Fedora ."
                "\n#########################################################"
                )

    def steam(self):
        print("Adding the steam package")
        self._packages.append('steam')
        for command in (
                'dnf install -y fedora-workstation-repositories',
                'dnf install -y steam --enablerepo=rpmfusion-nonfree-steam'):
            self._top_commands.append(command)

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True
        for package in (
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel.i686', 'libstdc++-devel.i686',
                'spirv-tools', 'libX11-devel.i686'):
            self._packages.append(package)

    def gamemode(self):
        print(
            "Adding packages nesressary for building gamemode."
            )
        for package in (
                'meson', 'systemd-devel',
                'pkg-config', 'git dbus-devel'):
            self._packages.append(package)

    def create_install_script(self):
        command = ['dnf', 'install', '-y']
        All.create_install_script_all(
            [command, 2]
            )


class Solus(All):
    """
    Solus install class
    """
    __slots__ = (
        '_packages',
        '_after'
        )

    def __init__(self):
        self._packages = []
        self._after = {'vkbasalt': [False, All]}
        super().__init__()

    def lutris(self):
        print("Adding lutris packages")
        for package in [
                'wine', 'wine-devel', 'wine-32bit-devel', 'winetricks',
                'vulkan, vulkan-32bit, vulkan-headers'
                ]:
            self._packages.append(package)

    def steam(self):
        for package in [
                'steam', 'linux-steam-integration'
                ]:
            self._packages.append(package)

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True
        for package in [
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel', 'libstdc++', 'spirv-tools'
                ]:
            self._packages.append(package)

    def gamemode(self):
        for package in [
                'gamemode', 'gamemode-32bit']:
            self._packages.append(package)

    def create_install_script(self):
        command = ['eopkg', 'install', '-y']
        All.create_install_script_all(
            [command, 2]
            )


class Ubuntu(All):
    """
    Ubuntu install class
    """
    __slots__ = (
        '_packages',
        '_top_commands',
        '_after',
        'version'
        )

    def __init__(self):
        self._packages = []
        self._top_commands = []
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All, '-y']
            }
        self.version = distro.version()
        super().__init__()

    def lutris(self):
        def wine():
            self._top_commands.append(
                'add-apt-repository ppa:lutris-team/lutris'
                )
            for command in [
                    'dpkg --add-architecture i386',
                    'wget -nc https://dl.winehq.org/wine-builds/winehq.key',
                    'apt-key add winehq.key']:
                self._top_commands.append(command)
            versions_repo = {
                'eoan': (
                    "apt-add-repository " +
                    "'deb https://dl.winehq.org/wine-builds/ubuntu/ " +
                    "eoan main'"
                    ),
                'disco': (
                    "apt-add-repository " +
                    "'deb https://dl.winehq.org/wine-builds/ubuntu/ " +
                    "disco main'"
                    ),
                'cosmic': (
                    "apt-add-repository " +
                    "'deb https://dl.winehq.org/wine-builds/ubuntu/ " +
                    "cosmic main'"
                    ),
                'bionic': (
                    "apt-add-repository " +
                    "'deb https://dl.winehq.org/wine-builds/ubuntu/ " +
                    "bionic main'"
                    ),
                'xenial': (
                    "apt-add-repository " +
                    "'deb https://dl.winehq.org/wine-builds/ubuntu/ " +
                    "xenial main'"
                    )
                }
            for version in versions_repo:
                if version in distro.codename().lower():
                    repository = versions_repo.get(version)
                    self._top_commands.append(repository)
                    if version == 'eoan':
                        self._top_commands.append(
                            'apt install --install-recommends' +
                            'wine-stable winehq-stable ' +
                            'wine-stable wine-stable-i386 wine-stable-amd64 -y'
                            )
                    else:
                        self._top_commands.append(
                            'apt install --install-recommends winehq-stable -y'
                            )
                else:
                    raise SystemError("Version of ubuntu not recognized")

        wine()

        # drivers
        def amd_intel(vulkan):
            self._top_commands.append("dpkg --add-architecture i386")
            self._packages.append("libgl1-mesa-dri:i386")
            if vulkan:
                for package in [
                        "mesa-vulkan-drivers",
                        "mesa-vulkan-drivers:i386"]:
                    self._packages.append(package)

    def steam(self):
        self._packages.append('steam')

    def vkbasalt(self):  # fixme
        # test on other ubuntu versions
        self._after['vkbasalt'][0] = True
        if 'eoan' in distro.codename().lower():
            for package in [
                    'build-essential', 'glslang-tools',
                    'vulkan-validationlayers-dev', 'libvulkan-dev',
                    'vulkan-tools', 'spirv-tools']:
                self._packages.append(package)

    def gamemode(self):
        for package in [
                'meson', 'libsystemd-dev',
                'pkg-config', 'ninja-build',
                'libdbus-1-dev', 'libinih-dev',
                'git', 'dbus-user-session'
                ]:
            self._packages.append(package)
        self._after['gamemode'][0] = True

    def create_install_script(self):
        command = ['apt', 'install', '-y']
        self._top_commands.append('apt update')
        All.create_install_script_all(
            [command, 2]
            )
