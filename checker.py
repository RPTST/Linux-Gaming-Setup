import os
import subprocess
import vdf


class All:
    @staticmethod
    def vkbasalt_all():
        path = os.path.expanduser("~/.local/share/vkBasalt/vkBasalt.conf")
        if path:
            return True
        return False

    @staticmethod
    def gamemode_all():
        try:
            subprocess.Popen(
                ("gamemoderun"),
                stdout=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).wait()
            return True

        except FileNotFoundError:
            return False

    @staticmethod
    def proton_ge():
        installed_releases = list()
        path = os.path.expanduser("~/.local/share/Steam/compatibilitytools.d")
        releases_list = os.listdir(path)

        def check_proton_inf(current_rel):
            with open(f"{path}/{current_rel}/compatibilitytool.vdf", "r") as file_obj:
                _data = file_obj.read()
                data_dict = vdf.loads(_data)
                tag_name = data_dict.get("compatibilitytools").get("compat_tools")
                tag_name = list(tag_name)[0]
            if tag_name == current_rel:
                return True
            return False

        def get_releases():
            nonlocal installed_releases

            for _release in releases_list:
                release = _release.replace("Proton-", "")
                print(
                    "Detected a folder that should be a",
                    "proton release with the tag name:",
                    release,
                )
                assert check_proton_inf(_release)
                installed_releases.append(release)

        if releases_list:
            get_releases()
            return installed_releases
