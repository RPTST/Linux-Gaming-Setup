import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import webbrowser
import installer
import distro
import program_dict


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
    def reset():
        pass # fixme

    def install(self, *args):
        distro_class = self.window.distro_class
        for program in self.window.programs:
            button_object = self.window.builder.get_object(program)
            if button_object.get_active:
                function = getattr(
                distro_class, program.replace('-', '_').lower()
                )
                print(function)
                

class Window:
    def __init__(self):
        self.handler = Handler(self)
        self.current_path = (
            f"{os.path.dirname(os.path.abspath(__file__))}/"
            )
        self._gtk_init()
        self.objects_and_vars()
        self.programs_flowb()
        
    @property
    def distro_class(self):
        """
        Gets the appropiate class to install programs
        """
        print(self.programs)
        def print_name(name):
            print("Your distro is/based on: " + name)

        if distro.like() == 'debian':
            if distro.id() == 'ubuntu':
                distribution = installer.Ubuntu
                print_name(distribution.__name__)
                return distribution()
        else:
            distribution =  getattr(installer, distro.like().capitalize())
            print_name(distribution.__name__)
            return distribution()

    def _gtk_init(self):
        """
        Sets some variables needed for the app
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_file(f'{self.current_path}ui.glade')
        
        self.builder.connect_signals(
            self.handler
            )
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(f'{self.current_path}style.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        self.window = self.builder.get_object('app_window')

    def objects_and_vars(self):
        self.refresh_btn  = self.builder.get_object(
            'refresh_everything'
            )
        self.menu_button = self.builder.get_object(
            'menu_button'
            )
        self.programs = [
            'lutris', 'steam', 'vkBasalt',
            'proton-ge', 'gamemode'
            ]
    def programs_flowb(self):
        program_flowb = self.builder.get_object('program_flowb')
        test = {}
        def box(program_name):
            vbox = Gtk.VBox()
            vbox.pack_start(Gtk.Label(program_name.capitalize()), True, True, 0)
            install_btn = Gtk.ToggleButton("Install")
            
            install_btn.set_name(program_name)
            vbox.pack_end(install_btn, True, True, 0)
            return vbox

        for program in self.programs:
            _box = box(program)
            program_flowb.add(_box)
            test[program] = _box

    def show_all(self):
        """
        Starts the app
        """
        print("Application started")
        self.window.show_all()
        Gtk.main()