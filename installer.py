import subprocess
class Arch:
    def __init__(self):
        self.after = {'vkBasalt':[False, ]}}
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

    def lutris():
        import enableMultilib
        print("Trying to enable multilib in pacman.conf\n")
        enableMultilib.pacmanConf()

        print("Returning wine & lutris packages\n")
        return ['gamemode-git', 'lib32-gamemode-git', 'lutris-git', 'wine-staging', 'giflib', 'lib32-giflib', 'libpng', 'lib32-libpng', 'libldap', 'lib32-libldap', 'gnutls', 'lib32-gnutls', 'mpg123', 'lib32-mpg123', 'openal', 'lib32-openal', 'v4l-utils', 'lib32-v4l-utils', 'libpulse', 'lib32-libpulse', 'libgpg-error', 'lib32-libgpg-error', 'alsa-plugins', 'lib32-alsa-plugins', 'alsa-lib', 'lib32-alsa-lib', 'libjpeg-turbo', 'lib32-libjpeg-turbo', 'sqlite', 'lib32-sqlite', 'libxcomposite', 'lib32-libxcomposite', 'libxinerama', 'lib32-libgcrypt', 'libgcrypt', 'lib32-libxinerama', 'ncurses', 'lib32-ncurses', 'opencl-icd-loader', 'lib32-opencl-icd-loader', 'libxslt', 'lib32-libxslt', 'libva', 'lib32-libva', 'gtk3', 'lib32-gtk3', 'gst-plugins-base-libs', 'lib32-gst-plugins-base-libs', 'vulkan-icd-loader', 'lib32-vulkan-icd-loader']

    def steam():
        print("Returning steam package.\n")
        return ['steam', 'steam-native-runtime', 'proton-ge-custom']

    def vkBasalt(build=False):
        if after_download == False:
            print("downloading vkBasalt and installing necressary dependencies.\n")
            yield ['glslang', 'vulkan-tools', 'lib32-libx11', 'libx11']
            print("Downloading vkBasalt to ~/Programs")
            subprocess.Popen(('mkdir', '~/Programs'))
            subprocess.Popen(('wget', 'https://github.com/DadSchoorse/vkBasalt/releases/latest/download/vkBasalt.tar.gz', '-O', '~/Programs'))
        else:
            #configuration https://www.youtube.com/watch?v=6p1SNBy4P74&t=638s
            print("Building and configuring it like Chris Titus Tech did.\n")
            subprocess.Popen(('tar', '-xzvf', '-C', '~/Programs', '&&', 'rm', '~/Programs/vkBasalt.tar.gz'))
            subprocess.Popen(('cd', '~/Programs/vkBasalt', '&&', 'make', 'install'))
            with open('~/Programs/vkBasalt/config', 'rw') as FileObj:
                config = FileObj.readlines()
                for i, line in enumerate(config):
                    if line.startswith('effects ='):
                        config[i] = 'effects = smaa:smaa:cas'
                FileObj.writelines(config)
