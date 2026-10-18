# -*- coding: utf-8 -*-

import os
import json
import calendar
import uuid
from datetime import datetime

from kivy.config import Config

Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "resizable", "1")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp, sp

from kivy.graphics import (
    Color,
    RoundedRectangle,
    Line,
    Ellipse,
)

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


# =========================================================
# 颜色
# =========================================================

BG = (0.965, 0.975, 0.985, 1)
WHITE = (1, 1, 1, 1)

TEXT = (0.12, 0.15, 0.20, 1)
SUBTEXT = (0.48, 0.51, 0.57, 1)

BLUE = (0.12, 0.42, 0.95, 1)
BLUE_LIGHT = (0.91, 0.95, 1.0, 1)

GREEN = (0.12, 0.65, 0.38, 1)
GREEN_LIGHT = (0.91, 0.97, 0.93, 1)

RED = (0.92, 0.25, 0.25, 1)
RED_LIGHT = (1.0, 0.93, 0.93, 1)

BORDER = (0.88, 0.90, 0.94, 1)

Window.clearcolor = BG


# =========================================================
# 字体
# =========================================================

def find_font():

    paths = [
        "/system/fonts/NotoSansCJK-Regular.ttc",
        "/system/fonts/NotoSansSC-Regular.otf",
        "/system/fonts/NotoSans-Regular.ttf",

        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyh.ttf",
        "C:/Windows/Fonts/simhei.ttf",

        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf",
    ]

    for path in paths:

        if os.path.exists(path):
            return path

    return None


FONT_PATH = find_font()

if FONT_PATH:

    try:

        LabelBase.register(
            name="AppFont",
            fn_regular=FONT_PATH
        )

        APP_FONT = "AppFont"

    except Exception:

        APP_FONT = "Roboto"

else:

    APP_FONT = "Roboto"


# =========================================================
# 工具
# =========================================================

def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        text = str(value).strip()

        if not text:
            return default

        return float(text)

    except Exception:

        return default


def money(value):

    try:

        return f"{float(value):.2f}"

    except Exception:

        return "0.00"


def now_time():

    return datetime.now().strftime("%H:%M")


# =========================================================
# 圆角按钮
# =========================================================

class RoundButton(Button):

    def __init__(
        self,
        bg_color=WHITE,
        radius=10,
        border_color=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self._bg_color = bg_color
        self._radius = radius
        self._border_color = border_color

        with self.canvas.before:

            self._bg = Color(
                *self._bg_color
            )

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(self._radius)]
            )

            if self._border_color:

                self._border = Color(
                    *self._border_color
                )

                self._line = Line(
                    rounded_rectangle=(
                        self.x,
                        self.y,
                        self.width,
                        self.height,
                        dp(self._radius)
                    ),
                    width=1
                )

        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics
        )

    def _update_graphics(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size

        if self._border_color:

            self._line.rounded_rectangle = (
                self.x,
                self.y,
                self.width,
                self.height,
                dp(self._radius)
            )

    def set_background(self, color):

        self._bg_color = color

        try:
            self._bg.rgba = color
        except Exception:
            pass


# =========================================================
# 卡片
# =========================================================

class Card(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.padding = dp(10)

        with self.canvas.before:

            self._color = Color(*WHITE)

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

            self._line_color = Color(*BORDER)

            self._line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(14)
                ),
                width=1
            )

        self.bind(
            pos=self._refresh,
            size=self._refresh
        )

    def _refresh(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size

        self._line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(14)
        )


# =========================================================
# 输入框
# =========================================================

class StyledInput(TextInput):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.font_name = APP_FONT
        self.font_size = sp(15)

        self.foreground_color = TEXT
        self.cursor_color = BLUE

        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)

        self.padding = (
            dp(12),
            dp(8),
            dp(12),
            dp(8)
        )

        with self.canvas.before:

            self._bg = Color(*WHITE)

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )

            self._border_color = Color(*BORDER)

            self._line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(10)
                ),
                width=1
            )

        self.bind(
            pos=self._refresh,
            size=self._refresh,
            focus=self._refresh
        )

    def _refresh(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size

        self._line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(10)
        )

        if self.focus:
            self._border_color.rgba = BLUE
        else:
            self._border_color.rgba = BORDER


# =========================================================
# 底部图标
# =========================================================

class TagButton(Button):

    def __init__(
        self,
        icon_type="calendar",
        **kwargs
    ):

        super().__init__(**kwargs)

        self.icon_type = icon_type
        self.active = False

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.bind(
            pos=self._redraw,
            size=self._redraw
        )

    def _redraw(self, *args):

        self.canvas.clear()

        color = (
            BLUE
            if self.active
            else SUBTEXT
        )

        with self.canvas:

            Color(*color)

            cx = self.center_x
            cy = self.center_y

            # ---------------------------------------------
            # 日历
            # ---------------------------------------------

            if self.icon_type == "calendar":

                RoundedRectangle(
                    pos=(
                        cx - dp(10),
                        cy - dp(8)
                    ),
                    size=(
                        dp(20),
                        dp(17)
                    ),
                    radius=[dp(3)]
                )

                Color(*WHITE)

                Line(
                    points=[
                        cx - dp(10),
                        cy + dp(3),
                        cx + dp(10),
                        cy + dp(3)
                    ],
                    width=1.2
                )

                Color(*color)

                Line(
                    points=[
                        cx - dp(5),
                        cy + dp(10),
                        cx - dp(5),
                        cy + dp(5)
                    ],
                    width=1.5
                )

                Line(
                    points=[
                        cx + dp(5),
                        cy + dp(10),
                        cx + dp(5),
                        cy + dp(5)
                    ],
                    width=1.5
                )

            # ---------------------------------------------
            # 近期：时钟
            # ---------------------------------------------

            elif self.icon_type == "recent":

                Line(
                    circle=(
                        cx,
                        cy,
                        dp(10),
                        0,
                        360
                    ),
                    width=1.6
                )

                Line(
                    points=[
                        cx,
                        cy,
                        cx,
                        cy + dp(5)
                    ],
                    width=1.6
                )

                Line(
                    points=[
                        cx,
                        cy,
                        cx + dp(5),
                        cy - dp(3)
                    ],
                    width=1.6
                )

            # ---------------------------------------------
            # 我的：人
            # ---------------------------------------------

            elif self.icon_type == "mine":

                # 头
                Ellipse(
                    pos=(
                        cx - dp(4),
                        cy + dp(2),
                    ),
                    size=(
                        dp(8),
                        dp(8)
                    )
                )

                # 身体
                RoundedRectangle(
                    pos=(
                        cx - dp(9),
                        cy - dp(9)
                    ),
                    size=(
                        dp(18),
                        dp(10)
                    ),
                    radius=[dp(5)]
                )


# =========================================================
# 日历日期
#
# 有账单：
# 浅蓝色背景
#
# 无账单：
# 白色
# =========================================================

class DayButton(Button):

    def __init__(
        self,
        day=0,
        has_record=False,
        this_month=True,
        selected=False,
        callback_func=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.day = day
        self.has_record = has_record
        self.this_month = this_month
        self.selected = selected
        self.callback_func = callback_func

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.padding = (0, 0)

        self.day_label = Label(
            text=str(day) if day else "",
            font_name=APP_FONT,
            font_size=sp(13),
            color=TEXT,
            halign="center",
            valign="middle",
            size_hint=(None, None)
        )

        self.add_widget(
            self.day_label
        )

        with self.canvas.before:

            self._cell_color = Color(*WHITE)

            self._cell_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(7)]
            )

            self._badge_color = Color(*BG)

            self._badge_rect = RoundedRectangle(
                pos=(0, 0),
                size=(dp(25), dp(25)),
                radius=[dp(5)]
            )

        self.bind(
            pos=self._redraw,
            size=self._redraw
        )

        self.bind(
            on_release=self._clicked
        )

        self._redraw()

    def _clicked(self, *args):

        if callable(self.callback_func):

            self.callback_func(
                self.day
            )

    def _redraw(self, *args):

        w = self.width
        h = self.height

        if w <= 0 or h <= 0:
            return

        self._cell_rect.pos = self.pos
        self._cell_rect.size = self.size

        # =================================================
        # 有账单：浅色背景
        # =================================================

        if self.has_record:

            self._cell_color.rgba = (
                0.95,
                0.97,
                1.0,
                1
            )

        else:

            self._cell_color.rgba = WHITE

        # =================================================
        # 选中日期
        # =================================================

        badge_size = min(
            dp(25),
            max(
                dp(20),
                w - dp(8)
            )
        )

        badge_x = (
            self.x +
            (w - badge_size) / 2
        )

        badge_y = (
            self.top -
            badge_size -
            dp(4)
        )

        self._badge_rect.pos = (
            badge_x,
            badge_y
        )

        self._badge_rect.size = (
            badge_size,
            badge_size
        )

        if self.selected:

            self._badge_color.rgba = BLUE
            self.day_label.color = WHITE

        else:

            self._badge_color.rgba = (
                0.93,
                0.95,
                0.98,
                1
            )

            if self.this_month:

                self.day_label.color = TEXT

            else:

                self.day_label.color = (
                    0.70,
                    0.73,
                    0.77,
                    1
                )

        self.day_label.size = (
            badge_size,
            badge_size
        )

        self.day_label.pos = (
            badge_x,
            badge_y
        )


# =========================================================
# Popup内容容器
#
# 不给 Popup 自己画内容背景
# Popup 只负责窗口
# =========================================================

class PopupPanel(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.padding = dp(14)

        self.spacing = dp(9)

        with self.canvas.before:

            self._color = Color(*WHITE)

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(16)]
            )

        self.bind(
            pos=self._refresh,
            size=self._refresh
        )

    def _refresh(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size


# =========================================================
# 主程序
# =========================================================

class AccountingApp(App):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.title = "记账"

        self.data_file = os.path.join(
            self.user_data_dir,
            "accounting_data.json"
        )

        self.data = {
            "initial_balance": 0.0,

            "platform_balances": {
                "现金": 0.0,
                "银行卡": 0.0,
                "支付宝": 0.0,
                "微信": 0.0
            },

            "records": {}
        }

        now = datetime.now()

        self.current_year = min(
            2040,
            max(
                2020,
                now.year
            )
        )

        self.current_month = now.month

        self.selected_day = now.day

        self.current_page = "account"

        self.root_layout = None
        self.content = None

        self.bottom_bar = None

        self.fab = None

        self.calendar_grid = None

        self.month_label = None

        self.detail_box = None

        self.load_data()

    # =====================================================
    # 数据
    # =====================================================

    def load_data(self):

        try:

            if not os.path.exists(
                self.data_file
            ):
                return

            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as f:

                loaded = json.load(f)

            if isinstance(
                loaded,
                dict
            ):

                self.data.update(
                    loaded
                )

            if not isinstance(
                self.data.get(
                    "platform_balances"
                ),
                dict
            ):

                self.data[
                    "platform_balances"
                ] = {}

            if not isinstance(
                self.data.get(
                    "records"
                ),
                dict
            ):

                self.data[
                    "records"
                ] = {}

            self.data[
                "initial_balance"
            ] = safe_float(
                self.data.get(
                    "initial_balance",
                    0
                )
            )

        except Exception:

            self.data = {
                "initial_balance": 0.0,

                "platform_balances": {
                    "现金": 0.0,
                    "银行卡": 0.0,
                    "支付宝": 0.0,
                    "微信": 0.0
                },

                "records": {}
            }

    def save_data(self):

        try:

            folder = os.path.dirname(
                self.data_file
            )

            os.makedirs(
                folder,
                exist_ok=True
            )

            temp_file = (
                self.data_file +
                ".tmp"
            )

            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

            if os.path.exists(
                self.data_file
            ):

                try:
                    os.remove(
                        self.data_file
                    )
                except Exception:
                    pass

            os.replace(
                temp_file,
                self.data_file
            )

        except Exception:
            pass

    def get_records(
        self,
        date_key
    ):

        result = self.data.get(
            "records",
            {}
        ).get(
            date_key,
            []
        )

        if isinstance(
            result,
            list
        ):

            return result

        return []

    def day_total(
        self,
        date_key
    ):

        income = 0.0
        expense = 0.0

        for item in self.get_records(
            date_key
        ):

            amount = safe_float(
                item.get(
                    "amount",
                    0
                )
            )

            if item.get(
                "type"
            ) == "income":

                income += amount

            else:

                expense += amount

        return income, expense

    def has_record(
        self,
        date_key
    ):

        records = self.get_records(
            date_key
        )

        return len(records) > 0

    def platform_balance(
        self,
        platform
    ):

        balance = safe_float(
            self.data.get(
                "platform_balances",
                {}
            ).get(
                platform,
                0
            )
        )

        for records in self.data.get(
            "records",
            {}
        ).values():

            if not isinstance(
                records,
                list
            ):
                continue

            for item in records:

                if item.get(
                    "platform"
                ) != platform:

                    continue

                amount = safe_float(
                    item.get(
                        "amount",
                        0
                    )
                )

                if item.get(
                    "type"
                ) == "income":

                    balance += amount

                else:

                    balance -= amount

        return balance

    def total_balance(self):

        total = safe_float(
            self.data.get(
                "initial_balance",
                0
            )
        )

        for records in self.data.get(
            "records",
            {}
        ).values():

            if not isinstance(
                records,
                list
            ):
                continue

            for item in records:

                amount = safe_float(
                    item.get(
                        "amount",
                        0
                    )
                )

                if item.get(
                    "type"
                ) == "income":

                    total += amount

                else:

                    total -= amount

        return total

    # =====================================================
    # 构建
    # =====================================================

    def build(self):

        self.root_layout = FloatLayout()

        self.content = FloatLayout(
            size_hint=(1, 1)
        )

        self.root_layout.add_widget(
            self.content
        )

        self.create_bottom_bar()

        self.create_fab()

        self.switch_page(
            "account"
        )

        return self.root_layout

    # =====================================================
    # 底部导航
    # =====================================================

    def create_bottom_bar(self):

        self.bottom_bar = BoxLayout(
            orientation="horizontal",
            spacing=dp(3),
            padding=dp(4),
            size_hint=(None, None),
            size=(
                min(
                    Window.width - dp(14),
                    dp(520)
                ),
                dp(62)
            ),
            pos=(
                dp(7),
                dp(7)
            )
        )

        with self.bottom_bar.canvas.before:

            Color(*WHITE)

            self.bottom_bg = RoundedRectangle(
                pos=self.bottom_bar.pos,
                size=self.bottom_bar.size,
                radius=[dp(18)]
            )

            Color(*BORDER)

            self.bottom_line = Line(
                rounded_rectangle=(
                    self.bottom_bar.x,
                    self.bottom_bar.y,
                    self.bottom_bar.width,
                    self.bottom_bar.height,
                    dp(18)
                ),
                width=1
            )

        self.bottom_bar.bind(
            pos=self._update_bottom_graphics,
            size=self._update_bottom_graphics
        )

        self.tag_account = TagButton(
            icon_type="calendar"
        )

        self.tag_recent = TagButton(
            icon_type="recent"
        )

        self.tag_mine = TagButton(
            icon_type="mine"
        )

        self.tag_account.bind(
            on_release=lambda x:
            self.switch_page(
                "account"
            )
        )

        self.tag_recent.bind(
            on_release=lambda x:
            self.switch_page(
                "recent"
            )
        )

        self.tag_mine.bind(
            on_release=lambda x:
            self.switch_page(
                "mine"
            )
        )

        self.bottom_bar.add_widget(
            self.tag_account
        )

        self.bottom_bar.add_widget(
            self.tag_recent
        )

        self.bottom_bar.add_widget(
            self.tag_mine
        )

        self.root_layout.add_widget(
            self.bottom_bar
        )

    def _update_bottom_graphics(
        self,
        *args
    ):

        self.bottom_bg.pos = (
            self.bottom_bar.pos
        )

        self.bottom_bg.size = (
            self.bottom_bar.size
        )

        self.bottom_line.rounded_rectangle = (
            self.bottom_bar.x,
            self.bottom_bar.y,
            self.bottom_bar.width,
            self.bottom_bar.height,
            dp(18)
        )

    def update_tags(self):

        self.tag_account.active = (
            self.current_page ==
            "account"
        )

        self.tag_recent.active = (
            self.current_page ==
            "recent"
        )

        self.tag_mine.active = (
            self.current_page ==
            "mine"
        )

        self.tag_account._redraw()
        self.tag_recent._redraw()
        self.tag_mine._redraw()

    # =====================================================
    # FAB
    # =====================================================

    def create_fab(self):

        self.fab = RoundButton(
            text="+",
            font_name=APP_FONT,
            font_size=sp(27),
            color=WHITE,
            bg_color=BLUE,
            radius=25,
            size_hint=(None, None),
            size=(
                dp(50),
                dp(50)
            )
        )

        self.fab.bind(
            on_release=lambda x:
            self.open_add_record()
        )

        self.root_layout.add_widget(
            self.fab
        )

        self.update_fab()

    def update_fab(self):

        if not self.fab:
            return

        if self.current_page == "account":

            self.fab.opacity = 1
            self.fab.disabled = False

            self.fab.pos = (
                Window.width -
                dp(62),

                dp(80)
            )

        else:

            self.fab.opacity = 0
            self.fab.disabled = True

    # =====================================================
    # 页面
    # =====================================================

    def switch_page(
        self,
        page
    ):

        self.current_page = page

        self.content.clear_widgets()

        self.calendar_grid = None
        self.month_label = None
        self.detail_box = None

        if page == "account":

            self.build_account()

        elif page == "recent":

            self.build_recent()

        elif page == "mine":

            self.build_mine()

        self.update_tags()

        self.update_fab()

    # =====================================================
    # 记账页面
    # =====================================================

    def build_account(self):

        page = BoxLayout(
            orientation="vertical",
            padding=(
                dp(5),
                dp(3),
                dp(5),
                dp(76)
            ),
            spacing=dp(3)
        )

        # -------------------------------------------------
        # 月份
        # -------------------------------------------------

        month_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(37),
            spacing=dp(5)
        )

        prev_button = RoundButton(
            text="‹",
            font_name=APP_FONT,
            font_size=sp(25),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint=(None, 1),
            width=dp(43)
        )

        self.month_label = Button(
            text="",
            font_name=APP_FONT,
            font_size=sp(16),
            bold=True,
            color=TEXT,
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        next_button = RoundButton(
            text="›",
            font_name=APP_FONT,
            font_size=sp(25),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint=(None, 1),
            width=dp(43)
        )

        prev_button.bind(
            on_release=lambda x:
            self.change_month(-1)
        )

        next_button.bind(
            on_release=lambda x:
            self.change_month(1)
        )

        self.month_label.bind(
            on_release=lambda x:
            self.open_year_popup()
        )

        month_bar.add_widget(
            prev_button
        )

        month_bar.add_widget(
            self.month_label
        )

        month_bar.add_widget(
            next_button
        )

        page.add_widget(
            month_bar
        )

        # -------------------------------------------------
        # 星期
        # -------------------------------------------------

        week_grid = GridLayout(
            cols=7,
            spacing=dp(2),
            size_hint_y=None,
            height=dp(21)
        )

        for name in [
            "一",
            "二",
            "三",
            "四",
            "五",
            "六",
            "日"
        ]:

            week_grid.add_widget(
                Label(
                    text=name,
                    font_name=APP_FONT,
                    font_size=sp(10),
                    color=SUBTEXT,
                    halign="center",
                    valign="middle"
                )
            )

        page.add_widget(
            week_grid
        )

        # -------------------------------------------------
        # 日历
        # -------------------------------------------------

        calendar_box = self.create_calendar()

        page.add_widget(
            calendar_box
        )

        # -------------------------------------------------
        # 账单详情
        # -------------------------------------------------

        self.detail_box = Card(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(4),
            size_hint_y=1
        )

        page.add_widget(
            self.detail_box
        )

        self.content.add_widget(
            page
        )

        self.refresh_account_header()

        self.refresh_detail()

    # =====================================================
    # 日历高度
    # =====================================================

    def get_calendar_height(self):

        h = Window.height

        if h < dp(650):

            row = dp(38)

        elif h < dp(800):

            row = dp(42)

        elif h < dp(1000):

            row = dp(45)

        else:

            row = dp(48)

        return (
            row * 6 +
            dp(2) * 5
        )

    # =====================================================
    # 创建日历
    # =====================================================

    def create_calendar(self):

        grid = GridLayout(
            cols=7,
            rows=6,
            spacing=dp(2),
            padding=0,
            size_hint_y=None,
            height=self.get_calendar_height()
        )

        self.calendar_grid = grid

        year = self.current_year
        month = self.current_month

        cal = calendar.Calendar(
            firstweekday=0
        )

        weeks = cal.monthdayscalendar(
            year,
            month
        )

        while len(weeks) < 6:

            weeks.append(
                [0] * 7
            )

        if month == 1:

            prev_year = year - 1
            prev_month = 12

        else:

            prev_year = year
            prev_month = month - 1

        if month == 12:

            next_year = year + 1
            next_month = 1

        else:

            next_year = year
            next_month = month + 1

        prev_days = calendar.monthrange(
            prev_year,
            prev_month
        )[1]

        first_week = weeks[0]

        leading = 0

        for value in first_week:

            if value == 0:
                leading += 1
            else:
                break

        cells = []

        for i in range(leading):

            cells.append(
                (
                    prev_days -
                    leading +
                    i +
                    1,

                    prev_year,
                    prev_month,
                    False
                )
            )

        for week in weeks:

            for day in week:

                if day:

                    cells.append(
                        (
                            day,
                            year,
                            month,
                            True
                        )
                    )

        normal_count = len(cells)

        for day in range(
            1,
            43 - normal_count
        ):

            cells.append(
                (
                    day,
                    next_year,
                    next_month,
                    False
                )
            )

        cells = cells[:42]

        for (
            day,
            cell_year,
            cell_month,
            this_month
        ) in cells:

            date_key = (
                f"{cell_year:04d}-"
                f"{cell_month:02d}-"
                f"{day:02d}"
            )

            selected = (
                this_month
                and cell_year ==
                self.current_year
                and cell_month ==
                self.current_month
                and day ==
                self.selected_day
            )

            button = DayButton(
                day=day,

                has_record=self.has_record(
                    date_key
                ),

                this_month=this_month,

                selected=selected,

                callback_func=lambda d,
                yy=cell_year,
                mm=cell_month,
                tm=this_month:
                self.select_date(
                    d,
                    yy,
                    mm,
                    tm
                )
            )

            grid.add_widget(
                button
            )

        return grid

    # =====================================================
    # 刷新日期
    # =====================================================

    def select_date(
        self,
        day,
        year,
        month,
        this_month
    ):

        if not this_month:

            if year < 2020:
                return

            if year > 2040:
                return

        self.current_year = year
        self.current_month = month
        self.selected_day = day

        self.switch_page(
            "account"
        )

    def refresh_account_header(self):

        if self.month_label:

            self.month_label.text = (
                f"{self.current_year}年"
                f"{self.current_month:02d}月"
            )

    def refresh_detail(self):

        if not self.detail_box:
            return

        self.detail_box.clear_widgets()

        date_key = (
            f"{self.current_year:04d}-"
            f"{self.current_month:02d}-"
            f"{self.selected_day:02d}"
        )

        title = Label(
            text=(
                f"{self.current_month}月"
                f"{self.selected_day}日"
                f" 账单"
            ),
            font_name=APP_FONT,
            font_size=sp(14),
            bold=True,
            color=TEXT,
            size_hint_y=None,
            height=dp(28),
            halign="left",
            valign="middle"
        )

        self.detail_box.add_widget(
            title
        )

        records = self.get_records(
            date_key
        )

        if not records:

            self.detail_box.add_widget(
                Label(
                    text="今天还没有账单",
                    font_name=APP_FONT,
                    font_size=sp(12),
                    color=SUBTEXT,
                    halign="center",
                    valign="middle"
                )
            )

            return

        scroll = ScrollView(
            do_scroll_x=False
        )

        list_box = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None
        )

        list_box.bind(
            minimum_height=
            list_box.setter("height")
        )

        for item in reversed(
            records
        ):

            list_box.add_widget(
                self.record_row(item)
            )

        scroll.add_widget(
            list_box
        )

        self.detail_box.add_widget(
            scroll
        )

    # =====================================================
    # 账单行
    # =====================================================

    def record_row(
        self,
        item
    ):

        kind = item.get(
            "type",
            "expense"
        )

        amount = safe_float(
            item.get(
                "amount",
                0
            )
        )

        platform = item.get(
            "platform",
            "未设置"
        )

        remark = item.get(
            "remark",
            ""
        )

        time = item.get(
            "time",
            ""
        )

        if kind == "income":

            kind_text = "收入"
            amount_text = "+" + money(
                amount
            )
            amount_color = GREEN

        else:

            kind_text = "支出"
            amount_text = "-" + money(
                amount
            )
            amount_color = RED

        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            padding=(
                dp(8),
                dp(5)
            ),
            size_hint_y=None,
            height=dp(50)
        )

        with row.canvas.before:

            Color(*WHITE)

            rect = RoundedRectangle(
                pos=row.pos,
                size=row.size,
                radius=[dp(9)]
            )

            Color(*BORDER)

            line = Line(
                rounded_rectangle=(
                    row.x,
                    row.y,
                    row.width,
                    row.height,
                    dp(9)
                ),
                width=1
            )

        row.bind(
            pos=lambda obj, val:
            self._row_bg(
                rect,
                line,
                obj
            ),

            size=lambda obj, val:
            self._row_bg(
                rect,
                line,
                obj
            )
        )

        left = BoxLayout(
            orientation="vertical"
        )

        top = Label(
            text=(
                f"{kind_text}  "
                f"{platform}"
            ),
            font_name=APP_FONT,
            font_size=sp(11.5),
            color=TEXT,
            halign="left",
            valign="middle"
        )

        bottom = Label(
            text=(
                remark +
                (
                    f"  {time}"
                    if time
                    else ""
                )
            ),
            font_name=APP_FONT,
            font_size=sp(9),
            color=SUBTEXT,
            halign="left",
            valign="middle"
        )

        left.add_widget(top)
        left.add_widget(bottom)

        amount_label = Label(
            text=amount_text,
            font_name=APP_FONT,
            font_size=sp(13),
            bold=True,
            color=amount_color,
            size_hint_x=None,
            width=dp(82),
            halign="right",
            valign="middle"
        )

        row.add_widget(left)
        row.add_widget(amount_label)

        return row

    def _row_bg(
        self,
        rect,
        line,
        widget
    ):

        rect.pos = widget.pos
        rect.size = widget.size

        line.rounded_rectangle = (
            widget.x,
            widget.y,
            widget.width,
            widget.height,
            dp(9)
        )

    # =====================================================
    # 月份
    # =====================================================

    def change_month(
        self,
        offset
    ):

        month = (
            self.current_month +
            offset
        )

        year = self.current_year

        if month < 1:

            month = 12
            year -= 1

        elif month > 12:

            month = 1
            year += 1

        if year < 2020:

            year = 2020
            month = 1

        if year > 2040:

            year = 2040
            month = 12

        self.current_year = year
        self.current_month = month

        max_day = calendar.monthrange(
            year,
            month
        )[1]

        self.selected_day = min(
            self.selected_day,
            max_day
        )

        self.switch_page(
            "account"
        )

    # =====================================================
    # 年份弹窗
    # =====================================================

    def open_year_popup(self):

        panel = PopupPanel()

        title = Label(
            text="选择年份",
            font_name=APP_FONT,
            font_size=sp(17),
            bold=True,
            color=TEXT,
            size_hint_y=None,
            height=dp(32)
        )

        panel.add_widget(
            title
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        year_grid = GridLayout(
            cols=3,
            spacing=dp(7),
            padding=dp(2),
            size_hint_y=None
        )

        year_grid.bind(
            minimum_height=
            year_grid.setter("height")
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.86, 0.78),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=True
        )

        for year in range(
            2020,
            2041
        ):

            active = (
                year ==
                self.current_year
            )

            button = RoundButton(
                text=str(year),
                font_name=APP_FONT,
                font_size=sp(14),
                color=(
                    WHITE
                    if active
                    else TEXT
                ),
                bg_color=(
                    BLUE
                    if active
                    else WHITE
                ),
                border_color=(
                    None
                    if active
                    else BORDER
                ),
                radius=9,
                size_hint_y=None,
                height=dp(42)
            )

            button.bind(
                on_release=lambda x,
                y=year:
                self._choose_year(
                    y,
                    popup
                )
            )

            year_grid.add_widget(
                button
            )

        scroll.add_widget(
            year_grid
        )

        panel.add_widget(
            scroll
        )

        close_btn = RoundButton(
            text="关闭",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint_y=None,
            height=dp(42)
        )

        panel.add_widget(
            close_btn
        )

        close_btn.bind(
            on_release=popup.dismiss
        )

        popup.open()

    def _choose_year(
        self,
        year,
        popup
    ):

        self.current_year = year

        max_day = calendar.monthrange(
            year,
            self.current_month
        )[1]

        self.selected_day = min(
            self.selected_day,
            max_day
        )

        popup.dismiss()

        self.switch_page(
            "account"
        )

    # =====================================================
    # 添加账单
    # =====================================================

    def open_add_record(self):

        panel = PopupPanel()

        title = Label(
            text="添加账单",
            font_name=APP_FONT,
            font_size=sp(18),
            bold=True,
            color=TEXT,
            size_hint_y=None,
            height=dp(32)
        )

        panel.add_widget(title)

        # -------------------------------------------------
        # 类型
        # -------------------------------------------------

        type_box = BoxLayout(
            spacing=dp(7),
            size_hint_y=None,
            height=dp(40)
        )

        expense_btn = RoundButton(
            text="支出",
            font_name=APP_FONT,
            font_size=sp(14),
            color=WHITE,
            bg_color=RED,
            radius=9
        )

        income_btn = RoundButton(
            text="收入",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        type_box.add_widget(
            expense_btn
        )

        type_box.add_widget(
            income_btn
        )

        panel.add_widget(
            type_box
        )

        selected_type = {
            "value": "expense"
        }

        def set_expense(*args):

            selected_type["value"] = (
                "expense"
            )

            expense_btn.set_background(
                RED
            )

            expense_btn.color = WHITE

            income_btn.set_background(
                WHITE
            )

            income_btn.color = TEXT

        def set_income(*args):

            selected_type["value"] = (
                "income"
            )

            income_btn.set_background(
                GREEN
            )

            income_btn.color = WHITE

            expense_btn.set_background(
                WHITE
            )

            expense_btn.color = TEXT

        expense_btn.bind(
            on_release=set_expense
        )

        income_btn.bind(
            on_release=set_income
        )

        # -------------------------------------------------
        # 金额
        # -------------------------------------------------

        amount_input = StyledInput(
            text="0.00",
            hint_text="金额",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44)
        )

        panel.add_widget(
            amount_input
        )

        # -------------------------------------------------
        # 平台
        # -------------------------------------------------

        platform_button = RoundButton(
            text="渠道 / 平台：现金",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint_y=None,
            height=dp(44)
        )

        selected_platform = {
            "value": "现金"
        }

        platform_button.bind(
            on_release=lambda x:
            self.choose_platform(
                selected_platform,
                platform_button
            )
        )

        panel.add_widget(
            platform_button
        )

        # -------------------------------------------------
        # 备注
        # -------------------------------------------------

        remark_input = StyledInput(
            hint_text="备注",
            multiline=False,
            size_hint_y=None,
            height=dp(44)
        )

        panel.add_widget(
            remark_input
        )

        # -------------------------------------------------
        # 按钮
        # -------------------------------------------------

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel_btn = RoundButton(
            text="取消",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        save_btn = RoundButton(
            text="保存",
            font_name=APP_FONT,
            font_size=sp(14),
            color=WHITE,
            bg_color=BLUE,
            radius=9
        )

        buttons.add_widget(
            cancel_btn
        )

        buttons.add_widget(
            save_btn
        )

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.88, None),
            height=dp(365),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel_btn.bind(
            on_release=popup.dismiss
        )

        def save_record(*args):

            amount = round(
                safe_float(
                    amount_input.text
                ),
                2
            )

            if amount <= 0:

                self.show_message(
                    "请输入正确金额"
                )

                return

            date_key = (
                f"{self.current_year:04d}-"
                f"{self.current_month:02d}-"
                f"{self.selected_day:02d}"
            )

            if date_key not in self.data[
                "records"
            ]:

                self.data[
                    "records"
                ][date_key] = []

            record = {
                "id": str(
                    uuid.uuid4()
                ),

                "type":
                    selected_type["value"],

                "amount":
                    amount,

                "platform":
                    selected_platform["value"],

                "remark":
                    remark_input.text.strip(),

                "time":
                    now_time()
            }

            self.data[
                "records"
            ][date_key].append(
                record
            )

            self.save_data()

            popup.dismiss()

            self.switch_page(
                "account"
            )

        save_btn.bind(
            on_release=save_record
        )

        popup.open()

        amount_input.text = "0.00"

    # =====================================================
    # 平台选择
    # =====================================================

    def choose_platform(
        self,
        selected_platform,
        platform_button
    ):

        platforms = list(
            self.data.get(
                "platform_balances",
                {}
            ).keys()
        )

        if not platforms:

            platforms = [
                "现金"
            ]

        panel = PopupPanel()

        title = Label(
            text="选择渠道 / 平台",
            font_name=APP_FONT,
            font_size=sp(17),
            bold=True,
            color=TEXT,
            size_hint_y=None,
            height=dp(32)
        )

        panel.add_widget(title)

        scroll = ScrollView(
            do_scroll_x=False
        )

        grid = GridLayout(
            cols=1,
            spacing=dp(6),
            size_hint_y=None
        )

        grid.bind(
            minimum_height=
            grid.setter("height")
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.82, 0.65),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0)
        )

        for platform in platforms:

            button = RoundButton(
                text=platform,
                font_name=APP_FONT,
                font_size=sp(14),
                color=TEXT,
                bg_color=WHITE,
                border_color=BORDER,
                radius=9,
                size_hint_y=None,
                height=dp(42)
            )

            button.bind(
                on_release=lambda x,
                p=platform:
                self._set_platform(
                    p,
                    selected_platform,
                    platform_button,
                    popup
                )
            )

            grid.add_widget(
                button
            )

        scroll.add_widget(
            grid
        )

        panel.add_widget(
            scroll
        )

        close_btn = RoundButton(
            text="取消",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint_y=None,
            height=dp(42)
        )

        panel.add_widget(
            close_btn
        )

        close_btn.bind(
            on_release=popup.dismiss
        )

        popup.open()

    def _set_platform(
        self,
        platform,
        selected_platform,
        platform_button,
        popup
    ):

        selected_platform["value"] = (
            platform
        )

        platform_button.text = (
            "渠道 / 平台：" +
            platform
        )

        popup.dismiss()

    # =====================================================
    # 近期页面
    # =====================================================

    def build_recent(self):
        root = BoxLayout(
            orientation="vertical",
            padding=(dp(9), dp(8), dp(9), dp(76)),
            spacing=dp(7)
        )

        title = Label(
            text="近期账单", font_name=APP_FONT, font_size=sp(20),
            bold=True, color=TEXT, size_hint_y=None, height=dp(38),
            halign="left", valign="middle"
        )
        root.add_widget(title)

        scroll = ScrollView(
            do_scroll_x=False, bar_width=dp(3),
            scroll_type=["bars", "content"]
        )
        list_box = BoxLayout(
            orientation="vertical", spacing=dp(8),
            size_hint_y=None, padding=(0, 0, 0, dp(8))
        )
        list_box.bind(minimum_height=list_box.setter("height"))

        all_records = []
        records_by_date = self.data.get("records", {})
        if isinstance(records_by_date, dict):
            for date_key, items in records_by_date.items():
                if not isinstance(items, list):
                    continue
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    copied = dict(item)
                    copied["_date"] = str(date_key)
                    all_records.append(copied)

        all_records.sort(
            key=lambda item: (str(item.get("_date", "")), str(item.get("time", ""))),
            reverse=True
        )

        if not all_records:
            empty_card = Card(
                orientation="vertical", size_hint_y=None,
                height=dp(110), padding=dp(15)
            )
            empty_card.add_widget(Label(
                text="还没有账单记录", font_name=APP_FONT,
                font_size=sp(14), color=SUBTEXT,
                halign="center", valign="middle"
            ))
            list_box.add_widget(empty_card)
        else:
            recent_count = min(2, len(all_records))
            recent_card = Card(
                orientation="vertical", spacing=dp(7),
                size_hint_y=None,
                height=dp(20) + dp(30) + recent_count * dp(53) +
                       max(0, recent_count - 1) * dp(7)
            )
            recent_card.add_widget(Label(
                text=f"最近{recent_count}笔账单", font_name=APP_FONT,
                font_size=sp(15), bold=True, color=TEXT,
                size_hint_y=None, height=dp(30),
                halign="left", valign="middle"
            ))
            for item in all_records[:2]:
                recent_card.add_widget(self.create_recent_record_row(item))
            list_box.add_widget(recent_card)

            years = set()
            for item in all_records:
                date_value = str(item.get("_date", ""))
                try:
                    years.add(int(date_value[:4]))
                except (TypeError, ValueError):
                    continue

            years_title = Label(
                text="按年份查看", font_name=APP_FONT,
                font_size=sp(15), bold=True, color=TEXT,
                size_hint_y=None, height=dp(32),
                halign="left", valign="middle"
            )
            list_box.add_widget(years_title)

            # 年份按钮和账单内容放入 list_box
            for year in sorted(years, reverse=True):
                year_header, year_body = self.create_year_section(year)
                list_box.add_widget(year_header)
                list_box.add_widget(year_body)

        scroll.add_widget(list_box)
        root.add_widget(scroll)
        self.content.add_widget(root)

        def refresh(*_args):
            try:
                list_box.do_layout()
                list_box.height = list_box.minimum_height
                scroll._trigger_layout()
                scroll.do_layout()
            except Exception:
                pass

        Clock.schedule_once(refresh, 0)
        Clock.schedule_once(refresh, 0.15)
        Clock.schedule_once(refresh, 0.4)

    def create_recent_record_row(self, item):

        date_key = str(item.get("_date", ""))
        parts = date_key.split("-")
        if len(parts) >= 3:
            try:
                date_text = f"{int(parts[1]):02d}-{int(parts[2]):02d}"
            except ValueError:
                date_text = date_key
        else:
            date_text = date_key

        kind = item.get("type", "expense")
        amount = safe_float(item.get("amount", 0))
        platform = str(item.get("platform", "未设置"))
        remark = str(item.get("remark", "") or "")
        time_text = str(item.get("time", "") or "")

        if kind == "income":
            amount_text = "+" + money(amount)
            amount_color = GREEN
            kind_text = "收入"
        else:
            amount_text = "-" + money(amount)
            amount_color = RED
            kind_text = "支出"

        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(53),
            spacing=dp(5),
            padding=(dp(7), dp(4))
        )

        with row.canvas.before:
            Color(*WHITE)
            rect = RoundedRectangle(
                pos=row.pos,
                size=row.size,
                radius=[dp(9)]
            )
            Color(*BORDER)
            line = Line(
                rounded_rectangle=(
                    row.x, row.y, row.width, row.height, dp(9)
                ),
                width=1
            )

        row.bind(
            pos=lambda obj, value, r=rect, l=line:
                self._recent_row_bg(obj, r, l),
            size=lambda obj, value, r=rect, l=line:
                self._recent_row_bg(obj, r, l)
        )

        left = BoxLayout(
            orientation="vertical",
            spacing=dp(1)
        )

        top_text = f"{date_text}  {kind_text} · {platform}"
        bottom_text = remark
        if time_text:
            bottom_text = f"{bottom_text}  {time_text}".strip()

        left.add_widget(
            Label(
                text=top_text,
                font_name=APP_FONT,
                font_size=sp(11),
                color=TEXT,
                halign="left",
                valign="middle",
                shorten=True,
                shorten_from="right"
            )
        )
        left.add_widget(
            Label(
                text=bottom_text,
                font_name=APP_FONT,
                font_size=sp(9),
                color=SUBTEXT,
                halign="left",
                valign="middle",
                shorten=True,
                shorten_from="right"
            )
        )

        amount_label = Label(
            text=amount_text,
            font_name=APP_FONT,
            font_size=sp(12),
            bold=True,
            color=amount_color,
            size_hint_x=None,
            width=dp(82),
            halign="right",
            valign="middle"
        )

        row.add_widget(left)
        row.add_widget(amount_label)
        return row

    # =====================================================
    # 近期年份板块
    # =====================================================

    def create_year_section(self, year):
        """返回固定高度的年份按钮和独立账单内容容器"""
        header = RoundButton(
            text=f"{year}年   ▼", font_name=APP_FONT,
            font_size=sp(15), bold=True, color=TEXT,
            bg_color=WHITE, border_color=BORDER, radius=10,
            size_hint_y=None, height=dp(46)
        )

        body = BoxLayout(
            orientation="vertical", spacing=dp(5),
            size_hint_y=None, height=0, opacity=0
        )

        all_records = []
        records_data = self.data.get("records", {})
        if isinstance(records_data, dict):
            for date_key, records in records_data.items():
                if not str(date_key).startswith(str(year)) or not isinstance(records, list):
                    continue
                for item in records:
                    if isinstance(item, dict):
                        copied = dict(item)
                        copied["_date"] = str(date_key)
                        all_records.append(copied)

        all_records.sort(
            key=lambda item: (str(item.get("_date", "")), str(item.get("time", ""))),
            reverse=True
        )

        for item in all_records:
            date_key = str(item.get("_date", ""))
            parts = date_key.split("-")
            try:
                date_text = f"{int(parts[1])}月{int(parts[2])}日" if len(parts) >= 3 else date_key
            except (ValueError, IndexError):
                date_text = date_key

            kind = item.get("type", "expense")
            amount = safe_float(item.get("amount", 0))
            platform = str(item.get("platform", "未设置"))
            remark = str(item.get("remark", "") or "")
            time_text = str(item.get("time", "") or "")
            if kind == "income":
                kind_text, amount_text, amount_color = "收入", "+" + money(amount), GREEN
            else:
                kind_text, amount_text, amount_color = "支出", "-" + money(amount), RED

            row = BoxLayout(
                orientation="horizontal", size_hint_y=None,
                height=dp(55), spacing=dp(5), padding=(dp(9), dp(5))
            )
            with row.canvas.before:
                Color(*WHITE)
                rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(9)])
                Color(*BORDER)
                line = Line(rounded_rectangle=(row.x, row.y, row.width, row.height, dp(9)), width=1)
            row.bind(
                pos=lambda obj, value, r=rect, l=line: self._recent_row_bg(obj, r, l),
                size=lambda obj, value, r=rect, l=line: self._recent_row_bg(obj, r, l)
            )

            left = BoxLayout(orientation="vertical", spacing=dp(1))
            top_text = f"{date_text}  {kind_text} · {platform}"
            bottom_text = f"{remark}  {time_text}".strip() if remark else time_text
            left.add_widget(Label(
                text=top_text, font_name=APP_FONT, font_size=sp(11.5),
                color=TEXT, halign="left", valign="middle",
                shorten=True, shorten_from="right"
            ))
            left.add_widget(Label(
                text=bottom_text, font_name=APP_FONT, font_size=sp(9),
                color=SUBTEXT, halign="left", valign="middle",
                shorten=True, shorten_from="right"
            ))
            amount_label = Label(
                text=amount_text, font_name=APP_FONT, font_size=sp(12),
                bold=True, color=amount_color, size_hint_x=None,
                width=dp(112), halign="right", valign="middle",
                shorten=True, shorten_from="left"
            )
            row.add_widget(left)
            row.add_widget(amount_label)
            body.add_widget(row)

        if not all_records:
            body.add_widget(Label(
                text="没有账单", font_name=APP_FONT, font_size=sp(12),
                color=SUBTEXT, size_hint_y=None, height=dp(40)
            ))

        expanded = {"value": False}

        def toggle(*_args):
            expanded["value"] = not expanded["value"]
            if expanded["value"]:
                body.opacity = 1
                body.height = body.minimum_height
                header.text = f"{year}年   ▲"
            else:
                body.opacity = 0
                body.height = 0
                header.text = f"{year}年   ▼"

            # 刷新 ScrollView 内容的 minimum_height，确保安卓首帧和展开后都更新
            Clock.schedule_once(lambda *_: self._refresh_recent_list_layout(body), 0)
            Clock.schedule_once(lambda *_: self._refresh_recent_list_layout(body), 0.12)

        header.bind(on_release=toggle)
        return header, body

    def _refresh_recent_list_layout(self, widget=None):
        try:
            node = widget
            while node is not None and not isinstance(node, ScrollView):
                node = node.parent
            if node is not None:
                content = node.children[0] if node.children else None
                if content is not None:
                    content.height = content.minimum_height
                    content.do_layout()
                node._trigger_layout()
                node.do_layout()
        except Exception:
            pass

    def _recent_row_bg(
        self,
        widget,
        rect,
        line
    ):

        rect.pos = widget.pos
        rect.size = widget.size

        line.rounded_rectangle = (
            widget.x,
            widget.y,
            widget.width,
            widget.height,
            dp(9)
        )

    # =====================================================
    # 我的
    # =====================================================

    def build_mine(self):

        root = BoxLayout(
            orientation="vertical",
            padding=(
                dp(10),
                dp(10),
                dp(10),
                dp(76)
            ),
            spacing=dp(9)
        )

        title = Label(
            text="我的",
            font_name=APP_FONT,
            font_size=sp(20),
            bold=True,
            color=TEXT,
            size_hint_y=None,
            height=dp(40),
            halign="left",
            valign="middle"
        )

        root.add_widget(
            title
        )

        # -------------------------------------------------
        # 余额
        # -------------------------------------------------

        balance_card = Card(
            orientation="vertical",
            size_hint_y=None,
            height=dp(105),
            padding=dp(15),
            spacing=dp(2)
        )

        balance_card.add_widget(
            Label(
                text="当前余额",
                font_name=APP_FONT,
                font_size=sp(12),
                color=SUBTEXT,
                halign="left",
                valign="middle"
            )
        )

        balance_card.add_widget(
            Label(
                text=money(
                    self.total_balance()
                ),
                font_name=APP_FONT,
                font_size=sp(27),
                bold=True,
                color=BLUE,
                halign="left",
                valign="middle"
            )
        )

        root.add_widget(
            balance_card
        )

        # -------------------------------------------------
        # 初始余额
        # -------------------------------------------------

        initial_btn = RoundButton(
            text=(
                "初始余额    " +
                money(
                    self.data.get(
                        "initial_balance",
                        0
                    )
                )
            ),
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=11,
            size_hint_y=None,
            height=dp(48)
        )

        initial_btn.bind(
            on_release=lambda x:
            self.open_initial_balance()
        )

        root.add_widget(
            initial_btn
        )

        # -------------------------------------------------
        # 平台
        # -------------------------------------------------

        platform_btn = RoundButton(
            text="渠道 / 平台管理",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=11,
            size_hint_y=None,
            height=dp(48)
        )

        platform_btn.bind(
            on_release=lambda x:
            self.open_platform_manager()
        )

        root.add_widget(
            platform_btn
        )

        # -------------------------------------------------
        # 清空
        # -------------------------------------------------

        clear_btn = RoundButton(
            text="清空全部账本数据",
            font_name=APP_FONT,
            font_size=sp(14),
            color=RED,
            bg_color=RED_LIGHT,
            radius=11,
            size_hint_y=None,
            height=dp(48)
        )

        clear_btn.bind(
            on_release=lambda x:
            self.confirm_clear()
        )

        root.add_widget(
            clear_btn
        )

        root.add_widget(
            Widget()
        )

        self.content.add_widget(
            root
        )

    # =====================================================
    # 初始余额弹窗
    # =====================================================

    def open_initial_balance(self):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text="设置初始余额",
                font_name=APP_FONT,
                font_size=sp(17),
                bold=True,
                color=TEXT,
                size_hint_y=None,
                height=dp(32)
            )
        )

        input_box = StyledInput(
            text=money(
                self.data.get(
                    "initial_balance",
                    0
                )
            ),
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44)
        )

        panel.add_widget(
            input_box
        )

        panel.add_widget(
            Label(
                text="金额最多保留两位小数",
                font_name=APP_FONT,
                font_size=sp(10),
                color=SUBTEXT,
                size_hint_y=None,
                height=dp(20)
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel = RoundButton(
            text="取消",
            font_name=APP_FONT,
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        save = RoundButton(
            text="保存",
            font_name=APP_FONT,
            color=WHITE,
            bg_color=BLUE,
            radius=9
        )

        buttons.add_widget(cancel)
        buttons.add_widget(save)

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.84, None),
            height=dp(245),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def save_value(*args):

            self.data[
                "initial_balance"
            ] = round(
                safe_float(
                    input_box.text
                ),
                2
            )

            self.save_data()

            popup.dismiss()

            self.switch_page(
                "mine"
            )

        save.bind(
            on_release=save_value
        )

        popup.open()

    # =====================================================
    # 平台管理
    # =====================================================

    def open_platform_manager(self):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text="渠道 / 平台管理",
                font_name=APP_FONT,
                font_size=sp(17),
                bold=True,
                color=TEXT,
                size_hint_y=None,
                height=dp(32)
            )
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        list_box = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint_y=None
        )

        list_box.bind(
            minimum_height=
            list_box.setter("height")
        )

        platforms = self.data.get(
            "platform_balances",
            {}
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.90, 0.80),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        for platform in platforms:

            row = BoxLayout(
                spacing=dp(5),
                size_hint_y=None,
                height=dp(45)
            )

            name_btn = RoundButton(
                text=platform,
                font_name=APP_FONT,
                font_size=sp(13),
                color=TEXT,
                bg_color=WHITE,
                border_color=BORDER,
                radius=8
            )

            amount_btn = RoundButton(
                text=money(
                    self.platform_balance(
                        platform
                    )
                ),
                font_name=APP_FONT,
                font_size=sp(13),
                color=BLUE,
                bg_color=BLUE_LIGHT,
                radius=8,
                size_hint_x=None,
                width=dp(95)
            )

            delete_btn = RoundButton(
                text="删除",
                font_name=APP_FONT,
                font_size=sp(12),
                color=RED,
                bg_color=RED_LIGHT,
                radius=8,
                size_hint_x=None,
                width=dp(55)
            )

            name_btn.bind(
                on_release=lambda x,
                p=platform:
                self.open_platform_amount(
                    p
                )
            )

            amount_btn.bind(
                on_release=lambda x,
                p=platform:
                self.open_platform_amount(
                    p
                )
            )

            delete_btn.bind(
                on_release=lambda x,
                p=platform:
                self.delete_platform(
                    p,
                    popup
                )
            )

            row.add_widget(
                name_btn
            )

            row.add_widget(
                amount_btn
            )

            row.add_widget(
                delete_btn
            )

            list_box.add_widget(
                row
            )

        scroll.add_widget(
            list_box
        )

        panel.add_widget(
            scroll
        )

        add_btn = RoundButton(
            text="＋ 添加平台",
            font_name=APP_FONT,
            font_size=sp(14),
            color=BLUE,
            bg_color=BLUE_LIGHT,
            radius=9,
            size_hint_y=None,
            height=dp(42)
        )

        panel.add_widget(
            add_btn
        )

        close_btn = RoundButton(
            text="关闭",
            font_name=APP_FONT,
            font_size=sp(14),
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9,
            size_hint_y=None,
            height=dp(42)
        )

        panel.add_widget(
            close_btn
        )

        close_btn.bind(
            on_release=popup.dismiss
        )

        add_btn.bind(
            on_release=lambda x:
            self.open_add_platform(
                popup
            )
        )

        popup.open()

    # =====================================================
    # 平台金额
    # =====================================================

    def open_platform_amount(
        self,
        platform
    ):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text=f"{platform} 初始金额",
                font_name=APP_FONT,
                font_size=sp(17),
                bold=True,
                color=TEXT,
                size_hint_y=None,
                height=dp(32)
            )
        )

        current = safe_float(
            self.data.get(
                "platform_balances",
                {}
            ).get(
                platform,
                0
            )
        )

        amount = StyledInput(
            text=money(current),
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44)
        )

        panel.add_widget(
            amount
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel = RoundButton(
            text="取消",
            font_name=APP_FONT,
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        save = RoundButton(
            text="保存",
            font_name=APP_FONT,
            color=WHITE,
            bg_color=BLUE,
            radius=9
        )

        buttons.add_widget(cancel)
        buttons.add_widget(save)

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.84, None),
            height=dp(225),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def save_amount(*args):

            self.data.setdefault(
                "platform_balances",
                {}
            )[platform] = round(
                safe_float(
                    amount.text
                ),
                2
            )

            self.save_data()

            popup.dismiss()

        save.bind(
            on_release=save_amount
        )

        popup.open()

    # =====================================================
    # 添加平台
    # =====================================================

    def open_add_platform(
        self,
        parent_popup=None
    ):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text="添加平台",
                font_name=APP_FONT,
                font_size=sp(17),
                bold=True,
                color=TEXT,
                size_hint_y=None,
                height=dp(32)
            )
        )

        name = StyledInput(
            hint_text="平台名称",
            multiline=False,
            size_hint_y=None,
            height=dp(44)
        )

        amount = StyledInput(
            text="0.00",
            hint_text="初始金额",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44)
        )

        panel.add_widget(name)
        panel.add_widget(amount)

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel = RoundButton(
            text="取消",
            font_name=APP_FONT,
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        save = RoundButton(
            text="保存",
            font_name=APP_FONT,
            color=WHITE,
            bg_color=BLUE,
            radius=9
        )

        buttons.add_widget(cancel)
        buttons.add_widget(save)

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.86, None),
            height=dp(285),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def save_platform(*args):

            platform = name.text.strip()

            if not platform:

                self.show_message(
                    "请输入平台名称"
                )

                return

            platforms = self.data.setdefault(
                "platform_balances",
                {}
            )

            if platform in platforms:

                self.show_message(
                    "这个平台已经存在"
                )

                return

            platforms[platform] = round(
                safe_float(
                    amount.text
                ),
                2
            )

            self.save_data()

            popup.dismiss()

            if parent_popup:

                parent_popup.dismiss()

            self.open_platform_manager()

        save.bind(
            on_release=save_platform
        )

        popup.open()

    # =====================================================
    # 删除平台
    # =====================================================

    def delete_platform(
        self,
        platform,
        parent_popup
    ):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text=(
                    f"确定删除「{platform}」吗？"
                ),
                font_name=APP_FONT,
                font_size=sp(14),
                color=TEXT,
                halign="center",
                valign="middle"
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel = RoundButton(
            text="取消",
            font_name=APP_FONT,
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        delete = RoundButton(
            text="删除",
            font_name=APP_FONT,
            color=WHITE,
            bg_color=RED,
            radius=9
        )

        buttons.add_widget(cancel)
        buttons.add_widget(delete)

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.84, None),
            height=dp(185),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def do_delete(*args):

            try:

                del self.data[
                    "platform_balances"
                ][platform]

            except Exception:
                pass

            self.save_data()

            popup.dismiss()
            parent_popup.dismiss()

            self.open_platform_manager()

        delete.bind(
            on_release=do_delete
        )

        popup.open()

    # =====================================================
    # 清空数据
    # =====================================================

    def confirm_clear(self):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text=(
                    "确定删除全部账单记录吗？\n"
                    "此操作无法恢复"
                ),
                font_name=APP_FONT,
                font_size=sp(14),
                color=TEXT,
                halign="center",
                valign="middle"
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        cancel = RoundButton(
            text="取消",
            font_name=APP_FONT,
            color=TEXT,
            bg_color=WHITE,
            border_color=BORDER,
            radius=9
        )

        delete = RoundButton(
            text="确定删除",
            font_name=APP_FONT,
            color=WHITE,
            bg_color=RED,
            radius=9
        )

        buttons.add_widget(cancel)
        buttons.add_widget(delete)

        panel.add_widget(
            buttons
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.86, None),
            height=dp(205),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0),
            auto_dismiss=False
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def clear_all(*args):

            self.data[
                "records"
            ] = {}

            self.save_data()

            popup.dismiss()

            self.switch_page(
                "account"
            )

        delete.bind(
            on_release=clear_all
        )

        popup.open()

    # =====================================================
    # 提示弹窗
    # =====================================================

    def show_message(
        self,
        message
    ):

        panel = PopupPanel()

        panel.add_widget(
            Label(
                text=message,
                font_name=APP_FONT,
                font_size=sp(14),
                color=TEXT,
                halign="center",
                valign="middle"
            )
        )

        button = RoundButton(
            text="确定",
            font_name=APP_FONT,
            font_size=sp(14),
            color=WHITE,
            bg_color=BLUE,
            radius=9,
            size_hint_y=None,
            height=dp(42)
        )

        panel.add_widget(
            button
        )

        popup = Popup(
            title="",
            content=panel,
            size_hint=(0.78, None),
            height=dp(170),
            separator_height=0,
            background="",
            background_color=(0, 0, 0, 0)
        )

        button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =====================================================
    # 屏幕
    # =====================================================

    def on_start(self):

        Clock.schedule_once(
            lambda dt:
            self._after_start(),
            0.2
        )

    def _after_start(self):

        self.update_bottom_size()
        self.update_fab()

    def update_bottom_size(self):

        if not self.bottom_bar:
            return

        width = min(
            Window.width - dp(14),
            dp(520)
        )

        if width < dp(250):

            width = max(
                dp(200),
                Window.width - dp(10)
            )

        self.bottom_bar.size = (
            width,
            dp(62)
        )

    def on_window_size(
        self,
        *args
    ):

        self.update_bottom_size()

        self.update_fab()

        if (
            self.current_page ==
            "account"
            and self.calendar_grid
        ):

            self.calendar_grid.height = (
                self.get_calendar_height()
            )

    def on_request_close(
        self,
        *args
    ):

        try:

            self.save_data()

        except Exception:

            pass

        return False


# =========================================================
# 启动
# =========================================================

if __name__ == "__main__":

    AccountingApp().run()