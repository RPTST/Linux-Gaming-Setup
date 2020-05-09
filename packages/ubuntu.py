class GpuNotSupported: pass
class CachingProperty:
    def __init__(self, func):
        self.func = func
        self.value = None

    def __get__(self, obj, objtype):
        if self.value is None:
            self.value = self.func(obj)

        return self.value


class Ubuntu:
    def __init__(self):
        pass

    def pckg_lutris(self):
        yield "lutris"

    def pckg_wine(self):
        def amd_intel():
            for package in [
                    "mesa-vulkan-drivers",
                    "mesa-vulkan-drivers:i386",
                    "libgl1-mesa-dri:i386"]:
                yield package

        def nvidia():
            raise GpuNotSupported(
                "This gpu is not supported yet for this program on the current",
                "distro. Please report this !"
                )

        if self.gpu_vendor == "amd" or "intel":
            amd_intel()
        else:
            nvidia()

    def pckg_steam(self):
        yield "steam"

    def pckg_vkbasalt(self):
        for package in [
                "build-essential", "gcc-multilib",
                "libx11-dev", "libx11-dev:i386",
                "glslang-tools", "spirv-tools"
                ]:
            yield package

    def pckg_gamemode(self):
        for package in [
                'meson', 'libsystemd-dev',
                'pkg-config', 'ninja-build',
                'libdbus-1-dev', 'libinih-dev',
                'git', 'dbus-user-session'
                ]:
            yield package
