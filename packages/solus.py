class CachingProperty:
    def __init__(self, func):
        self.func = func
        self.value = None

    def __get__(self, obj, objtype):
        if self.value is None:
            self.value = self.func(obj)

        return self.value


class Solus:
    def __init__(self):
        pass

    def pckg_wine(self):
        for package in [
                'wine', 'wine-devel', 'wine-32bit-devel', 'winetricks',
                'vulkan, vulkan-32bit, vulkan-headers'
                ]:
            yield package

    def pckg_lutris(self):
        print("Adding lutris packages")
        yield 'lutris'

    def pckg_steam(self):
        for package in [
                'steam', 'linux-steam-integration'
                ]:
            yield package

    def pckg_vkbasalt(self):
        for package in [
                'vulkan-tools', 'glslang', 'libX11-devel',
                'glibc-devel', 'libstdc++', 'spirv-tools'
                ]:
            yield package
