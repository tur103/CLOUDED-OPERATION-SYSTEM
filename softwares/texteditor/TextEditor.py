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
        text_input_font = self.text_input.GetFont()
        self.text_font_dict = {"size": text_input_font.GetPointSize(),
                               "family": text_input_font.GetFamily(),
                               "style": text_input_font.GetStyle(),
                               "weight": text_input_font.GetWeight(),
                               "underline": text_input_font.GetUnderlined()}
        self.create_menu_bar()
        self.Bind(EVT_TEXT, self.on_text_enter, source=self.text_input)
        self.Bind(EVT_LEFT_UP, self.on_highlight_text, source=self.text_input)
        self.font = Font(15, DEFAULT, NORMAL, BOLD)
        self.add_title(CREDIT, (100, 600))
        self.window.Show(True)
        if not self.file_name:
            self.on_new("new")

    def get_file_data(self):
        """

        Getting the name of the file from it's path
        and getting the data from the file.

        """
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
        """

        Adding the text input for entering and displaying text
        in the text editor.

        return:
            TextCtrl: The text input controller.

        """
        return TextCtrl(self.panel, pos=(0, 0), size=(1000, 580),
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
        """

        Creating the graphic listed and iconed menu bar for the user
        that includes actions to perform on the text.

        """
        menu_bar = MenuBar()
        file_menu = Menu()
        new = MenuItem(file_menu, 1, '&New\tCtrl+N')
        new.SetBitmap(Bitmap(NEW_IMAGE))
        file_menu.AppendItem(new)
        self.Bind(EVT_MENU, self.on_new, id=1)
        open = MenuItem(file_menu, 2, '&Open\tCtrl+O')
        open.SetBitmap(Bitmap(OPEN_IMAGE))
        file_menu.AppendItem(open)
        self.Bind(EVT_MENU, self.on_open, id=2)
        save_as = MenuItem(file_menu, 3, '&Save &As\tCtrl+S')
        save_as.SetBitmap(Bitmap(SAVE_AS_IMAGE))
        file_menu.AppendItem(save_as)
        self.Bind(EVT_MENU, self.on_save_as, save_as)
        exit = MenuItem(file_menu, 4, '&Quit\tCtrl+Q')
        exit.SetBitmap(Bitmap(QUIT_IMAGE))
        file_menu.AppendItem(exit)
        self.Bind(EVT_MENU, self.on_quit, id=4)
        menu_bar.Append(file_menu, '&File')
        edit_menu = Menu()
        self.undo = MenuItem(edit_menu, 5, '&Undo\tCtrl+Z')
        self.undo.SetBitmap(Bitmap(UNDO_IMAGE))
        edit_menu.AppendItem(self.undo)
        self.undo.Enable(False)
        self.Bind(EVT_MENU, self.on_undo, id=5)
        self.redo = MenuItem(edit_menu, 6, '&Redo\tCtrl+Y')
        self.redo.SetBitmap(Bitmap(REDO_IMAGE))
        edit_menu.AppendItem(self.redo)
        self.redo.Enable(False)
        self.Bind(EVT_MENU, self.on_redo, id=6)
        self.cut = MenuItem(edit_menu, 7, '&Cut\tCtrl+X')
        self.cut.SetBitmap(Bitmap(CUT_IMAGE))
        edit_menu.AppendItem(self.cut)
        self.cut.Enable(False)
        self.Bind(EVT_MENU, self.on_cut, id=7)
        self.copy = MenuItem(edit_menu, 8, '&Copy\tCtrl+C')
        self.copy.SetBitmap(Bitmap(COPY_IMAGE))
        edit_menu.AppendItem(self.copy)
        self.copy.Enable(False)
        self.Bind(EVT_MENU, self.on_copy, id=8)
        self.duplicate = MenuItem(edit_menu, 16, '&Duplicate\tCtrl+D')
        self.duplicate.SetBitmap(Bitmap(DUPLICATE_IMAGE))
        edit_menu.AppendItem(self.duplicate)
        self.Bind(EVT_MENU, self.on_duplicate, id=16)
        self.paste = MenuItem(edit_menu, 9, '&Paste\tCtrl+V')
        self.paste.SetBitmap(Bitmap(PASTE_IMAGE))
        edit_menu.AppendItem(self.paste)
        self.Bind(EVT_MENU, self.on_paste, id=9)
        self.delete = MenuItem(edit_menu, 10, '&Delete\tDELETE')
        self.delete.SetBitmap(Bitmap(DELETE_IMAGE))
        edit_menu.AppendItem(self.delete)
        self.delete.Enable(False)
        self.Bind(EVT_MENU, self.on_delete, id=10)
        self.find = MenuItem(edit_menu, 11, '&Find\tCtrl+F')
        self.find.SetBitmap(Bitmap(FIND_IMAGE))
        edit_menu.AppendItem(self.find)
        self.Bind(EVT_MENU, self.on_find, id=11)
        self.replace = MenuItem(edit_menu, 12, '&Replace\tCtrl+R')
        self.replace.SetBitmap(Bitmap(REPLACE_IMAGE))
        edit_menu.AppendItem(self.replace)
        self.replace.Enable(False)
        self.Bind(EVT_MENU, self.on_replace, id=12)
        self.replace_all = MenuItem(edit_menu, 13, '&Replace &All\tCtrl+H')
        self.replace_all.SetBitmap(Bitmap(REPLACE_ALL_IMAGE))
        edit_menu.AppendItem(self.replace_all)
        self.replace_all.Enable(False)
        self.Bind(EVT_MENU, self.on_replace_all, id=13)
        self.select_all = MenuItem(edit_menu, 14, '&Select &All\tCtrl+A')
        self.select_all.SetBitmap(Bitmap(SELECT_ALL_IMAGE))
        edit_menu.AppendItem(self.select_all)
        self.Bind(EVT_MENU, self.on_select_all, id=14)
        self.time_and_date = MenuItem(edit_menu, 15, '&Time &And &Date\tCtrl+T')
        self.time_and_date.SetBitmap(Bitmap(TIME_AND_DATE_IMAGE))
        edit_menu.AppendItem(self.time_and_date)
        self.Bind(EVT_MENU, self.on_time_and_date, id=15)
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
        font = Menu()
        swiss_font = font.Append(ID_ANY, 'Swiss', 'Swiss Font')
        self.Bind(EVT_MENU, self.on_swiss_font, swiss_font)
        decorative_font = font.Append(ID_ANY, 'Decorative', 'Decorative Font')
        self.Bind(EVT_MENU, self.on_decorative_font, decorative_font)
        modern_font = font.Append(ID_ANY, 'Modern', 'Modern Font')
        self.Bind(EVT_MENU, self.on_modern_font, modern_font)
        roman_font = font.Append(ID_ANY, 'Roman', 'Roman Font')
        self.Bind(EVT_MENU, self.on_roman_font, roman_font)
        script_font = font.Append(ID_ANY, 'Script', 'Script Font')
        self.Bind(EVT_MENU, self.on_script_font, script_font)
        style_menu.AppendMenu(ID_ANY, "&Font", font)
        size = Menu()
        point8 = size.Append(ID_ANY, '8', '8 Size')
        self.Bind(EVT_MENU, self.on_point8, point8)
        point10 = size.Append(ID_ANY, '10', '10 Size')
        self.Bind(EVT_MENU, self.on_point10, point10)
        point12 = size.Append(ID_ANY, '12', '12 Size')
        self.Bind(EVT_MENU, self.on_point12, point12)
        point14 = size.Append(ID_ANY, '14', '14 Size')
        self.Bind(EVT_MENU, self.on_point14, point14)
        point16 = size.Append(ID_ANY, '16', '16 Size')
        self.Bind(EVT_MENU, self.on_point16, point16)
        point18 = size.Append(ID_ANY, '18', '18 Size')
        self.Bind(EVT_MENU, self.on_point18, point18)
        point20 = size.Append(ID_ANY, '20', '20 Size')
        self.Bind(EVT_MENU, self.on_point20, point20)
        point22 = size.Append(ID_ANY, '22', '22 Size')
        self.Bind(EVT_MENU, self.on_point22, point22)
        point24 = size.Append(ID_ANY, '24', '24 Size')
        self.Bind(EVT_MENU, self.on_point24, point24)
        point26 = size.Append(ID_ANY, '26', '26 Size')
        self.Bind(EVT_MENU, self.on_point26, point26)
        point28 = size.Append(ID_ANY, '28', '28 Size')
        self.Bind(EVT_MENU, self.on_point28, point28)
        point36 = size.Append(ID_ANY, '36', '6 Size')
        self.Bind(EVT_MENU, self.on_point36, point36)
        point48 = size.Append(ID_ANY, '48', '48 Size')
        self.Bind(EVT_MENU, self.on_point48, point48)
        point72 = size.Append(ID_ANY, '72', '72 Size')
        self.Bind(EVT_MENU, self.on_point72, point72)
        style_menu.AppendMenu(ID_ANY, "&Size", size)
        design = Menu()
        self.bold = MenuItem(design, 17, '&Bold\tCtrl+B', kind=ITEM_CHECK)
        self.bold.SetBitmap(Bitmap(BOLD_ICON))
        design.AppendItem(self.bold)
        self.Bind(EVT_MENU, self.on_bold, id=17)
        self.italic = MenuItem(design, 18, '&Italic\tCtrl+I', kind=ITEM_CHECK)
        self.italic.SetBitmap(Bitmap(ITALIC_ICON))
        design.AppendItem(self.italic)
        self.Bind(EVT_MENU, self.on_italic, id=18)
        self.underline = MenuItem(design, 19, '&Underline\tCtrl+U', kind=ITEM_CHECK)
        self.underline.SetBitmap(Bitmap(UNDERLINE_ICON))
        design.AppendItem(self.underline)
        self.Bind(EVT_MENU, self.on_underline, id=19)
        style_menu.AppendMenu(ID_ANY, "&design", design)
        menu_bar.Append(style_menu, '&Style')
        self.window.SetMenuBar(menu_bar)
        self.toolbar = self.window.CreateToolBar()
        new_tool = self.toolbar.AddLabelTool(ID_NEW, "New", Bitmap(NEW_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_new, new_tool)
        open_tool = self.toolbar.AddLabelTool(ID_OPEN, "Open", Bitmap(OPEN_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_open, open_tool)
        save_as_tool = self.toolbar.AddLabelTool(ID_SAVEAS, "Save As", Bitmap(SAVE_AS_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_save_as, save_as_tool)
        quit_tool = self.toolbar.AddLabelTool(ID_EXIT, "Quit", Bitmap(QUIT_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_quit, quit_tool)
        self.toolbar.AddSeparator()
        undo_tool = self.toolbar.AddLabelTool(ID_UNDO, "Undo", Bitmap(UNDO_IMAGE))
        self.toolbar.EnableTool(ID_UNDO, False)
        self.Bind(wx.EVT_TOOL, self.on_undo, undo_tool)
        redo_tool = self.toolbar.AddLabelTool(ID_REDO, "Redo", Bitmap(REDO_IMAGE))
        self.toolbar.EnableTool(ID_REDO, False)
        self.Bind(wx.EVT_TOOL, self.on_redo, redo_tool)
        cut_tool = self.toolbar.AddLabelTool(ID_CUT, "Cut", Bitmap(CUT_IMAGE))
        self.toolbar.EnableTool(ID_CUT, False)
        self.Bind(wx.EVT_TOOL, self.on_cut, cut_tool)
        copy_tool = self.toolbar.AddLabelTool(ID_COPY, "Copy", Bitmap(COPY_IMAGE))
        self.toolbar.EnableTool(ID_COPY, False)
        self.Bind(wx.EVT_TOOL, self.on_copy, copy_tool)
        duplicate_tool = self.toolbar.AddLabelTool(ID_DUPLICATE, "Duplicate", Bitmap(DUPLICATE_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_duplicate, duplicate_tool)
        paste_tool = self.toolbar.AddLabelTool(ID_PASTE, "Paste", Bitmap(PASTE_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_paste, paste_tool)
        delete_tool = self.toolbar.AddLabelTool(ID_DELETE, "Delete", Bitmap(DELETE_IMAGE))
        self.toolbar.EnableTool(ID_DELETE, False)
        self.Bind(wx.EVT_TOOL, self.on_delete, delete_tool)
        find_tool = self.toolbar.AddLabelTool(ID_FIND, "Find", Bitmap(FIND_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_find, find_tool)
        replace_tool = self.toolbar.AddLabelTool(ID_REPLACE, "Replace", Bitmap(REPLACE_IMAGE))
        self.toolbar.EnableTool(ID_REPLACE, False)
        self.Bind(wx.EVT_TOOL, self.on_replace, replace_tool)
        replace_all_tool = self.toolbar.AddLabelTool(ID_REPLACE_ALL, "Replace All", Bitmap(REPLACE_ALL_IMAGE))
        self.toolbar.EnableTool(ID_REPLACE_ALL, False)
        self.Bind(wx.EVT_TOOL, self.on_replace_all, replace_all_tool)
        select_all_tool = self.toolbar.AddLabelTool(ID_SELECTALL, "Select All", Bitmap(SELECT_ALL_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_select_all, select_all_tool)
        time_and_date_tool = self.toolbar.AddLabelTool(ID_OK, "Time And Date", Bitmap(TIME_AND_DATE_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_time_and_date, time_and_date_tool)
        bold_tool = self.toolbar.AddLabelTool(ID_BOLD, "Bold", Bitmap(BOLD_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_bold_icon, bold_tool)
        italic_tool = self.toolbar.AddLabelTool(ID_ITALIC, "Italic", Bitmap(ITALIC_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_italic_icon, italic_tool)
        underline_tool = self.toolbar.AddLabelTool(ID_UNDERLINE, "Underline", Bitmap(UNDERLINE_IMAGE))
        self.Bind(wx.EVT_TOOL, self.on_underline_icon, underline_tool)
        self.toolbar.Realize()

    def on_font(self):
        """

        Changing the font of the text for the one
        that the user chose.

        """
        new_font = Font(self.text_font_dict["size"], self.text_font_dict["family"],
                        self.text_font_dict["style"], self.text_font_dict["weight"],
                        self.text_font_dict["underline"])
        self.text_input.SetStyle(-1, -1, wx.TextAttr(NullColour, NullColour, new_font))

    def on_point(self):
        """

        Changing the size of the text for the one
        that the user chose.

        """
        new_font = Font(self.text_font_dict["size"], self.text_font_dict["family"],
                        self.text_font_dict["style"], self.text_font_dict["weight"],
                        self.text_font_dict["underline"])
        self.text_input.SetStyle(-1, -1, wx.TextAttr(NullColour, NullColour, new_font))

    def on_bold_icon(self, event):
        """

        Checks or unchecks the bold icon.

        """
        if self.bold.IsChecked():
            self.bold.Check(False)
        else:
            self.bold.Check(True)
        self.on_bold(None)

    def on_bold(self, event):
        """

        Changing the bold of the text for the one
        that the user chose.

        """
        self.text_font_dict["weight"] = BOLD if self.bold.IsChecked() else NORMAL
        new_font = Font(self.text_font_dict["size"], self.text_font_dict["family"],
                        self.text_font_dict["style"], self.text_font_dict["weight"],
                        self.text_font_dict["underline"])
        self.text_input.SetStyle(-1, -1, wx.TextAttr(NullColour, NullColour, new_font))

    def on_italic_icon(self, event):
        """

        Checks or unchecks the italic icon.

        """
        if self.italic.IsChecked():
            self.italic.Check(False)
        else:
            self.italic.Check(True)
        self.on_italic(None)

    def on_italic(self, event):
        """

        Changing the italic style of the text for the one
        that the user chose.

        """
        self.text_font_dict["style"] = ITALIC if self.italic.IsChecked() else NORMAL
        new_font = Font(self.text_font_dict["size"], self.text_font_dict["family"],
                        self.text_font_dict["style"], self.text_font_dict["weight"],
                        self.text_font_dict["underline"])
        self.text_input.SetStyle(-1, -1, wx.TextAttr(NullColour, NullColour, new_font))

    def on_underline_icon(self, event):
        """

        Checks or unchecks the underline icon.

        """
        if self.underline.IsChecked():
            self.underline.Check(False)
        else:
            self.underline.Check(True)
        self.on_underline(None)

    def on_underline(self, event):
        """

        Changing the underline style of the text for the one
        that the user chose.

        """
        self.text_font_dict["underline"] = True if self.underline.IsChecked() else False
        new_font = Font(self.text_font_dict["size"], self.text_font_dict["family"],
                        self.text_font_dict["style"], self.text_font_dict["weight"],
                        self.text_font_dict["underline"])
        self.text_input.SetStyle(-1, -1, wx.TextAttr(NullColour, NullColour, new_font))

    def on_foreground(self, color):
        """

        Changing the color of the text for the one
        that the user chose.

        """
        if self.text_input.HasSelection():
            begin, end = self.text_input.GetSelection()
            self.text_input.SetStyle(begin, end, wx.TextAttr(NamedColour(color)))

    def on_background(self, color):
        """

        Changing the background color of the text for the one
        that the user chose.

        """
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

    def on_swiss_font(self, event):
        self.text_font_dict["family"] = FONTFAMILY_SWISS
        self.on_font()

    def on_decorative_font(self, event):
        self.text_font_dict["family"] = FONTFAMILY_DECORATIVE
        self.on_font()

    def on_modern_font(self, event):
        self.text_font_dict["family"] = FONTFAMILY_MODERN
        self.on_font()

    def on_roman_font(self, event):
        self.text_font_dict["family"] = FONTFAMILY_ROMAN
        self.on_font()

    def on_script_font(self, event):
        self.text_font_dict["family"] = FONTFAMILY_SCRIPT
        self.on_font()

    def on_point8(self, event):
        self.text_font_dict["size"] = 8
        self.on_point()

    def on_point10(self, event):
        self.text_font_dict["size"] = 10
        self.on_point()

    def on_point12(self, event):
        self.text_font_dict["size"] = 12
        self.on_point()

    def on_point14(self, event):
        self.text_font_dict["size"] = 14
        self.on_point()

    def on_point16(self, event):
        self.text_font_dict["size"] = 16
        self.on_point()

    def on_point18(self, event):
        self.text_font_dict["size"] = 18
        self.on_point()

    def on_point20(self, event):
        self.text_font_dict["size"] = 20
        self.on_point()

    def on_point22(self, event):
        self.text_font_dict["size"] = 22
        self.on_point()

    def on_point24(self, event):
        self.text_font_dict["size"] = 24
        self.on_point()

    def on_point26(self, event):
        self.text_font_dict["size"] = 26
        self.on_point()

    def on_point28(self, event):
        self.text_font_dict["size"] = 28
        self.on_point()

    def on_point36(self, event):
        self.text_font_dict["size"] = 36
        self.on_point()

    def on_point48(self, event):
        self.text_font_dict["size"] = 48
        self.on_point()

    def on_point72(self, event):
        self.text_font_dict["size"] = 72
        self.on_point()

    def on_quit(self, event):
        """

        Closing the text editor software.

        """
        self.window.Close()

    def on_new(self, event):
        """

        Opening a new text file in the text editor software.

        """
        self.message_box()
        if not self.file_name:
            sys.exit()
        self.on_highlight_text(None)

    def on_open(self, event):
        """

        Opening an existing text file in the text editor software.

        """
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
        self.on_highlight_text(None)

    def on_save_as(self, event):
        """

        Saving the current text file as new one.

        """
        entered = True
        while entered:
            message_box = TextEntryDialog(self.window, SAVE_AS_MESSAGE, SAVE_AS_TITLE, defaultValue=NEW_FILE)
            button = message_box.ShowModal()
            if button == ID_OK:
                file_name = message_box.GetValue() + TXT_EXT
                folder = "\\".join(os.path.abspath(__file__).split("\\")[:-3] + [SYSTEM_FOLDER, file_name])
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
        self.on_highlight_text(None)

    def on_undo(self, event):
        """

        Performing an undo action on the text.

        """
        self.text_input.Undo()
        self.on_highlight_text(None)

    def on_redo(self, event):
        """

        Performing a redo action on the text.

        """
        self.text_input.Redo()
        self.on_highlight_text(None)

    def on_cut(self, event):
        """

        Performing a cut action on the selected text.

        """
        text = self.text_input.FindFocus()
        if text:
            text.Cut()
            self.on_highlight_text(None)

    def on_copy(self, event):
        """

        Performing a copy action on the selected text.

        """
        text = self.text_input.FindFocus()
        if text:
            text.Copy()
            self.on_highlight_text(None)

    def on_duplicate(self, event):
        """

        Performing a duplicate action on the selected text.

        """
        if self.text_input.HasSelection():
            text = self.text_input.GetStringSelection()
            frm, to = self.text_input.GetSelection()
            self.text_input.SetInsertionPoint(to)
            self.text_input.WriteText(text)
        else:
            all_text = self.text_input.GetValue()
            cursor = self.text_input.GetInsertionPoint()
            cursor_line = self.text_input.PositionToXY(cursor)[1]
            text_line = self.text_input.GetLineText(cursor_line)
            lines_of_text = all_text.split("\n")
            lines_of_text.insert(cursor_line + 1, text_line)
            all_text = "\n".join(lines_of_text)
            self.text_input.Clear()
            self.text_input.SetValue(all_text)

    def on_paste(self, event):
        """

        Pasting the text from the clipboard to the file.

        """
        self.text_input.Paste()
        self.on_highlight_text(None)

    def on_delete(self, event):
        """

        Performing a delete action on the selected text.

        """
        frm, to = self.text_input.GetSelection()
        self.text_input.Remove(frm, to)
        self.on_highlight_text(None)

    def on_find(self, event):
        """

        Performing a find action on the selected text.
        Finds the next text that matches to the given pattern.

        """
        message_box = TextEntryDialog(self.window, FIND_MESSAGE, FIND_TITLE,
                                      defaultValue=self.text_input.GetStringSelection())
        button = message_box.ShowModal()
        if button == ID_OK:
            text_to_search = message_box.GetValue()
            if text_to_search:
                text = self.text_input.GetValue()
                findings = []
                for match in re.finditer(text_to_search, text):
                    findings.append((match.start(), match.end()))
                cursor = self.text_input.GetInsertionPoint()
                for find in findings:
                    if find[1] >= cursor:
                        self.text_input.SetSelection(find[0], find[1])
                        break
        self.on_highlight_text(None)

    def on_replace(self, event):
        """

        Performing a replace action on the selected text
        with another given one.
        Replaces the selected text with another given pattern.

        """
        if self.text_input.HasSelection():
            message_box = TextEntryDialog(self.window, REPLACE_MESSAGE, REPLACE_TITLE,
                                          defaultValue=self.text_input.GetStringSelection())
            button = message_box.ShowModal()
            if button == ID_OK:
                frm, to = self.text_input.GetSelection()
                self.text_input.Remove(frm, to)
                self.text_input.SetInsertionPoint(frm)
                self.text_input.WriteText(message_box.GetValue())
        self.on_highlight_text(None)

    def on_replace_all(self, event):
        """

        Performing a replace action on the selected text and all it's matches
        with another given one.
        Replaces the selected text and all it's matches with another given pattern.

        """
        if self.text_input.HasSelection():
            message_box = TextEntryDialog(self.window, REPLACE_ALL_MESSAGE, REPLACE_ALL_TITLE,
                                          defaultValue=self.text_input.GetStringSelection())
            button = message_box.ShowModal()
            if button == ID_OK:
                text = self.text_input.GetValue()
                text = text.replace(self.text_input.GetStringSelection(), message_box.GetValue())
                self.text_input.Clear()
                self.text_input.SetValue(text)
        self.on_highlight_text(None)

    def on_select_all(self, event):
        """

        Selecting all the text.

        """
        self.text_input.SetSelection(-1, -1)
        self.on_highlight_text(None)

    def on_time_and_date(self, event):
        """

        Adding the date and time to the specified
        location in the file.

        """
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
        self.on_highlight_text(None)

    def message_box(self):
        """

        Displaying massage box.
        The user entering the name of the new file he wants to
        create in the box.

        """
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
        """

        Executes when there is a change in the data of the file.
        when text added, deleted or modified in the file it's saved
        automatically.

        """
        data = event.GetString()
        file_handle = open(self.file_name, REGULAR_WRITING)
        self.data = data
        file_handle.write(self.data)
        file_handle.close()
        if self.text_input.CanUndo():
            self.toolbar.EnableTool(ID_UNDO, True)
            self.undo.Enable(True)
        else:
            self.toolbar.EnableTool(ID_UNDO, False)
            self.undo.Enable(False)
        if self.text_input.CanRedo():
            self.toolbar.EnableTool(ID_REDO, True)
            self.redo.Enable(True)
        else:
            self.toolbar.EnableTool(ID_REDO, False)
            self.redo.Enable(False)
        self.on_highlight_text(None)

    def on_highlight_text(self, event):
        """

        Opening the actions that depends on selected text.

        """
        if self.text_input.CanCut():
            self.toolbar.EnableTool(ID_CUT, True)
            self.cut.Enable(True)
            self.toolbar.EnableTool(ID_COPY, True)
            self.copy.Enable(True)
            self.toolbar.EnableTool(ID_DELETE, True)
            self.delete.Enable(True)
            self.toolbar.EnableTool(ID_REPLACE, True)
            self.replace.Enable(True)
            self.toolbar.EnableTool(ID_REPLACE_ALL, True)
            self.replace_all.Enable(True)
            if self.is_selected_all():
                self.toolbar.EnableTool(ID_SELECTALL, False)
                self.select_all.Enable(False)
        else:
            self.toolbar.EnableTool(ID_CUT, False)
            self.cut.Enable(False)
            self.toolbar.EnableTool(ID_COPY, False)
            self.copy.Enable(False)
            self.toolbar.EnableTool(ID_DELETE, False)
            self.delete.Enable(False)
            self.toolbar.EnableTool(ID_REPLACE, False)
            self.replace.Enable(False)
            self.toolbar.EnableTool(ID_REPLACE_ALL, False)
            self.replace_all.Enable(False)
            self.toolbar.EnableTool(ID_SELECTALL, True)
            self.select_all.Enable(True)

    def is_selected_all(self):
        """

        Function that checks if all the text is selected in the editor.

        returns:
            bool: true or false.

        """
        all_text = self.text_input.GetValue()
        selected_text = self.text_input.GetStringSelection()
        return True if all_text == selected_text else False


app = TextEditor()
app.MainLoop()
