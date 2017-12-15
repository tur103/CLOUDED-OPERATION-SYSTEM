from wx import *
from txt_constants import *
import sys
import os
import re
from datetime import datetime


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
                        value=self.data, style=TE_MULTILINE | SUNKEN_BORDER | TE_RICH)

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
        replace = edit_menu.Append(ID_REPLACE, 'Replace', 'Replace text')
        self.Bind(EVT_MENU, self.on_replace, replace)
        replace_all = edit_menu.Append(ID_REPLACE_ALL, 'Replace All', 'Replace All text')
        self.Bind(EVT_MENU, self.on_replace_all, replace_all)
        select_all = edit_menu.Append(ID_SELECTALL, 'Select All', 'Select All text')
        self.Bind(EVT_MENU, self.on_select_all, select_all)
        time_and_date = edit_menu.Append(ID_OK, 'Time/Date', 'Display Time And Date')
        self.Bind(EVT_MENU, self.on_time_and_date, time_and_date)
        menu_bar.Append(edit_menu, '&Edit')
        style_menu = Menu()
        foreground_color = Menu()
        black_foreground = foreground_color.Append(ID_ANY, 'Black', 'Black Text')
        self.Bind(EVT_MENU, self.on_black_foreground, black_foreground)
        blue_foreground = foreground_color.Append(ID_ANY, 'Blue', 'Blue Text')
        self.Bind(EVT_MENU, self.on_blue_foreground, blue_foreground)
        green_foreground = foreground_color.Append(ID_ANY, 'Green', 'Green Text')
        self.Bind(EVT_MENU, self.on_green_foreground, green_foreground)
        cyan_foreground = foreground_color.Append(ID_ANY, 'Cyan', 'Cyan Text')
        self.Bind(EVT_MENU, self.on_cyan_foreground, cyan_foreground)
        navy_foreground = foreground_color.Append(ID_ANY, 'Navy', 'Navy Text')
        self.Bind(EVT_MENU, self.on_navy_foreground, navy_foreground)
        dark_grey_foreground = foreground_color.Append(ID_ANY, 'Dark Grey', 'Dark Grey Text')
        self.Bind(EVT_MENU, self.on_dark_grey_foreground, dark_grey_foreground)
        indian_red_foreground = foreground_color.Append(ID_ANY, 'Indian Red', 'Indian Red Text')
        self.Bind(EVT_MENU, self.on_indian_red_foreground, indian_red_foreground)
        violet_foreground = foreground_color.Append(ID_ANY, 'Violet', 'Violet Text')
        self.Bind(EVT_MENU, self.on_violet_foreground, violet_foreground)
        grey_foreground = foreground_color.Append(ID_ANY, 'Grey', 'Grey Text')
        self.Bind(EVT_MENU, self.on_grey_foreground, grey_foreground)
        dark_slate_blue_foreground = foreground_color.Append(ID_ANY, 'Dark Slate Blue', 'Dark Slate Blue Text')
        self.Bind(EVT_MENU, self.on_dark_slate_blue_foreground, dark_slate_blue_foreground)
        firebrick_foreground = foreground_color.Append(ID_ANY, 'FireBrick', 'FireBrick Text')
        self.Bind(EVT_MENU, self.on_firebrick_foreground, firebrick_foreground)
        maroon_foreground = foreground_color.Append(ID_ANY, 'Maroon', 'Maroon Text')
        self.Bind(EVT_MENU, self.on_maroon_foreground, maroon_foreground)
        sienna_foreground = foreground_color.Append(ID_ANY, 'Sienna', 'Sienna Text')
        self.Bind(EVT_MENU, self.on_sienna_foreground, sienna_foreground)
        dark_orchid_foreground = foreground_color.Append(ID_ANY, 'Dark Orchid', 'Dark Orchid Text')
        self.Bind(EVT_MENU, self.on_dark_orchid_foreground, dark_orchid_foreground)
        khaki_foreground = foreground_color.Append(ID_ANY, 'Khaki', 'Khaki Text')
        self.Bind(EVT_MENU, self.on_khaki_foreground, khaki_foreground)
        brown_foreground = foreground_color.Append(ID_ANY, 'Brown', 'Brown Text')
        self.Bind(EVT_MENU, self.on_brown_foreground, brown_foreground)
        purple_foreground = foreground_color.Append(ID_ANY, 'Purple', 'Purple Text')
        self.Bind(EVT_MENU, self.on_purple_foreground, purple_foreground)
        orange_foreground = foreground_color.Append(ID_ANY, 'Orange', 'Orange Text')
        self.Bind(EVT_MENU, self.on_orange_foreground, orange_foreground)
        violet_red_foreground = foreground_color.Append(ID_ANY, 'Violet Red', 'Violet Red Text')
        self.Bind(EVT_MENU, self.on_violet_red_foreground, violet_red_foreground)
        gold_foreground = foreground_color.Append(ID_ANY, 'Gold', 'Gold Text')
        self.Bind(EVT_MENU, self.on_gold_foreground, gold_foreground)
        red_foreground = foreground_color.Append(ID_ANY, 'Red', 'Red Text')
        self.Bind(EVT_MENU, self.on_red_foreground, red_foreground)
        orange_red_foreground = foreground_color.Append(ID_ANY, 'Orange Red', 'Orange Red Text')
        self.Bind(EVT_MENU, self.on_orange_red_foreground, orange_red_foreground)
        light_magenta_foreground = foreground_color.Append(ID_ANY, 'Light Magenta', 'Light Magenta Text')
        self.Bind(EVT_MENU, self.on_light_magenta_foreground, light_magenta_foreground)
        coral_foreground = foreground_color.Append(ID_ANY, 'Coral', 'Coral Text')
        self.Bind(EVT_MENU, self.on_coral_foreground, coral_foreground)
        pink_foreground = foreground_color.Append(ID_ANY, 'Pink', 'Pink Text')
        self.Bind(EVT_MENU, self.on_pink_foreground, pink_foreground)
        yellow_foreground = foreground_color.Append(ID_ANY, 'Yellow', 'Yellow Text')
        self.Bind(EVT_MENU, self.on_yellow_foreground, yellow_foreground)
        white_foreground = foreground_color.Append(ID_ANY, 'White', 'White Text')
        self.Bind(EVT_MENU, self.on_white_foreground, white_foreground)
        style_menu.AppendMenu(ID_ANY, "&Foreground &Color", foreground_color)
        background_color = Menu()
        black_background = background_color.Append(ID_ANY, 'Black', 'Black Background')
        self.Bind(EVT_MENU, self.on_black_background, black_background)
        blue_background = background_color.Append(ID_ANY, 'Blue', 'Blue Background')
        self.Bind(EVT_MENU, self.on_blue_background, blue_background)
        green_background = background_color.Append(ID_ANY, 'Green', 'Green Background')
        self.Bind(EVT_MENU, self.on_green_background, green_background)
        cyan_background = background_color.Append(ID_ANY, 'Cyan', 'Cyan Background')
        self.Bind(EVT_MENU, self.on_cyan_background, cyan_background)
        navy_background = background_color.Append(ID_ANY, 'Navy', 'Navy Background')
        self.Bind(EVT_MENU, self.on_navy_background, navy_background)
        dark_grey_background = background_color.Append(ID_ANY, 'Dark Grey', 'Dark Grey Background')
        self.Bind(EVT_MENU, self.on_dark_grey_background, dark_grey_background)
        indian_red_background = background_color.Append(ID_ANY, 'Indian Red', 'Indian Red Background')
        self.Bind(EVT_MENU, self.on_indian_red_background, indian_red_background)
        violet_background = background_color.Append(ID_ANY, 'Violet', 'Violet Background')
        self.Bind(EVT_MENU, self.on_violet_background, violet_background)
        grey_background = background_color.Append(ID_ANY, 'Grey', 'Grey Background')
        self.Bind(EVT_MENU, self.on_grey_background, grey_background)
        dark_slate_blue_background = background_color.Append(ID_ANY, 'Dark Slate Blue', 'Dark Slate Blue Background')
        self.Bind(EVT_MENU, self.on_dark_slate_blue_background, dark_slate_blue_background)
        firebrick_background = background_color.Append(ID_ANY, 'FireBrick', 'FireBrick Background')
        self.Bind(EVT_MENU, self.on_firebrick_background, firebrick_background)
        maroon_background = background_color.Append(ID_ANY, 'Maroon', 'Maroon Background')
        self.Bind(EVT_MENU, self.on_maroon_background, maroon_background)
        sienna_background = background_color.Append(ID_ANY, 'Sienna', 'Sienna Background')
        self.Bind(EVT_MENU, self.on_sienna_background, sienna_background)
        dark_orchid_background = background_color.Append(ID_ANY, 'Dark Orchid', 'Dark Orchid Background')
        self.Bind(EVT_MENU, self.on_dark_orchid_background, dark_orchid_background)
        khaki_background = background_color.Append(ID_ANY, 'Khaki', 'Khaki Background')
        self.Bind(EVT_MENU, self.on_khaki_background, khaki_background)
        brown_background = background_color.Append(ID_ANY, 'Brown', 'Brown Background')
        self.Bind(EVT_MENU, self.on_brown_background, brown_background)
        purple_background = background_color.Append(ID_ANY, 'Purple', 'Purple Background')
        self.Bind(EVT_MENU, self.on_purple_background, purple_background)
        orange_background = background_color.Append(ID_ANY, 'Orange', 'Orange Background')
        self.Bind(EVT_MENU, self.on_orange_background, orange_background)
        violet_red_background = background_color.Append(ID_ANY, 'Violet Red', 'Violet Red Background')
        self.Bind(EVT_MENU, self.on_violet_red_background, violet_red_background)
        gold_background = background_color.Append(ID_ANY, 'Gold', 'Gold Background')
        self.Bind(EVT_MENU, self.on_gold_background, gold_background)
        red_background = background_color.Append(ID_ANY, 'Red', 'Red Background')
        self.Bind(EVT_MENU, self.on_red_background, red_background)
        orange_red_background = background_color.Append(ID_ANY, 'Orange Red', 'Orange Red Background')
        self.Bind(EVT_MENU, self.on_orange_red_background, orange_red_background)
        light_magenta_background = background_color.Append(ID_ANY, 'Light Magenta', 'Light Magenta Background')
        self.Bind(EVT_MENU, self.on_light_magenta_background, light_magenta_background)
        coral_background = background_color.Append(ID_ANY, 'Coral', 'Coral Background')
        self.Bind(EVT_MENU, self.on_coral_background, coral_background)
        pink_background = background_color.Append(ID_ANY, 'Pink', 'Pink Background')
        self.Bind(EVT_MENU, self.on_pink_background, pink_background)
        yellow_background = background_color.Append(ID_ANY, 'Yellow', 'Yellow Background')
        self.Bind(EVT_MENU, self.on_yellow_background, yellow_background)
        white_background = background_color.Append(ID_ANY, 'White', 'White Background')
        self.Bind(EVT_MENU, self.on_white_background, white_background)
        style_menu.AppendMenu(ID_ANY, "&Background &Color", background_color)
        menu_bar.Append(style_menu, '&Style')
        self.window.SetMenuBar(menu_bar)

    def on_foreground(self, color):
        if self.text_input.HasSelection():
            begin, end = self.text_input.GetSelection()
            self.text_input.SetStyle(begin, end, wx.TextAttr(NamedColour(color)))

    def on_background(self, color):
        if self.text_input.HasSelection():
            begin, end = self.text_input.GetSelection()
            self.text_input.SetStyle(begin, end, wx.TextAttr(NullColour, NamedColour(color)))

    def on_black_foreground(self, event):
        self.on_foreground(BLACK)

    def on_blue_foreground(self, event):
        self.on_foreground(BLUE)

    def on_green_foreground(self, event):
        self.on_foreground(GREEN)

    def on_cyan_foreground(self, event):
        self.on_foreground(CYAN)

    def on_navy_foreground(self, event):
        self.on_foreground(NAVY)

    def on_dark_grey_foreground(self, event):
        self.on_foreground(DARK_GREY)

    def on_indian_red_foreground(self, event):
        self.on_foreground(INDIAN_RED)

    def on_violet_foreground(self, event):
        self.on_foreground(VIOLET)

    def on_grey_foreground(self, event):
        self.on_foreground(GREY)

    def on_dark_slate_blue_foreground(self, event):
        self.on_foreground(DARK_SLATE_BLUE)

    def on_firebrick_foreground(self, event):
        self.on_foreground(FIREBRICK)

    def on_maroon_foreground(self, event):
        self.on_foreground(MAROON)

    def on_sienna_foreground(self, event):
        self.on_foreground(SIENNA)

    def on_dark_orchid_foreground(self, event):
        self.on_foreground(DARK_ORCHID)

    def on_khaki_foreground(self, event):
        self.on_foreground(KHAKI)

    def on_brown_foreground(self, event):
        self.on_foreground(BROWN)

    def on_purple_foreground(self, event):
        self.on_foreground(PURPLE)

    def on_orange_foreground(self, event):
        self.on_foreground(ORANGE)

    def on_violet_red_foreground(self, event):
        self.on_foreground(VIOLET_RED)

    def on_gold_foreground(self, event):
        self.on_foreground(GOLD)

    def on_red_foreground(self, event):
        self.on_foreground(RED)

    def on_orange_red_foreground(self, event):
        self.on_foreground(ORANGE_RED)

    def on_light_magenta_foreground(self, event):
        self.on_foreground(LIGHT_MAGENTA)

    def on_coral_foreground(self, event):
        self.on_foreground(CORAL)

    def on_pink_foreground(self, event):
        self.on_foreground(PINK)

    def on_yellow_foreground(self, event):
        self.on_foreground(YELLOW)

    def on_white_foreground(self, event):
        self.on_foreground(WHITE)

    def on_black_background(self, event):
        self.on_background(BLACK)

    def on_blue_background(self, event):
        self.on_background(BLUE)

    def on_green_background(self, event):
        self.on_background(GREEN)

    def on_cyan_background(self, event):
        self.on_background(CYAN)

    def on_navy_background(self, event):
        self.on_background(NAVY)

    def on_dark_grey_background(self, event):
        self.on_background(DARK_GREY)

    def on_indian_red_background(self, event):
        self.on_background(INDIAN_RED)

    def on_violet_background(self, event):
        self.on_background(VIOLET)

    def on_grey_background(self, event):
        self.on_background(GREY)

    def on_dark_slate_blue_background(self, event):
        self.on_background(DARK_SLATE_BLUE)

    def on_firebrick_background(self, event):
        self.on_background(FIREBRICK)

    def on_maroon_background(self, event):
        self.on_background(MAROON)

    def on_sienna_background(self, event):
        self.on_background(SIENNA)

    def on_dark_orchid_background(self, event):
        self.on_background(DARK_ORCHID)

    def on_khaki_background(self, event):
        self.on_background(KHAKI)

    def on_brown_background(self, event):
        self.on_background(BROWN)

    def on_purple_background(self, event):
        self.on_background(PURPLE)

    def on_orange_background(self, event):
        self.on_background(ORANGE)

    def on_violet_red_background(self, event):
        self.on_background(VIOLET_RED)

    def on_gold_background(self, event):
        self.on_background(GOLD)

    def on_red_background(self, event):
        self.on_background(RED)

    def on_orange_red_background(self, event):
        self.on_background(ORANGE_RED)

    def on_light_magenta_background(self, event):
        self.on_background(LIGHT_MAGENTA)

    def on_coral_background(self, event):
        self.on_background(CORAL)

    def on_pink_background(self, event):
        self.on_background(PINK)

    def on_yellow_background(self, event):
        self.on_background(YELLOW)

    def on_white_background(self, event):
        self.on_background(WHITE)

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

    def on_replace(self, event):
        if self.text_input.HasSelection():
            message_box = TextEntryDialog(self.window, REPLACE_MESSAGE, REPLACE_TITLE,
                                          defaultValue=self.text_input.GetStringSelection())
            button = message_box.ShowModal()
            if button == ID_OK:
                frm, to = self.text_input.GetSelection()
                self.text_input.Remove(frm, to)
                self.text_input.SetInsertionPoint(frm)
                self.text_input.WriteText(message_box.GetValue())

    def on_replace_all(self, event):
        if self.text_input.HasSelection():
            message_box = TextEntryDialog(self.window, REPLACE_ALL_MESSAGE, REPLACE_ALL_TITLE,
                                          defaultValue=self.text_input.GetStringSelection())
            button = message_box.ShowModal()
            if button == ID_OK:
                text = self.text_input.GetValue()
                text = text.replace(self.text_input.GetStringSelection(), message_box.GetValue())
                self.text_input.Clear()
                self.text_input.SetValue(text)

    def on_select_all(self, event):
        self.text_input.SetSelection(-1, -1)

    def on_time_and_date(self, event):
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        hour = str(now.hour)
        minute = str(now.minute)
        time = ":".join([hour, minute])
        date = "/".join([day, month, year])
        time_and_date = " ".join([time, date])
        self.text_input.WriteText(time_and_date)

    def message_box(self):
        entered = True
        while entered:
            message_box = TextEntryDialog(self.window, NEW_FILE_MESSAGE, NEW_FILE_TITLE, defaultValue=NEW_FILE)
            button = message_box.ShowModal()
            if button == ID_OK:
                file_name = message_box.GetValue() + TXT_EXT
                folder = "\\".join(os.path.abspath(__file__).split("\\")[:-3] + [SYSTEM_FOLDER, file_name])
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
