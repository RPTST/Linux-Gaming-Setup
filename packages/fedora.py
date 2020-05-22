class CachingProperty:
    def __init__(self, func):
        self.func = func
        self.value = None

    def __get__(self, obj, objtype):
        if self.value is None:
            self.value = self.func(obj)

        return self.value


class Fedora:
    def __init__(self):
        pass

    @CachingProperty
    def pckg_wine(self):
        if self.fedora_ver == "31":
            for package in (
                "winehq-staging",
                "vulkan-loader",
                "vulkan-loader.i686",
                "winetricks",
                "lutris",
            ):
                yield package
        elif self.fedora_ver == "30":
            for package in (
                "winehq-staging",
                "vulkan-loader",
                "vulkan-loader.i686",
                "winetricks",
            ):
                yield package

    @CachingProperty
    def pckg_lutris(self):
        yield "lutris"

    def pckg_vkbasalt(self):
        for package in (
            "vulkan-tools",
            "glslang",
            "libX11-devel",
            "glibc-devel.i686",
            "libstdc++-devel.i686",
            "spirv-tools",
            "libX11-devel.i686",
        ):
            yield package

    @CachingProperty
    def pckg_gamemode(self):
        for package in ("meson", "systemd-devel", "pkg-config", "git dbus-devel"):
            yield package
