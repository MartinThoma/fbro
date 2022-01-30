# Core Library modules
import curses
import logging
from curses import panel
from typing import Any, List, Tuple

# First party modules
from fbro import aws

logger = logging.getLogger(__name__)

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
            self.position = len(self.items) - 1
        elif self.position >= len(self.items):
            self.position = 0

    def display(self):
        self.panel.top()
        self.panel.show()

        page_length = curses.LINES - 3

        while True:
            self.window.clear()
            self.window.refresh()
            curses.doupdate()
            self.window.addstr(1, 1, self.title, curses.A_NORMAL)

            start = 0
            while start + page_length <= self.position:
                start += page_length
            end = start + page_length

            for index, item in enumerate(self.items[start:end], start=start):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = f"- {item[0]}"
                self.window.addstr(2 + index - start, 1, msg, mode)
            if len(self.items) > start + page_length:
                self.window.addstr(curses.LINES - 1, 1, "...", curses.A_NORMAL)

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
        keys = list(aws.list_files(self.bucket, prefix=self.prefix))
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
    try:
        # Test if there is a working AWS connection
        aws.get_bucket_names()
    except Exception as e:
        print(f"{type(e)}: {e}")
        print("AWS connection is not working")
        return ""
    curses.wrapper(AwsApp)
