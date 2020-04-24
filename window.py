import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import os
import webbrowser
import distro
import installer
import info


class Handler:
    """
    This class is a handler class as the name says.
    The functions to be executed depending on a signal
    can be found by opening ui.glade with Glade
    """
    def __init__(self, Window_obj):
        self.window = Window_obj

    def on_destroy(self, *args):
        print('quitting')
        Gtk.main_quit()

    def refresh(self, *args):
        if self.window.refresh_btn.get_active():
            print('refreshed')

    def self_github_page(self, *args):
        webbrowser.open_new(
            'https://github.com/RubixPower/Linux-Gaming-Setup'
            )

    def lutris_page(self, *args):
        webbrowser.open_new(
            'https://lutris.net/'
            )

    def lutris_github(self, *args):
        webbrowser.open_new(
            'https://github.com/lutris/lutris'
            )
    def reset(self, *args):
        pass # fixme

    def install(self, *args):
        distro_class = self.window.distro_class()
        to_install = self.window.programs_to_install()
        for _program in to_install:
            program = _program.replace('-', '_').lower()
            function = getattr(distro_class, program)
            print(function)
            function()

class Window:
    def __init__(self):
        self.handler = Handler(self)
        self.current_path = (
            os.path.dirname(os.path.abspath(__file__)) + '/'
            )
        self._app_init()
        self.toggle_programs = dict()
        self.popout_programs = dict()

    @property
    def distro_class(self):
        """
        Gets the appropiate class to install programs
        """
        def print_name(name):
            print("Your distro is/based on: " + name)

        if distro.like() == 'debian':
            if distro.id() == 'ubuntu':
                distribution = installer.Ubuntu
                print_name(distribution.__name__)
                return distribution
        else:
            distribution = getattr(installer, distro.like().capitalize())
            print_name(distribution.__name__)
            return distribution

    @property
    def gpu_vendor(self):
        return info.GraphicsCard().vendor

    def _app_init(self):
        """
        Sets some variables needed for the app
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.current_path + 'ui.glade')

        self.builder.connect_signals(
            self.handler
            )
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(self.current_path + 'style.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        self.window = self.builder.get_object('app_window')

        # Function needed to be executed
        self.set_gpu_vendor()
        self.objects_and_vars()
        self.programs_flowb()

    def set_gpu_vendor(self):
        """
        Tries to detect the gpu vendor and set the value in popover menu
        """
        combo_box = self.builder.get_object('gpu_vendor')
        combo_box.set_active_id(self.gpu_vendor)

    def objects_and_vars(self):
        self.menu_button = self.builder.get_object(
            'menu_button'
            )
        self.toggle_programs = {
            'Lutris': None,
            'Steam': None,
            'vkBasalt': None,
            'Gamemode': None
            }
        self.popout_programs = {
            'Proton-Ge': None
            }

    def programs_to_install(self):
        """
        Gets programs to install by checking if the
        toggle button is active or not.
        """
        programs = list()
        for button_obj in self.toggle_programs.values():
            if button_obj.get_active():
                program_name = button_obj.get_name().replace('-', '_')
                program_name = program_name.lower()
                programs.append(program_name)
        return programs

    def programs_flowb(self):
        program_flowb = self.builder.get_object('program_flowb')
        def box(program_name, toggle_btn):
            if toggle_btn:
                vbox = Gtk.VBox()
                vbox.pack_start(Gtk.Label(program_name), True, True, 0)
                install_btn = Gtk.ToggleButton("Install")
                install_btn.set_name(program_name)

                vbox.pack_end(install_btn, True, True, 0)

            else:
                vbox = Gtk.VBox()
                vbox.pack_start(Gtk.Label(program_name), True, True, 0)
                install_btn = Gtk.Button("Choose")
                install_btn.set_name(program_name)
                # install_btn.connect(program_name)

                vbox.pack_end(install_btn, True, True, 0)

            return vbox, install_btn

        for program in self.toggle_programs:
            _box, button_obj = box(program, True)
            program_flowb.add(_box)
            self.toggle_programs[program] = button_obj
        for program in self.popout_programs:
            _box, button_obj = box(program, False)
            program_flowb.add(_box)
            self.popout_programs[program] = button_obj

    def show_all(self):
        """
        Starts the app
        """
        print("Application started")
        self.window.show_all()
        Gtk.main()
