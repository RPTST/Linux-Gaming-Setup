import os
import os.path
import tempfile
import shutil
import sys

__all__ = ("pacmanConf",)


def _pacmanConf(path="/etc/pacman.conf"):
    with open(path, "r") as file:
        data = file.readlines()

    if "[multilib]\n" in data:
        return 0

    for i, line in enumerate(data):
        if line.startswith("#[multilib]"):
            data[i] = "[multilib]\n"
            data[i + 1] = "Include = /etc/pacman.d/mirrorlist\n"
            break
    else:
        return 1

    with tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(path), delete=False
    ) as tmp_file:
        tmp_file.writelines(data)
    shutil.copystat(path, tmp_file.name, follow_symlinks=False)
    shutil.copyfile(path, path + ".backup")
    os.rename(tmp_file.name, path)

    return 2


def pacmanConf():
    print("\nrunning enableMultilib().")
    try:
        enabled_multilib = _pacmanConf()
    except PermissionError:
        print("enableMultilib.py wasnt executed as root!\n\n", file=sys.stderr)
        return

    if enabled_multilib == 0:
        print(
            """
Seems like multilib is already uncommented, to be sure you can check it in /etc/pacman.conf.
You can check this site for more info about enabling multilib:
https://www.linuxsecrets.com/archlinux-wiki/wiki.archlinux.org/index.php/Multilib.html\n
              """.strip()
        )
    elif enabled_multilib == 1:
        print(
            """
Either multilib is already enabled, or the script can't find it in your /etc/pacman.conf file.
You can check this site for more info about enabling multilib:
https://www.linuxsecrets.com/archlinux-wiki/wiki.archlinux.org/index.php/Multilib.html\n
              """.strip()
        )
    else:
        assert enabled_multilib == 2

    exit_code = os.spawnv(os.P_WAIT, "pacman", ("-Syu",))
    if exit_code != 0:
        print("error: pacman returned non-zero exit code (%i)" % (exit_code,))
