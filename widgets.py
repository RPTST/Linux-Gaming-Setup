import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
import os
import time
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
        # _class = Window
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
                btn_obj = _box.button
                popout_programs[_program][1] = btn_obj
                self.add(_box)
                btn_obj.connect("clicked", _class.handler.choose_release)

                # create the version selector window
                api_link = popout_programs[_program][0]
                selector, tree_store = _class.create_ver_selector(
                    api_link, _program
                    )
                popout_programs[_program][2] = selector
                popout_programs[_program][3] = tree_store

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
        label = Gtk.Label(message)
        label.set_line_wrap_mode(Gtk.WrapMode.CHAR)
        box = self.get_content_area()
        box.add(label)
        self.set_default_size(120, 100)
        self.show()


class ReleaseSelector(Gtk.ApplicationWindow):
    """
    Window to install different version of the program.
    Currently used only for proton-ge.
    """
    def __init__(self, program_name, json_objects, handler):
        Gtk.Window.__init__(self)
        self.set_deletable(False)
        self.set_decorated(False)
        self.program_name = program_name
        self.json_objects = json_objects
        self.handler = handler
        self.hide_on_delete()
        self.set_default_size(250, 300)

        self.set_title = ("Manage", program_name, "versions")
        self.tree_view = TreeView(self.json_objects)

        self.add(self.body())

    def body(self):
        def top_label():
            label = Gtk.Label()
            text = self.program_name + " version managment."
            label.set_text(text)
            return label

        def scroll_tree_view():
            scrolled_win = Gtk.ScrolledWindow()
            scrolled_win.add(self.tree_view)
            return scrolled_win

        def bottom_button():
            button = Gtk.Button("OK")
            button.connect("clicked", self.on_destroy)
            button.set_halign(Gtk.Align.END)
            return button

        box = Gtk.VBox()
        box.pack_start(top_label(), False, True, 0)
        box.pack_start(scroll_tree_view(), True, True, 0)
        box.pack_end(bottom_button(), False, False, 0)
        return box

    def on_destroy(self, window):
        self.hide()



class TreeView(Gtk.TreeView):
    def __init__(self, json_objects):
        Gtk.TreeView.__init__(self)
        self.data_objects = json_objects
        self.store = self.list_store()
        self.set_model(self.store)
        self.set_columns_renderers()

    def set_columns_renderers(self):
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("", renderer_toggle, active=0)
        self.append_column(column_toggle)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Release", renderer_text, text=1)
        self.append_column(column_text)

        renderer_release_type = Gtk.CellRendererText()
        column_release_type = Gtk.TreeViewColumn("Prelease ?", renderer_release_type, text=2)
        self.append_column(column_release_type)

    def list_store(self):
        _list_store = Gtk.ListStore(bool, str, str)
        for data_object in self.data_objects:
            check_button = Gtk.CheckButton()
            tag_name = data_object.get('tag_name')
            check_button.set_name(tag_name)
            release = data_object.get('prerelease')
            _list_store.append([
                    False, str(tag_name), str(release)
                    ]
                )
        return _list_store

    def on_cell_toggled(self, widget, path):
        self.store[path][0] = not self.store[path][0]


class DownloadingStatus(Gtk.ApplicationWindow):
    pass