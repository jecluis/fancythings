#!/usr/bin/python3

from blessed import Terminal
from .composer import Widget


class Dialog(Widget):

    def __init__(self, term: Terminal, show_by_default=False):
        super().__init__()
        self.term = term
        self.content = []
        self.show = show_by_default

    def set_content(self, lst):
        self.content = lst

    def toggle_show(self):
        self.show = not self.show
    
    def render(self):
        if not self.show:
            return

        content = []
        for c in self.content:
            content.extend(self.term.wrap(c))
        
        # attempt to horizontally center dialog
        center_x = int(self.term.width / 2)
        longest_content = len(max(content, key=self.term.length))
        start_x = center_x - int(longest_content/2)

        assert start_x >= 0
        do_dividers = False
        divider_len = longest_content
        divider = self.term.ljust('', divider_len, '-')
        content.insert(0, divider)
        content.append(divider)

        """
        with open('debug.log', 'a') as f:
            j = {
                "longest_content": longest_content,
                "start_x": start_x,
                "center_x": center_x,
                "content": content
            }
            import json
            json.dump(j, f)
        """
        
        offset = 0
        for content_line in content:
            padded = self.term.ljust(content_line, longest_content)
            line = f"{self.term.gray20_on_sienna}" + padded
            print(
                self.term.move_xy(start_x, offset) +
                line,
                end='', flush=True
            )
            offset += 1



    
