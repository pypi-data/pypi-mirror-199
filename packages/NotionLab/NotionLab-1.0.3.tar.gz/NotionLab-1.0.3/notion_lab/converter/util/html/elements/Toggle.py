from typing import Dict

from ..html import *


class Toggle:
    b_ctx: Dict
    details: str

    def __init__(self, b_ctx: Dict, details: str):
        self.b_ctx = b_ctx
        self.details = details

    def export(self):
        r = ""
        r += "<details>"
        r += "<summary>"
        for child in self.b_ctx["rich_text"]:
            r += div(child)
        r += "</summary>"
        r += self.details
        r += "</details>"
        return r
