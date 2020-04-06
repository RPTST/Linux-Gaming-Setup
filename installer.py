import subprocess
class Installer:
    def __init__(self):
        self.yay_package = False

    # Arch
    def yay(self):
        packages = subprocess.getoutput("pacman --query").splitlines()
        for package in packages:
            if package.split()[0] in ["yay", "yay-bin", "yay-git"]:
                self.yay_package = True
                print("Yay found !")

    def ArchInstaller(self, to_install):
        if self.yay_package == False:
            print("yay not installed or not found !")
            quit
        else:
            pass
        if to_install:
            for program in to_install:
                dictionary.get(program)()

        def lutris():
            print("Installing wine and its dependencies")


            print("Installing dependencies for lutris-git.")

            print("Installing lutris app.")
            
        def steam():
            print("Installing steam.")

        def vkBasalt():
            print("installing vkBasalt.")

        def gamemode():
            print("Installing gamemode.")

        def linux_gc():
            print("Installing the gc kernel with bmq scheduler.")

        dictionary = {'lutris': lutris, 'steam': steam, 'vkbasalt': vkBasalt, 'gamemmode': gamemode}



a = Installer()
a.yay()
a.ArchInstaller(None)