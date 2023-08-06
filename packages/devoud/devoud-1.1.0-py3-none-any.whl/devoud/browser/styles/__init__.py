# TODO: Упростить до .qss файлов

import json
from string import Template

from devoud import rpath
import devoud.browser.styles.svg


class Theme:
    app_icons = {'Linux': 'icons:devoud.svg',
                 'Windows': 'icons:devoud.ico',
                 'Darwin': 'icons:devoud.icns'}

    def __init__(self, parent, name=None):
        self.parent = parent
        if name is None:
            name = parent.settings.get('theme')
        self.name = name

        # стандартная тема
        self.title_buttons_color = {
            "min": "#4c5270",
            "max": "#4c5270",
            "close": "#aa2f2f"
        }

        self.bg = '#282A3A'
        self.fg = '#eef1f1'

        self.address_panel_button = {
            'border': '#aa2f2f',
            'hover': '#3D3F59'
        }

        self.search_box = {
            'bg': '#515375',
            'fg': '#eef1f1',
            'item': '#1d1f2a'
        }

        self.address_line_frame = {
            'bg': '#1D1F2A',
            'fg': '#dfdfdf',
            'border': '#515375',
            'hover': '#515375'
        }

        self.line_edit = {
            'bg': '#1D1F2A',
            'fg': '#dfdfdf',
            'border': '#515375',
            'hover': '#515375'
        }

        self.button = {
            'bg': '#282a3a',
            'fg': '#eef1f1',
            'hover': '#3D3F59',
            'border': '#aa2f2f'
        }

        self.tab_widget = {
            "bg": "#282a3a",
            "fg": "#dfdfdf",
            "select_bg": "#515375",
            "select_fg": "#dfdfdf",
            "hover": "#3D3F59",
            "button_fg": "#dfdfdf"
        }

        self.tree_widget = {
            "header_bg": "#1d1f2a",
            "header_fg": "#dfdfdf",
            "hover_bg": "#404364",
            "hover_fg": "#dfdfdf",
            "pressed_bg": "#515375",
            "pressed_fg": "#dfdfdf",
            "button_bg": "#282a3a",
            "button_fg": "#dfdfdf",
            "button_hover_bg": "#515375",
            "button_hover_fg": "#dfdfdf",
            "button_border": "#515375"
        }

        self.find_on_page_widget = {
            "bg": "#282a3a",
            "fg": "#dfdfdf",
            "line_edit_bg": "#1d1f2a",
            "line_edit_fg": "#dfdfdf",
            "checkbox_on": "#aa2f2f",
            "checkbox_off": "#aa2f2f",
            "btn_arrow_bg": "#282a3a",
            "btn_arrow_fg": "#dfdfdf",
            "btn_arrow_hover": "#515375",
            "btn_close_bg": "#aa2f2f",
            "btn_close_fg": "#dfdfdf"
        }

        self.combobox = {
            'bg': '#515375',
            'fg': '#eef1f1',
            'item': '#1d1f2a'
        }

        self.check_box = {
            'normal': '#1d1f2a',
            'checked': '#aa2f2f'
        }

        self.sections_panel = {
            'bg': '#1d1f2a',
            'fg': '#eef1f1',
            'select': '#515375',
            'hover': '#3D3F59'
        }

        self.container = {
            'bg': '#363a4f',
            'fg': '#eef1f1'
        }

        self.container_title = {
            'bg': '#1d1f2a',
            'fg': '#eef1f1',
            'alt_fg': '#b3b5b5'
        }

        self.container_title_btn = {
            'bg': '#363a4f',
            'fg': '#eef1f1',
            'hover': '#515375'
        }

        self.download_item = {
            'bg': '#1d1f2a',
            'fg': '#eef1f1',
            'alt_fg': '#b3b5b5'
        }

        self.progress_bar = {
            'fg': '#eef1f1',
            'chunk': '#aa2f2f',
            'border': '#515375'
        }

        self.import_theme()
        svg.set_icon_color(self, self.parent.FS.user_dir())

    def import_theme(self):
        try:
            with open(rpath(f"ui/themes/{self.name}.json"), "r") as read_file:
                print('[Стили]: Загружается тема', self.name)
                data = json.load(read_file)
        except FileNotFoundError:
            print('[Стили]: Файл темы не найден', self.name)
            return

        self.title_buttons_color = data.get('title_buttons_color', self.title_buttons_color)
        self.bg = data.get('bg', self.bg)
        self.fg = data.get('fg', self.fg)
        self.search_box = data.get('search_box', self.search_box)
        self.address_panel_button = data.get('address_panel_button', self.address_panel_button)
        self.address_line_frame = data.get('address_line_frame', self.address_line_frame)
        self.line_edit = data.get('line_edit', self.line_edit)
        self.button = data.get('button', self.button)
        self.tab_widget = data.get('tab_widget', self.tab_widget)
        self.tree_widget = data.get('tree_widget', self.tree_widget)
        self.find_on_page_widget = data.get('find_on_page_widget', self.find_on_page_widget)
        self.combobox = data.get('combobox', self.combobox)
        self.check_box = data.get('check_box', self.check_box)
        self.sections_panel = data.get('sections_panel', self.sections_panel)
        self.container = data.get('container', self.container)
        self.container_title = data.get('container_title', self.container_title)
        self.container_title_btn = data.get('container_title_btn', self.container_title_btn)
        self.download_item = data.get('download_item', self.download_item)
        self.progress_bar = data.get('progress_bar', self.progress_bar)

    @staticmethod
    def rgba(h: str, opacity: float = 1):
        h = h.lstrip('#')
        res = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        return f'rgba({res[0]}, {res[1]}, {res[2]}, {opacity})'

    def style(self):
        return Template("""
        #central_widget {
            background-color: transparent;
        }

        QWidget {
            background: $bg;
            outline: 0px;
            color: $fg;
            border: 0;
            font: 11pt "Clear Sans Medium";
        }

        QPushButton {
            background: $button_bg;
            color: $button_fg;
            border-radius: 6px;
        }

        QPushButton:hover {
            background: $button_hover_bg;
        }

        QPushButton:pressed {
            background: $button_hover_bg;
            border: 2px solid $button_pressed_border;
        }

        QPushButton:disabled {
            background: $button_disabled_bg;
        }

        QPushButton::menu-indicator { 
            height: 0px;
            width: 0px;
        }
        
        QMessageBox QAbstractButton {
            padding: 4px;
        }

        #add_tab_button_panel {
            icon: url(custom:add.svg);
        }

        #back_button {
            icon: url(custom:arrow_left.svg);
        }

        #back_button:disabled {
            background: $button_disabled_bg;
        }

        #forward_button {
            icon: url(custom:arrow_right.svg);
        }

        #forward_button:disabled {
            background: $button_disabled_bg;
        }

        #stop_load_button {
            icon: url(custom:close(address_panel).svg);
        }

        #update_button {
            icon: url(custom:update.svg);
        }

        #home_button {
            icon: url(custom:home.svg);
        }

        #menu_button {
            icon: url(custom:options.svg);
        }

        QToolTip {
            background-color: $bg;
            color: $fg;
            font: 10pt "Clear Sans Medium";
            border: 2px solid $tool_tip_border;
            padding: 3px;
        }

        QLabel {
            background: transparent;
        }

        QComboBox {
            border: 0px;
            background: $combobox_bg;
            color: $combobox_fg;
            border-radius: 6px;
            padding: 0px 15px 0px 10px;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            background: $line_edit_bg;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            image: url(custom:arrow_down.svg);
        }

        QComboBox QAbstractItemView {
            border: 0px;
            border-radius: 0;
        }

        #address_panel QComboBox {
            padding: 0px 0px 0px 7px;
            background: $search_box_bg;
            color: $search_box_fg;
            border-top-left-radius: 5px;
            border-bottom-left-radius: 5px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }

        #address_panel QComboBox QAbstractItemView {
            border: 0px;
            width: 100px;
            border-radius: 0px;
            background: $search_box_item;
        }

        #address_panel QCombobox:editable {
            background: white;
        }

        #address_panel QComboBox::drop-down {
            margin-right: 5px;
            background: 0;
        }

        #address_panel QPushButton {
            background: $bg;
            border: none;
        }

        #address_panel QPushButton:hover {
            background: $address_panel_button_hover;
        }

        #address_panel QPushButton:pressed {
            background: $address_panel_button_hover;
            border: 2px solid $address_panel_button_border;
        }

        #address_line_frame {
            background: $address_line_frame_bg;
            color: $address_line_frame_fg;
            padding: 0;
            border-radius: 6px;
        }

        #address_line_frame QLineEdit {
            background: transparent;
            color: $address_line_frame_fg;
            padding-left: 2px;
            padding-right: 2px;
        }

        #address_line_frame QLineEdit:focus {
            border: 2px solid $address_line_frame_border;
        }

        #address_line_frame QPushButton {
            border: none;
            background: transparent;
            border-radius: 0;
        }

        #address_line_frame QPushButton:hover {
            background: $address_panel_button_hover;
        }
        
        #address_line_frame #bookmark_button {
            border-top-right-radius: 6px;
            border-top-left-radius: 0px;
            border-bottom-right-radius: 6px;
            border-bottom-left-radius: 0px;
        }

        LineEdit {
            background: $line_edit_bg;
            color: $line_edit_fg;
            padding-left: 5px;
            border-radius: 0;
            selection-background-color: $line_edit_border;
        }

        QProgressBar {
            border: 0;
        }

        QProgressBar::chunk {
            background: $progress_bar_chunk;
        }

        QCheckBox::indicator {
            background: $checkbox_indicator_normal;
            border-radius: 6px;
        }

        QCheckBox::indicator:checked {
            background: $checkbox_indicator_checked;
        }

        #container_content {
            background: $container_content_bg;
            border-bottom-right-radius: 6px;
            border-bottom-left-radius: 6px;
        }

        #container_content QWidget {
            background: transparent;
            font: 12pt "Clear Sans Medium";
            color: $container_content_fg;
        }

        #container_content QLineEdit {
            border: 2px solid $line_edit_border;
            selection-background-color: $line_edit_border;
            border-radius: 6px;
            padding-left: 7px;
            padding-right: 7px;
            padding-bottom: 1px;
            font: 11pt "Clear Sans Medium";
            background: $line_edit_bg;
            color: $line_edit_fg;
        }

        #container_content QPushButton {
            background: $button_bg;
            color: $button_fg;
            border-radius: 6px;
        }

        #container_content QComboBox {
            border: 0px;
            background: $combobox_bg;
            color: $combobox_fg;
            border-radius: 6px;
            padding: 0px 15px 0px 10px;
        }

        #container_content QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            background: $line_edit_bg;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            image: url(custom:arrow_down.svg);
        }

        #container_content QPushButton:hover {
            background: $button_hover_bg;
        }

        #container_content QPushButton:pressed {
            background: $button_hover_bg;
            border: 2px solid $button_pressed_border;
        }

        #container_content QComboBox QAbstractItemView {
            border: 0px;
            border-radius: 0px;
            background: $combobox_item;
        }

        #container_title {
            background: $container_title_bg;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            outline: 0px;
        }

        #container_title_text {
            padding-top: 2px;
            padding-bottom: 2px;
            background: none;
            font: 16pt 'Clear Sans Medium';
            color: $container_title_fg;
        }

        #container_title QPushButton {
            border: 0px;
            border-radius: 6px;
            background: $container_title_button_bg;
            color: $container_title_button_fg;
            font-size: 14px;
            padding: 2px;
        }

        #container_title QPushButton:hover {
            background: $container_title_button_hover;
        }

        #find_widget {
            border-radius: 0;
            background: $find_bg;
            color: $find_fg;
        }

        #find_widget_edit {
            background: $find_edit_bg;
            color: $find_edit_fg;
            border-radius: 6px;
            padding: 4px;
        }
        
        #find_widget QCheckBox::indicator {
            background: $find_checkbox_off;
            border-radius: 6px;
        }
        
        #find_widget QCheckBox::indicator:checked {
            background: $find_checkbox_on;
        }

        #find_widget_back {
            background: $find_arrow_bg;
            border-radius: 6px;
            padding: 4px;
            padding-right: 0px;
            padding-left: 0px;
            icon: url(custom:arrow_left.svg)
        }

        #find_widget_forward {
            background: $find_arrow_bg;
            color: $find_arrow_fg;
            border-radius: 6px;
            padding: 4px;
            padding-right: 0px;
            padding-left: 0px;
            icon: url(custom:arrow_right.svg)
        }
        
        #find_widget_back:hover, #find_widget_forward:hover {
            background: $find_arrow_hover;
        }

        #find_widget_close {
            border-radius: 6px;
            font-size: 14px;
            padding: 4px;
            padding-left: 6px;
            padding-right: 6px;
            background: $find_close_bg;
            color: $find_close_fg;
            border: 0;
        }
        
        #title_bar_icon {
            margin-top: 7px;
        }

        #title_bar_label {
            margin-top: 5px;
        }

        #minimize_button, #maximize_button {
            background: none;
            border: none;
            border: 2px solid transparent;
            image: url(custom:hide.svg);
        }

        #minimize_button:hover, #maximize_button:hover {
            background: $window_min_button;
            border-radius: 6px;
        }

        #close_button {
            background: none;
            border: none;
            border: 2px solid transparent;
            image: url(custom:close_window.svg);
        }

        #close_button:hover {
            background: $close_button;
            icon: none;
            border-radius: 6px;
        }
        
        #sections_panel {
            background: $sections_panel_bg;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            min-width: 50px;
            max-width: 50px;
        }

        #sections_panel::item {
            border-radius: 0;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QListWidget {
            show-decoration-selected: 0;
        }

        QListWidget::item {
            padding-left: 10px;
            border: 0;
            border-radius: 6px;
        }

        QListWidget::item:hover {
            background: $sections_panel_hover;
            color: $tab_widget_select_fg;
        }

        QListWidget::item:selected {
            background: $sections_panel_select;
            border-radius: 6px;
        }
        
        QTreeView::item:hover {
            background: $tree_item_hover_bg;
            color: $tree_item_hover_fg;
        }
        
        QTreeView::item:selected {
            outline: 0px;
            background: $tree_item_pressed_bg;
            color: $tree_item_pressed_fg
        }
        
        QHeaderView::section {
            background-color: $header_bg;
            color: $header_fg;
            padding-left: 12px;
            padding-right: 12px;
            padding-top: 2px;
            padding-bottom: 2px;
            border-top: 2px solid $container_content_bg;
            show-decoration-selected: 0;
        }
        
        QHeaderView::section:horizontal:first {
            border-left: 0;
        }
        
        QHeaderView::section:horizontal:last {
            border-right: 0;
        }
        
        QHeaderView::section:horizontal {
            border-right: 2px solid $container_content_bg;
        }
        
        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(custom:arrow_right(tree_item).svg);
        }
        
        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings  {
                border-image: none;
                image: url(custom:arrow_down(tree_item).svg);
        }
        
        QTreeWidget QProgressBar {
            border: 2px solid $progress_bar_border;
            border-radius: 6px;
            text-align: center;
            color: $progress_bar_fg;
            margin: 5px;
        }
        
        QTreeWidget QProgressBar::chunk {
            border-radius: 3px;
        }
        
        QTreeWidget QPushButton {
            background: $tree_button_bg;
            color: $tree_button_fg;
            border: 2px solid $tree_button_border;
        }
        
        QTreeWidget QPushButton:hover {
            background: $tree_button_hover_bg;
            color: $tree_button_hover_fg;
        }

        QTreeWidget #downloads_item_folder {
            icon: url(custom:folder(tree_item).svg);
        }
        
        QTreeWidget #downloads_item_remove {
            icon: url(custom:close(tree_item).svg);
        }
        
        QTabWidget {
            background: $tab_widget_bg;
            border: 0px;
            padding: 0px;
        }

        QTabWidget::tab-bar {
            left: 1px;
            right: 35px;
        }

        QTabBar::tab {
            margin: 4px;
            margin-top: 6px;
            margin-bottom: 5px;
            border-radius: 6px;
            min-width: 100px;
            max-width: 200px;
            color: $tab_widget_fg;
            padding: 5px;
        }

        QTabBar::tab:text {
            padding-left: 5px;
        }

        QTabWidget::pane {}

        QTabBar {
            qproperty-drawBase: 0;
        }

        QTabBar::tab:selected {
            background: $tab_widget_select_bg;
            color: $tab_widget_select_fg;
        }

        QTabBar::tab:!selected:hover {
            background: $tab_widget_hover_bg;
        }

        QTabBar::tab:!selected {
            background: $tab_widget_bg;
            color: $tab_widget_fg;
        }

        QTabBar QToolButton::right-arrow {
            image: url(custom:arrow_right.svg);
        }

        QTabBar QToolButton::left-arrow {
            image: url(custom:arrow_left.svg);
        }

        QTabBar::close-button {
            image: url(custom:close(tab_bar).svg);
            background: $tab_widget_hover_bg;
            border-radius: 6px;
            margin-right: 3px;
            min-width 15px;
        }

        QTabBar::tear {
            image: none;
        }

        #add_tab_button {
            min-width: 25px;
            min-height: 25px;
            margin-top: 8px;
            margin-left: 10px;
            background: transparent;
            icon: url(custom:add(tab_bar).svg);
            border-radius: 6px;
            border: none;
        }

        #add_tab_button:hover {
            background: $button_hover_bg;
        }

        #add_tab_button:pressed {
            border: 2px solid $button_pressed_border;
        }

        QScrollBar:horizontal {
                background: $sections_panel_bg;
                max-height: 11px;
                border-radius: 4px;
                margin-top: 3px;
        }

        QScrollBar::handle:horizontal {
                background-color: $checkbox_indicator_checked;
                min-width: 5px;
                border-radius: 4px;
        }

        QScrollBar::add-line:horizontal {
                border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
        }

        QScrollBar::sub-line:horizontal {
                border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
        }

        QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on {
                border-image: url(:/qss_icons/rc/right_arrow.png);
        }

        QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
                border-image: url(:/qss_icons/rc/left_arrow.png);
        }

        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
        }


        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
        }

        QScrollBar:vertical {
                background: $sections_panel_bg;
                max-width: 11px;
                border-radius: 4px;
                margin-left: 3px;
        }

        QScrollBar::handle:vertical {
                background-color: $checkbox_indicator_checked;
                min-height: 5px;
                border-radius: 4px;
        }

        QScrollBar::sub-line:vertical {
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
        }

        QScrollBar::add-line:vertical {
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
        }

        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
                border-image: none;
        }

        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
                border-image: none;
        }

        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
        }

        #popup_link {
            background: $bg;
            color: $fg;
            padding-left: 2px;
            padding-right: 2px;
            border-top-right-radius: 6px; 
        }

        QMenu {
            color: $context_menu_fg;
            background-color: $context_menu_bg;
            border: 2px solid $context_menu_border;
            border-radius: 6px;
        }

        QMenu::item {
            padding: 6px;
            padding-left: 6px;
            padding-right: 6px;
            background: transparent;
        }

        QMenu::item:selected {
            color: $context_menu_select_fg;
            background: $context_menu_select_bg;
            border-radius: 3px;
        }

        QMenu::separator {
            background-color: $context_menu_border;
            height: 0.1em;
        }

        """).substitute(bg=self.bg,
                        fg=self.fg,
                        button_bg=self.button['bg'],
                        button_fg=self.button['fg'],
                        button_hover_bg=self.button['hover'],
                        button_pressed_border=self.button['border'],
                        button_disabled_bg=self.rgba(self.button["hover"], 0.3),
                        combobox_bg=self.combobox['bg'],
                        combobox_fg=self.combobox['fg'],
                        combobox_item=self.combobox['item'],
                        checkbox_indicator_normal=self.check_box['normal'],
                        checkbox_indicator_checked=self.check_box['checked'],
                        search_box_bg=self.search_box['bg'],
                        search_box_fg=self.search_box['fg'],
                        search_box_item=self.search_box['item'],
                        line_edit_bg=self.line_edit['bg'],
                        line_edit_fg=self.line_edit['fg'],
                        line_edit_border=self.line_edit['border'],
                        line_edit_hover=self.line_edit['hover'],
                        address_panel_button_border=self.address_panel_button['border'],
                        address_panel_button_hover=self.address_panel_button['hover'],
                        address_line_frame_fg=self.address_line_frame['fg'],
                        address_line_frame_bg=self.address_line_frame['bg'],
                        address_line_frame_border=self.address_line_frame['border'],
                        address_line_frame_hover=self.address_line_frame['hover'],
                        progress_bar_fg=self.progress_bar['fg'],
                        progress_bar_chunk=self.progress_bar['chunk'],
                        progress_bar_border=self.progress_bar['border'],
                        header_bg=self.tree_widget['header_bg'],
                        header_fg=self.tree_widget['header_fg'],
                        tree_item_hover_bg=self.tree_widget['hover_bg'],
                        tree_item_hover_fg=self.tree_widget['hover_fg'],
                        tree_item_pressed_bg=self.tree_widget['pressed_bg'],
                        tree_item_pressed_fg=self.tree_widget['pressed_fg'],
                        tree_button_bg=self.tree_widget['button_bg'],
                        tree_button_fg=self.tree_widget['button_fg'],
                        tree_button_hover_bg=self.tree_widget['button_hover_bg'],
                        tree_button_hover_fg=self.tree_widget['button_hover_fg'],
                        tree_button_border=self.tree_widget['button_border'],
                        find_bg=self.find_on_page_widget['bg'],
                        find_fg=self.find_on_page_widget['fg'],
                        find_edit_bg=self.find_on_page_widget['line_edit_bg'],
                        find_edit_fg=self.find_on_page_widget['line_edit_fg'],
                        find_checkbox_on=self.find_on_page_widget['checkbox_on'],
                        find_checkbox_off=self.find_on_page_widget['checkbox_off'],
                        find_arrow_bg=self.find_on_page_widget['btn_arrow_bg'],
                        find_arrow_fg=self.find_on_page_widget['btn_arrow_fg'],
                        find_arrow_hover=self.find_on_page_widget['btn_arrow_hover'],
                        find_close_bg=self.find_on_page_widget['btn_close_bg'],
                        find_close_fg=self.find_on_page_widget['btn_close_fg'],
                        container_title_bg=self.container_title['bg'],
                        container_title_fg=self.container_title['fg'],
                        container_title_alt_fg=self.container_title['alt_fg'],
                        container_title_button_bg=self.container_title_btn['bg'],
                        container_title_button_fg=self.container_title_btn['fg'],
                        container_title_button_hover=self.container_title_btn['hover'],
                        container_content_bg=self.container['bg'],
                        container_content_fg=self.container['fg'],
                        close_button=self.title_buttons_color['close'],
                        window_min_button=self.title_buttons_color['min'],
                        tool_tip_border=self.line_edit['border'],
                        sections_panel_bg=self.sections_panel['bg'],
                        sections_panel_hover=self.sections_panel['hover'],
                        sections_panel_select=self.sections_panel['select'],
                        context_menu_fg=self.fg,
                        context_menu_bg=self.bg,
                        context_menu_border=self.search_box['bg'],
                        context_menu_select_bg=self.container['bg'],
                        context_menu_select_fg=self.container['fg'],
                        tab_widget_bg=self.tab_widget['bg'],
                        tab_widget_fg=self.tab_widget['fg'],
                        tab_widget_select_bg=self.tab_widget['select_bg'],
                        tab_widget_select_fg=self.tab_widget['select_fg'],
                        tab_widget_hover_bg=self.tab_widget['hover'],
                        tab_widget_button_fg=self.tab_widget['button_fg'],
                        download_item_bg=self.download_item['bg'],
                        download_item_fg=self.download_item['fg'],
                        download_item_alt_fg=self.download_item['alt_fg'])
