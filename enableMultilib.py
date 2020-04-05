import os


def pacmanConf():
    print("\nenableMultilib.py executed.")
    try:
        with open('/etc/pacman.conf', 'r') as file:
            data = file.readlines()
        for i, line in enumerate(data):
            if line.startswith("#[multilib]"):
                data[i] = "[multilib]\n"
                data[i+1] = "SigLevel = PackageRequired\n"
                data[i+2] = "Include = /etc/pacman.d/mirrorlist\n"
                os.system("sudo pacman -Syu")
            elif line == "[multilib]\n":
                print("""   Seems like multilib it's already uncommented, to be sure you can check it on /etc/pacman.conf
                            You can check this site for know more about enabling multilib:
                            https://www.linuxsecrets.com/archlinux-wiki/wiki.archlinux.org/index.php/Multilib.html\n
                            """)
                break
            else:
                print(
                        """
                        Either multilib is already enabled, or the script can't find it on your /etc/pacman.conf file.
                        You can check this site for know more about enabling multilib:
                        https://www.linuxsecrets.com/archlinux-wiki/wiki.archlinux.org/index.php/Multilib.html
                        """)
                break

        with open('/etc/pacman.conf', 'w') as file:
            file.writelines(data)
    except PermissionError:
        print("enableMultilib.py wasnt executed as root !\n\n")
