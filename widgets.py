import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os


class ProgramBox(Gtk.VBox):
    def __init__(self, program_name, option):
        Gtk.Box.__init__(self)
        self.program_name = program_name
        self.get_func_by_opt(option)

    @property
    def new_toggle_button(self):
        btn = Gtk.ToggleButton("Install")
        btn.set_name(self.program_name)
        return btn

    @property
    def new_button(self):
        btn = Gtk.Button("Install")
        btn.set_name(self.program_name)
        return btn

    def get_func_by_opt(self, option):
        options = {
            'click_install': self.toggle_install,
            'show_releases': self.choose_install
            }
        options.get(option)()

    def toggle_install(self):
        label = Gtk.Label(self.program_name)
        self.button = self.new_toggle_button
        self.pack_start(label, False, False, 0)
        self.pack_end(self.button, False, False, 0)

    def choose_install(self):
        label = Gtk.Label(self.program_name)
        self.button = self.new_button
        self.pack_start(label, False, False, 0)
        self.pack_end(self.button, False, False, 0)


class FlowBox(Gtk.FlowBox):
    """
    FlowBox element which is used for program boxes
    """
    def __init__(self, _class):
        Gtk.FlowBox.__init__(self)
        self.set_homogeneous(False)
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_min_children_per_line(0)
        self.set_max_children_per_line(5)

        self.add_programs(_class)

    def add_programs(self, _class):
        toggle_programs = _class.toggle_programs
        popout_programs = _class.popout_programs
        if toggle_programs:
            for _program in toggle_programs:
                _box = ProgramBox(_program, 'click_install')
                self.add(_box)
                toggle_programs[_program] = _box.button

        if popout_programs:
            for _program in popout_programs:
                _box = ProgramBox(_program, 'show_releases')
                self.add(_box)
                popout_programs[_program][1] = _box.button


class MessageDialog(Gtk.Dialog):
    """
    Used to make message window to warn the user
    """
    def __init__(self, parent, title, message):
        Gtk.Dialog.__init__(
            self,
            title,
            parent,
            0,
            (
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
                ),
            )

        self.set_default_size(140, 100)
        label = Gtk.Label(message)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class MultipleReleases(Gtk.Window):  # fixme
    """
    Window to install different version of the program.
    Currently used only for proton-ge.
    """
    def __init__(self, program_name, json_onjects):
        Gtk.Window.__init__(self)
        self.set_title = program_name

    def return_body(self):
        vbox = Gtk.VBox()