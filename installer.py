import subprocess
import os
import shutil
import distro
import multi

class PackageNotFound(Exception):
    pass


class GpuNotSupported(Exception):
    pass


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
        self.create_folder(self.programs_folder + '/tmp')

    def create_folder(self, path):
        try:
            os.makedirs(os.path.expanduser(path))
            print("Folder created at this path:" + path)

        except FileExistsError:
            print(f"It seems that the {path} folder has already been created.")

    def vkbasalt_all(self):
        download_link = (
            "https://github.com/DadSchoorse/vkbasalt/" +
            "releases/latest/download/vkbasalt.tar.gz"
            )
        print("downloading vkBasalt.tar.gz and extracting it to ~/Programs/tmp")
        multi.download_extract(download_link, self.programs_folder + '/tmp')

        print("Building and configuring it like Chris Titus Tech did.\n")
        subprocess.Popen(
            (
                'make', f'{self.programs_folder}/tmp/vkBasalt'
                )
            ).wait()
        with open(
                os.path.expanduser('~/.local/share/vkBasalt/vkBasalt.conf'),
                'r+'
                ) as config_file:
            config = config_file.readlines()
            for i, line in enumerate(config):
                if line.startswith('effects ='):
                    config[i] = 'effects = smaa:smaa:cas'
            config_file.writelines(config)
            config_file.close()

        print("Removing folder ./tmp")
        shutil.rmtree(self.programs_folder + '/tmp/vkBasalt')

    def gamemode_all(self, last_arg):
        download_path = self.programs_folder + '/tmp'
        gamemode_path = download_path + '/Gamemode'
        api_link = (
            'https://api.github.com/repos/' +
            'FeralInteractive/Gamemode/releases'
            )
        dl_link = multi.get_release_data(
            api_link,
            'last'
            )[0].get('download_url')

        print("Cloning Gamemode.")

        multi.download_extract(dl_link, download_path)
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
                getattr(self, key)()

    @staticmethod
    def create_install_cmd_all(command, insert_int, packages):
        """
        Creates the install command
        """
        for package in packages:
            command.insert(insert_int, package)
        return ' '.join(command)

    def create_install_script_all(self, create_icmd, _packages, _top_commands):
        """
        Creates the install.sh file
        """
        if create_icmd[1]:
            install_cmd = All.create_install_cmd_all(
                create_icmd[0],
                create_icmd[1],
                _packages
                )

        if self.__class__.__base__.__name__ == 'Arch':
            print("Arch installer script")
            with open('./main_install.sh', 'a') as script_file:
                script_file.write("echo 'Install script executed'\n")
                if create_icmd[1]:
                    script_file.write(install_cmd + "\n")
                    script_file.write('pkexec sh _top_commands')
                    os.path.isfile('./main_install.sh')

        else:
            print("Installer script for all other distros")
            with open('./main_install.sh', 'a') as script_file:
                script_file.write("echo 'Install script executed'\n")
                if _top_commands:
                    script_file.write("echo 'Top command/s executed'\n")
                    for _top_cmd in _top_commands:
                        script_file.write(_top_cmd + '\n')
                if create_icmd[1]:
                    script_file.write("echo 'Packages are being downloaded'\n")
                    script_file.write(install_cmd + '\n')


class Arch(All):
    __slots__ = (
        "gpu_vendor",
        "_top_commands",
        "_after"
        )

    def __init__(self, gpu_vendor):
        super().__init__()
        self.gpu_vendor = gpu_vendor
        self._top_commands = list()
        self._after = {'vkbasalt_all': [False, All]}
        if not self._check_yay():
            raise PackageNotFound("Yay not installed")

    def _check_yay(self):
        """
        Checks if yay installed and if it is not
        the command to be installed will be added to the top
        if the install scirpt
        """
        packages = subprocess.getoutput("pacman --query").splitlines()
        for package in packages:
            if package.startswith("yay"):
                print("Yay found !")
                return True
        raise PackageNotFound("yay not installed !")

    def wine(self):
        for package in [
                'lib32-opencl-icd-loader', 'libpng', 'gnutls',
                'wine-staging', 'giflib', 'lib32-giflib', 'libpulse',
                'lib32-libpng', 'libldap', 'lib32-libldap',
                'lib32-gnutls', 'mpg123', 'lib32-mpg123', 'openal',
                'lib32-openal', 'v4l-utils', 'lib32-v4l-utils',
                'lib32-libpulse', 'libgpg-error', 'lib32-libgpg-error',
                'alsa-plugins', 'lib32-alsa-plugins', 'alsa-lib', 'gtk3'
                'lib32-alsa-lib', 'libjpeg-turbo', 'lib32-libjpeg-turbo',
                'sqlite', 'lib32-sqlite', 'libxcomposite', 'lib32-gtk3',
                'libxinerama', 'lib32-libgcrypt', 'libgcrypt',
                'ncurses', 'lib32-ncurses', 'opencl-icd-loader',
                'libxslt', 'lib32-libxslt', 'libva', 'lib32-libva',
                'gst-plugins-base-libs', 'lib32-gst-plugins-base-libs',
                'lib32-vulkan-icd-loader', 'lib32-libxcomposite',
                'lib32-libxinerama', 'vulkan-icd-loader'
                ]:
            yield package


    def lutris(self):
        yield "lutris-git"
        print(f"Returning packages for vulkan support on {self.gpu_vendor} gpu")

        def amd():
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

        def nvidia():
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

        def intel():
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
            'amd': amd,
            'intel': intel,
            'nvidia': nvidia
            }
        for vulkan_package in vulkan.get(self.gpu_vendor)():  # for vulkan support
            yield vulkan_package

    def steam(self):
        print("returning steam packages")
        for package in [
                'steam-native-runtime',
                'steam'
                ]:
            yield package

    def vkbasalt(self):
        print(
            "Returning necressary dependencies",
            "for vkBasalt to work."
            )
        for package in [
                'glslang', 'vulkan-tools',
                'lib32-libx11', 'libx11'
                ]:
            yield package
        self._after['vkbasalt_all'][0] = True


    def gamemode(self):
        print("Returning gamemode packages")
        for package in [
                'gamemode-git', 'lib32-gamemode-git',
                'meson', 'systemd-devel',
                'pkg-config git', 'dbus-devel'
                ]:
            yield package

    def install_script(self, install_programs):
        command = [
            'yay', '-S', '--redownloadall', '--nosudoloop',
            '--nocleanmenu', '--nodiffmenu', '--noeditmenu',
            '--sudo', 'pkexec'
            ]
        packages = list()
        for program in install_programs:
            packages += list(getattr(self, program)())
        self.create_install_script_all(
            [command, 2], packages, self._top_commands)


class Fedora(All):
    __slots__ = (
        "_top_commands",
        "_after",
        "gpu_vendor"
        )
    def __init__(self, gpu_vendor):
        super().__init__()
        self._top_commands = list()
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All]
            }
        self.gpu_vendor = None

    def wine(self):
        fedora_ver = float(distro.version())
        print("Returning packages needed for lutris app.")
        if fedora_ver == '31':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/31/winehq.repo'
                )
            for package in (
                    'winehq-staging', 'vulkan-loader', 'vulkan-loader.i686',
                    'winetricks', 'lutris'):
                yield package

        elif fedora_ver == '30':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/30/winehq.repo'
                )
            for package in (
                    'winehq-staging', 'vulkan-loader',
                    'vulkan-loader.i686', 'winetricks'):
                yield package

        else:
            print(
                "\n#########################################################"
                "\nOlder version of Fedora than Fedora 30 or 31 detected.",
                "\nPlease refer to https://wiki.winehq.org/Fedora ."
                "\n#########################################################"
                )
            raise SystemError("This version of Fedora not supported yet")

    def lutris(self):
        yield 'lutris'

    def steam(self):
        print("Adding the steam package")
        for command in (
                'dnf install -y fedora-workstation-repositories',
                'dnf install -y steam --enablerepo=rpmfusion-nonfree-steam'):
            self._top_commands.append(command)
        yield 'steam'

    def vkbasalt(self):
        self._after['vkbasalt_all'][0] = True
        for package in (
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel.i686', 'libstdc++-devel.i686',
                'spirv-tools', 'libX11-devel.i686'):
            yield package

    def gamemode(self):
        print(
            "Adding packages nesressary for building gamemode."
            )
        for package in (
                'meson', 'systemd-devel',
                'pkg-config', 'git dbus-devel'):
            yield package

    def install_script(self, install_programs):
        command = ['dnf', 'install', '-y']
        packages = list()
        for program in install_programs:
            packages += list(getattr(self, program)())

        self.create_install_script_all(
            [command, 2], packages, self._top_commands
            )


class Solus(All):
    __slots__ = (
        "_top_commands",
        "_after"
        )
    def __init__(self, gpu_vendor):
        self._top_commands = list()
        self._after = {'vkbasalt_all': [False, All]}
        super().__init__()

    def wine(self):
        for package in [
                'wine', 'wine-devel', 'wine-32bit-devel', 'winetricks',
                'vulkan, vulkan-32bit, vulkan-headers'
                ]:
            yield package

    def lutris(self):
        print("Adding lutris packages")
        yield 'lutris'

    def steam(self):
        for package in [
                'steam', 'linux-steam-integration'
                ]:
            yield package

    def vkbasalt(self):
        self._after['vkbasalt_all'][0] = True
        for package in [
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel', 'libstdc++', 'spirv-tools'
                ]:
            yield package

    def gamemode(self):
        for package in [
                'gamemode', 'gamemode-32bit']:
            yield package

    def install_script(self, install_programs):
        command = ['eopkg', 'install', '-y']
        packages = list()
        for program in install_programs:
            function = getattr(self, program)
            packages += list(function())
        self.create_install_script_all(
            [command, 2], packages, self._top_commands
            )


class Ubuntu(All):
    __slots__ = (
        "gpu_vendor",
        "_top_commands",
        "_after",
        "version"
        )

    def __init__(self, gpu_vendor):
        super().__init__()
        self.gpu_vendor = gpu_vendor
        self._top_commands = list()
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All, '-y']
            }
        self.version = distro.version()

    def lutris(self):
        self._top_commands.append(
            'add-apt-repository ppa:lutris-team/lutris'
            )
        yield "lutris"

    def wine(self):
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

        def amd_intel():
            self._top_commands.append("dpkg --add-architecture i386")
            yield "libgl1-mesa-dri:i386"
            for package in [
                    "mesa-vulkan-drivers",
                    "mesa-vulkan-drivers:i386"]:
                yield package

        def nvidia():
            raise GpuNotSupported(
                "This gpu is not supported yet for this program on the current",
                "distro. Please report this !"
                )

        if self.gpu_vendor == 'amd' or 'intel':
            amd_intel()
        else:
            nvidia()

    def steam(self):
        yield 'steam'

    def gamemode(self):
        for package in [
                'meson', 'libsystemd-dev',
                'pkg-config', 'ninja-build',
                'libdbus-1-dev', 'libinih-dev',
                'git', 'dbus-user-session'
                ]:
            yield package
        self._after['gamemode'][0] = True

    def install_script(self, install_programs):
        command = ['apt', 'install', '-y']
        packages = list()
        for program in install_programs:
            packages += list(getattr(self, program)())
        self.create_install_script_all(
            [command, 2], packages, self._top_commands
            )
