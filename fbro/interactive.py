#!/usr/bin/python

# Core Library modules
import curses
from curses import panel
from typing import Any, List, Tuple

# First party modules
from fbro import aws

WindowType = Any  # curses.window does not work


class Menu:
    def __init__(
        self, items: List[Tuple[str, Any]], stdscreen: WindowType, title: str = ""
    ):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items: List[Tuple[str, Any]] = items
        self.title = title

    def navigate(self, n: int) -> None:
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            self.window.addstr(1, 1, self.title, curses.A_NORMAL)
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = f"- {item[0]}"
                self.window.addstr(2 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n"), curses.KEY_RIGHT]:
                self.items[self.position][1]()
            elif key == curses.KEY_UP:
                self.navigate(-1)
            elif key == curses.KEY_DOWN:
                self.navigate(1)
            elif key == curses.KEY_LEFT:
                break

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class MenuLoader:
    def __init__(self, screen: WindowType, bucket: str, prefix: str = ""):
        self.bucket = bucket
        self.screen = screen
        self.prefix = prefix

    def display(self):
        keys = [key for key in aws.list_files(self.bucket, prefix=self.prefix)]
        items = [
            (key, MenuLoader(self.screen, self.bucket, prefix=f"{key}").display)
            for key in keys
        ]
        menu = Menu(items, self.screen, title=f"s3://{self.bucket}/{self.prefix}")
        return menu.display()


class AwsApp:
    def __init__(self, stdscreen: WindowType):
        self.screen = stdscreen
        curses.curs_set(0)

        main_menu_items = [
            (f"s3://{bucketname}", MenuLoader(self.screen, bucketname).display)
            for bucketname in aws.get_bucket_names()
        ]
        main_menu = Menu(main_menu_items, self.screen, title="Buckets on s3")
        main_menu.display()


def main():
    curses.wrapper(AwsApp)
