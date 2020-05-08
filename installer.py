import subprocess
import os
import shutil
import inspect
import distro
import multi
from packages import arch, fedora, solus, ubuntu


class PackageNotFound(Exception): pass


class GpuNotSupported(Exception): pass


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
        subprocess.Popen(
            (
                'make', f'{self.programs_folder}/tmp/vkBasalt',
                'install'
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
        if os.path.isdir(os.path.expanduser('~/.steam')):
            os.makedirs(os.path.expanduser('~/.steam/root/compatibilitytools.d'))
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
        cmd = ' '.join(command)
        return cmd

    def create_install_script_all(self, create_icmd, _packages):
        """
        Creates the install.sh file
        """
        if _packages:
            install_cmd = All.create_install_cmd_all(
                create_icmd[0],
                create_icmd[1],
                _packages
                )

        if self.__class__.__name__ == 'Arch':
            print("Arch installer script")
            with open(self.current_folder + 'install.sh', 'a') as script_file:
                script_file.write("echo 'Install script executed'\n")
                if _packages:
                    script_file.write(install_cmd + "\n")
                    script_file.write('pkexec sh _top_commands')

        else:
            print("Installer script for all other distros")
            with open(self.current_folder + 'install.sh', 'a') as script_file:
                script_file.write("echo 'Install script executed'\n")
                _top_commands = self._top_commands
                if _top_commands:
                    script_file.write("echo 'Top command/s executed'\n")
                    for _top_cmd in _top_commands:
                        print(_top_cmd)
                        script_file.write(_top_cmd + '\n')
                if _packages:
                    script_file.write("echo 'Packages are being downloaded'\n")
                    script_file.write(install_cmd + '\n')


class Arch(All, arch.Arch):
    __slots__ = (
        "gpu_vendor",
        "_top_commands",
        "_after",
        )

    def __init__(self, gpu_vendor):
        super().__init__()
        self.gpu_vendor = gpu_vendor
        self._top_commands = list()
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All]
            }
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

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True

    def gamemode(self):
        self._after['gamemode'][0] = True

    def install_script(self, install_programs):
        command = [
            'yay', '-S', '--redownloadall', '--nosudoloop',
            '--nocleanmenu', '--nodiffmenu', '--noeditmenu',
            '--sudo', 'pkexec'
            ]
        packages = list()
        for program_name in install_programs:
            try:
                program_packages = list(getattr(self, 'pckg_' + program_name)())
                getattr(self, program_name)()

            except AttributeError:
                pass
            packages += program_packages
        self.create_install_script_all(
            [command, 2], packages, self._top_commands
            )


class Fedora(All, fedora.Fedora):
    __slots__ = (
        "_top_commands",
        "_after",
        "gpu_vendor",
        "fedora_ver"
        )
    def __init__(self, gpu_vendor):
        super().__init__()
        self._top_commands = list()
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All]
            }
        self.gpu_vendor = None
        self.fedora_ver = float(distro.version())

    def wine(self):
        if self.fedora_ver == '31':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/31/winehq.repo'
                )

        elif self.fedora_ver == '30':
            self._top_commands.append(
                'dnf config-manager --add-repo' +
                'https://dl.winehq.org/wine-builds/fedora/30/winehq.repo'
                )
        else:
            print(
                "\n#########################################################"
                "\nOlder version of Fedora than Fedora 30 or 31 detected.",
                "\nPlease refer to https://wiki.winehq.org/Fedora ."
                "\n#########################################################"
                )
            raise SystemError("This version of Fedora not supported yet")

    def steam(self):
        for command in (
                'dnf install -y fedora-workstation-repositories',
                'dnf install -y steam --enablerepo=rpmfusion-nonfree-steam'):
            self._top_commands.append(command)

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True

    def gamemode(self):
        self._after['gamemode'][0] = True

    def install_script(self, install_programs):
        command = ['dnf', 'install', '-y']
        packages = list()
        for program_name in install_programs:
            try:
                program_packages = getattr(self, 'pckg_' + program_name)
                packages += list(program_packages)

            except AttributeError:
                getattr(self, program_name)()

        self.create_install_script_all(
            [command, 2], packages
            )


class Solus(All, solus.Solus):
    __slots__ = (
        "_top_commands",
        "_after"
        )
    def __init__(self, gpu_vendor):
        self._top_commands = list()
        self._after = {
            'vkbasalt': [False, All],
            'gamemode': [False, All]
            }
        super().__init__()

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True

    def gamemode(self):
        self._after['gamemode'][0] = True

    def install_script(self, install_programs):
        command = ['eopkg', 'install', '-y']
        packages = list()
        for program_name in install_programs:
            try:
                program_packages = getattr(self, 'pckg_' + program_name)
                packages += list(program_packages)
                
            except AttributeError:
                getattr(self, program_name)()
            
        self.create_install_script_all(
            [command, 2], packages
            )


class Ubuntu(All, ubuntu.Ubuntu):
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
            'gamemode': [False, All]
            }
        self.version = distro.version()

    def lutris(self):
        self._top_commands.append(
            'add-apt-repository ppa:lutris-team/lutris'
            )

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

    def vkbasalt(self):
        self._after['vkbasalt'][0] = True

    def gamemode(self):
        self._after['gamemode'][0] = True

    def install_script(self, install_programs):
        command = ['apt', 'install', '-y']
        packages = list()
        for program_name in install_programs:
            try:
                program_packages = getattr(self, 'pckg_' + program_name)
                packages += list(program_packages)

            except AttributeError:
                getattr(self, program_name)()
        self.create_install_script_all(
            [command, 2], packages,
            )
