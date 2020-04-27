import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import os
import webbrowser
import distro
import installer
import info
import widgets


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
        print("Button clicked")
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
        to_reset = self.window.get_active_toggle_btn()
        toggle_programs = self.window.toggle_programs
        for program_name in to_reset:
            btn_obj = toggle_programs.get(program_name)
            btn_obj.set_active(False)
        

    def install(self, *args):
        distro_class = self.window.distro_class()
        distro_class.gpu_vendor = self.window.gpu_vendor.lower()
        to_install = self.window.get_active_toggle_btn()
        for _program in to_install:
            program = _program.replace('-', '_').lower()
            function = getattr(distro_class, program)
            print(function)
            function()


class Window(Gtk.ApplicationWindow):
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

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)
        self.set_urgency_hint(True)
        self._app_init()
        self.set_default_size(400, 100)

    def _app_init(self):
        self.variables()
        self.headerbar()
        self.body()
        self.menu_popover()
        self.set_gpu_vendor()

    def variables(self):
        self.handler = Handler(self)
        self.current_path = (
            os.path.dirname(os.path.abspath(__file__)) + '/'
            )
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.current_path + 'ui.glade')
        self.builder.connect_signals(
            self.handler
            )
        self.toggle_programs = {
            'Lutris': None,
            'Steam': None,
            'vkBasalt': None,
            'Gamemode': None
            }
        self.popout_programs = {
            'Proton-Ge': [
                'https://api.github.com/repos/GloriousEggroll/' +
                'proton-ge-custom/releases',
                None
                ]
            }


    def headerbar(self):
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        self.set_titlebar(header_bar)

        self.menu_button = Gtk.MenuButton()
        icon = Gio.ThemedIcon(name="view-more")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.menu_button.add(image)
        header_bar.pack_end(self.menu_button)

    def body(self):
        vbox = Gtk.VBox()
        vbox.set_homogeneous(False)
        flowbox = widgets.FlowBox(self)
        vbox.pack_start(flowbox, False, True, 0)

        def do_buttons_box():
            button_reset = Gtk.Button("Reset")
            button_reset.connect("clicked", self.handler.reset)

            button_install = Gtk.Button("Install")
            button_install.connect("clicked", self.handler.install)

            do_buttons_box = Gtk.HBox()
            do_buttons_box.pack_start(button_reset, True, True, 0)
            do_buttons_box.pack_end(button_install, True, True, 0)
            return do_buttons_box
        vbox.pack_end(do_buttons_box(), False, False, 0)
        
        self.add(vbox)

    
    def get_active_toggle_btn(self):
        """
        Gets programs to install by checking if the
        toggle button is active or not.
        """
        programs = list()
        for button_obj in self.toggle_programs.values():
            if button_obj.get_active():
                program_name = button_obj.get_name().replace('-', '_')
                programs.append(program_name)
        return programs

    def menu_popover(self):
        popover = self.builder.get_object('menu_popover')
        self.menu_button.set_popover(popover)

    def set_gpu_vendor(self):
        if self.gpu_vendor == 'unknown':
            dialog = widgets.MessageDialog(
                self,
                title="Warning",
                message=(
                    "You will have to select ur gpu vendor manually" +
                    "by clicking on the menu button and select it form the combo button")
                )
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
        else:
            select_vendor_button = self.builder.get_object(
                'select_gpu_vendor'
                )
            select_vendor_button.set_active_id(
                self.gpu_vendor)

    def multiple_rel_programs(self):
        """
        Makes the window to choose which versions
        of the program u want to install (example: proton-ge)
        """
