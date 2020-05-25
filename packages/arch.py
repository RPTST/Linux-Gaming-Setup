class CachingProperty:
    def __init__(self, func):
        self.func = func
        self.value = None

    def __get__(self, obj, objtype):
        if self.value is None:
            self.value = self.func(obj)

        return self.value


class Arch:
    def __init__(self):
        pass

    @CachingProperty
    def pckg_wine(self):
        for package in [
            "lib32-opencl-icd-loader",
            "libpng",
            "gnutls",
            "wine-staging",
            "giflib",
            "lib32-giflib",
            "libpulse",
            "lib32-libpng",
            "libldap",
            "lib32-libldap",
            "lib32-gnutls",
            "mpg123",
            "lib32-mpg123",
            "openal",
            "lib32-openal",
            "v4l-utils",
            "lib32-v4l-utils",
            "lib32-libpulse",
            "libgpg-error",
            "lib32-libgpg-error",
            "alsa-plugins",
            "lib32-alsa-plugins",
            "alsa-lib",
            "gtk3" "lib32-alsa-lib",
            "libjpeg-turbo",
            "lib32-libjpeg-turbo",
            "sqlite",
            "lib32-sqlite",
            "libxcomposite",
            "lib32-gtk3",
            "libxinerama",
            "lib32-libgcrypt",
            "libgcrypt",
            "ncurses",
            "lib32-ncurses",
            "opencl-icd-loader",
            "libxslt",
            "lib32-libxslt",
            "libva",
            "lib32-libva",
            "gst-plugins-base-libs",
            "lib32-gst-plugins-base-libs",
            "lib32-vulkan-icd-loader",
            "lib32-libxcomposite",
            "lib32-libxinerama",
            "vulkan-icd-loader",
        ]:
            yield package

    @CachingProperty
    def pckg_lutris(self):
        yield "lutris-git"

        def amd():
            """
            Returns Vulkan packages for Amd gpus
            """
            return [
                "lib32-mesa",
                "vulkan-radeon",
                "lib32-vulkan-radeon",
                "vulkan-icd-loader",
                "lib32-vulkan-icd-loader",
            ]

        def nvidia():
            """
            Returns Vulkan packages for Nvidia gpus
            """
            return [
                "nvidia",
                "nvidia-utils",
                "lib32-nvidia-utils",
                "nvidia-settings",
                "vulkan-icd-loader",
                "lib32-vulkan-icd-loader",
            ]

        def intel():
            """
            Returns packages Vulkan packages for Intel igpus
            """
            return [
                "lib32-mesa",
                "vulkan-intel",
                "lib32-vulkan-intel",
                "vulkan-icd-loader",
                "lib32-vulkan-icd-loader",
            ]

        vulkan = {"amd": amd, "intel": intel, "nvidia": nvidia}
        for vulkan_package in vulkan.get(self.gpu_vendor)():  # for vulkan support
            yield vulkan_package

    @CachingProperty
    def pckg_steam(self):
        for package in ["steam-native-runtime", "steam"]:
            yield package

    @CachingProperty
    def pckg_vkbasalt(self):
        for package in ["glslang", "vulkan-tools", "lib32-libx11", "libx11"]:
            yield package

    @CachingProperty
    def pckg_gamemode(self):
        for package in ["meson", "systemd", "git", "dbus"]:
            yield package
