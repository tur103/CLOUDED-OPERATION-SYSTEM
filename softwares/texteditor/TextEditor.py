from wx import *
from txt_constants import *
import sys
import os
import re


class TextEditor(App):
    def __init__(self):
        super(TextEditor, self).__init__()
        self.file_name = sys.argv[1]
        self.data = ""
        self.get_file_data()
        self.window = self.create_window()
        self.panel = Panel(self.window)
        self.horizontal_box = BoxSizer(VERTICAL)
        self.text_input = self.add_text_input()
        self.create_menu_bar()
        self.Bind(EVT_TEXT, self.on_text_enter, source=self.text_input)
        self.font = Font(15, DEFAULT, NORMAL, BOLD)
        self.add_title(CREDIT, (100, 700))
        self.window.Show(True)
        if not self.file_name:
            self.on_new("new")

    def get_file_data(self):
        if self.file_name == NULL:
            self.file_name = ""
        if self.file_name:
            file_handle = open(self.file_name, READING)
            self.data = file_handle.read()
            file_handle.close()
        else:
            self.data = ""

    def create_window(self):
        """

        Creating a wx window.

        Returns:
            Frame: The wx window frame.

        """
        window = Frame(None, title=TXT_TITLE + self.file_name, size=TXT_SIZE)
        window.Centre()
        icon = EmptyIcon()
        icon.CopyFromBitmap(Bitmap(TXT_ICON, BITMAP_TYPE_ANY))
        window.SetIcon(icon)
        return window

    def add_text_input(self):
        return TextCtrl(self.panel, pos=(0, 0), size=(1000, 680),
                        value=self.data, style=TE_MULTILINE | SUNKEN_BORDER)

    def add_title(self, title, pos):
        """

        Add a given title to the window by a given position.

        Args:
            title (string): The title to be written.
            pos (tuple): The coordinates in the window.

        """
        heading = StaticText(self.panel, label=title, pos=pos)
        heading.SetFont(self.font)

    def create_menu_bar(self):
        menu_bar = MenuBar()
        file_menu = Menu()
        new = file_menu.Append(ID_NEW, 'New', 'New file')
        self.Bind(EVT_MENU, self.on_new, new)
        open = file_menu.Append(ID_OPEN, 'Open', 'Open file')
        self.Bind(EVT_MENU, self.on_open, open)
        save_as = file_menu.Append(ID_SAVEAS, 'Save As', 'Save the file')
        self.Bind(EVT_MENU, self.on_save_as, save_as)
        exit = file_menu.Append(ID_EXIT, 'Quit', 'Quit application')
        self.Bind(EVT_MENU, self.on_quit, exit)
        menu_bar.Append(file_menu, '&File')
        edit_menu = Menu()
        undo = edit_menu.Append(ID_UNDO, 'Undo', 'Undo text')
        self.Bind(EVT_MENU, self.on_undo, undo)
        cut = edit_menu.Append(ID_CUT, 'Cut', 'Cut text')
        self.Bind(EVT_MENU, self.on_cut, cut)
        copy = edit_menu.Append(ID_COPY, 'Copy', 'Copy text')
        self.Bind(EVT_MENU, self.on_copy, copy)
        paste = edit_menu.Append(ID_PASTE, 'Paste', 'Paste text')
        self.Bind(EVT_MENU, self.on_paste, paste)
        delete = edit_menu.Append(ID_DELETE, 'Delete', 'Delete text')
        self.Bind(EVT_MENU, self.on_delete, delete)
        find = edit_menu.Append(ID_FIND, 'Find', 'Find text')
        self.Bind(EVT_MENU, self.on_find, find)
        menu_bar.Append(edit_menu, '&Edit')
        self.window.SetMenuBar(menu_bar)

    def on_quit(self, event):
        self.window.Close()

    def on_new(self, event):
        self.message_box()

    def on_open(self, event):
        dialog = FileDialog(self.window, "File Browser", "", "",
                            "Text files (*.txt)|*.txt",
                            wx.FD_FILE_MUST_EXIST)
        button = dialog.ShowModal()
        if button == ID_OK:
            self.file_name = dialog.GetPath()
            file_handle = open(self.file_name, READING)
            self.text_input.SetValue(file_handle.read())
            file_handle.close()
            self.window.SetTitle(TXT_TITLE + self.file_name)

    def on_save_as(self, event):
        entered = True
        while entered:
            message_box = TextEntryDialog(self.window, SAVE_AS_MESSAGE, SAVE_AS_TITLE, defaultValue=NEW_FILE)
            button = message_box.ShowModal()
            if button == ID_OK:
                file_name = message_box.GetValue() + TXT_EXT
                folder = "\\".join(os.path.abspath(__file__).split("\\")[:-2] + [SYSTEM_FOLDER, file_name])
                try:
                    file_handle = open(folder, REGULAR_WRITING)
                    file_handle.write(self.data)
                    file_handle.close()
                    entered = False
                    self.file_name = folder
                    self.window.SetTitle(TXT_TITLE + folder)
                except IOError:
                    pass
            else:
                entered = False

    def on_undo(self, event):
        self.text_input.Undo()

    def on_cut(self, event):
        text = self.text_input.FindFocus()
        if text:
            text.Cut()

    def on_copy(self, event):
        text = self.text_input.FindFocus()
        if text:
            text.Copy()

    def on_paste(self, event):
        self.text_input.Paste()

    def on_delete(self, event):
        frm, to = self.text_input.GetSelection()
        self.text_input.Remove(frm, to)

    def on_find(self, event):
        message_box = TextEntryDialog(self.window, FIND_MESSAGE, FIND_TITLE,
                                      defaultValue=self.text_input.GetStringSelection())
        button = message_box.ShowModal()
        if button == ID_OK:
            text_to_search = message_box.GetValue()
            if text_to_search:
                text = self.text_input.GetValue()
                findings = []
                for match in re.finditer(text_to_search, text):
                    word_line = len(text[:match.start()].split("\n")) - 1
                    findings.append((match.start(), match.end(), word_line))
                cursor = self.text_input.GetInsertionPoint()
                cursor_line = len(self.text_input.GetRange(0, self.text_input.GetInsertionPoint()).split("\n")) - 1
                cursor -= cursor_line
                for find in findings:
                    if find[1] >= cursor:
                        current_line = find[2]
                        self.text_input.SetSelection(find[0] + current_line, find[1] + current_line)
                        break

    def message_box(self):
        entered = True
        while entered:
            message_box = TextEntryDialog(self.window, NEW_FILE_MESSAGE, NEW_FILE_TITLE, defaultValue=NEW_FILE)
            button = message_box.ShowModal()
            if button == ID_OK:
                file_name = message_box.GetValue() + TXT_EXT
                folder = "\\".join(os.path.abspath(__file__).split("\\")[:-2] + [SYSTEM_FOLDER, file_name])
                try:
                    file_handle = open(folder, REGULAR_WRITING)
                    file_handle.close()
                    entered = False
                    self.file_name = folder
                    self.text_input.Clear()
                    self.window.SetTitle(TXT_TITLE + folder)
                except IOError:
                    pass
            else:
                entered = False

    def on_text_enter(self, event):
        data = event.GetString()
        file_handle = open(self.file_name, REGULAR_WRITING)
        self.data = data
        file_handle.write(self.data)


app = TextEditor()
app.MainLoop()
