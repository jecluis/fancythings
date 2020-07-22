#!/usr/bin/python3

from contextlib import contextmanager
from blessed import Terminal
from threading import Lock
from typing import List


class StatusBuffer:

    BEHAVIOR_TOP = 1
    BEHAVIOR_BOTTOM = 2

    def __init__(self, term: Terminal):
        self.top_status = []
        self.bottom_status = []
        self.buffer = []
        self.buffer_behavior = StatusBuffer.BEHAVIOR_TOP
        self.lock = Lock()
        self.term = term

        self.draw_offset = 0

    
    def refresh(self):

        self.draw_offset = 0
        self.lock.acquire()

        print(self.term.clear)

        # refresh top to bottom
        self.draw_top_status()
        self.draw_buffer()
        self.draw_bottom_status()

        self.lock.release()


    def draw_top_status(self):

        for line in self.top_status:
            status_bar_line = self._get_status_bar(line)
            self._print(status_bar_line)

    def draw_buffer(self):

        # buffer needs to be aware of top and bottom status, so it can
        # limit the offsets it can work in and the lines to be shown
        top_offset = len(self.top_status)
        bottom_offset = self.term.height - len(self.bottom_status)

        # limit message number for our draw box
        # older messages (front of list) are lost
        buffer_size = bottom_offset - top_offset
        buffer_values = self.buffer
        if len(self.buffer) > buffer_size:
            buffer_values = self.buffer[buffer_size:]

        buffer_print_start_offset = top_offset
        if self.buffer_behavior == StatusBuffer.BEHAVIOR_BOTTOM:
            buffer_print_start_offset = bottom_offset - len(self.buffer)

        # create print buffer
        lst = []
        bg = f"{self.term.on_grey38}"
        pos = 0
        for offset in range(top_offset, bottom_offset):
            line = bg
            if offset >= buffer_print_start_offset:
                if pos < len(self.buffer):
                    line += self.buffer[pos]
                    pos += 1
            self._print(line)
        pass

    def draw_bottom_status(self):
        for line in self.bottom_status:
            status_bar_line = self._get_status_bar(line)
            self._print(status_bar_line)
        pass

    def _get_status_bar(self, line):
        t = self.term
        msg = self.term.ljust(f"{t.on_black}{line}")
        return msg

    def _print(self, line):
        t = self.term
        if self.draw_offset >= self.term.height:
            return

        padded_msg = self.term.ljust(line)
        print(
            self.term.move_xy(0, self.draw_offset) +
            self.term.clear_eol +
            padded_msg +
            f"{self.term.normal}",
            end='', flush=True)
        self.draw_offset = self.draw_offset + 1 # move one line down


    def set_top_status(self, lines: List[str]):
        self.top_status = lines

    def set_bottom_status(self, lines: List[str]):
        self.bottom_status = lines

    def set_buffer(self, lines: List[str]):
        self.buffer = lines

    def set_buffer_behavior(self, behavior):
        self.buffer_behavior = behavior


@contextmanager
def Buffer(term):
    sb = StatusBuffer(term)
    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        yield sb
