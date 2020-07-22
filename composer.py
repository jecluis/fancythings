#!/usr/bin/python

import time
from contextlib import contextmanager
from abc import ABC, abstractmethod
from blessed import Terminal


class Widget(ABC):

    def __init__(self):
        self.triggers = {}

    @abstractmethod
    def render(self):
        pass

    def set_trigger(self, lst, callback):

        for ch in lst:
            assert isinstance(ch, str) and len(ch) == 1
            self.triggers[ch] = callback

    def handle_inkey(self, ch):
        if ch in self.triggers:
            callback = self.triggers[ch]
            callback(ch)
            return True

        return False


class Composer:

    def __init__(self):
        self.widgets = []

    def add_widget(self, widget):
        assert isinstance(widget, Widget)
        self.widgets.append(widget)
        pass

    def refresh(self):
        for w in self.widgets:
            w.render()

    def handle_inkey(self, ch):
        for w in self.widgets:
            if not hasattr(w, "handle_inkey"):
                continue
            if w.handle_inkey(ch):
                break


@contextmanager
def ComposerContext(term: Terminal):
    composer = Composer()
    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        yield composer