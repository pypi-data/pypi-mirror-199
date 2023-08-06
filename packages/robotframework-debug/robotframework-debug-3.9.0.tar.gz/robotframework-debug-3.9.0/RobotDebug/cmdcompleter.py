import re

from prompt_toolkit.completion import Completer, Completion

from .robotkeyword import normalize_kw, parse_keyword
from .styles import _get_style_completions


class CmdCompleter(Completer):
    """Completer for debug shell."""

    def __init__(self, commands, cmd_repl=None):
        self.names = []
        self.displays = {}
        self.display_metas = {}
        for name, display, display_meta in commands:
            self.names.append(name)
            self.displays[name] = display
            self.display_metas[name] = display_meta
        self.cmd_repl = cmd_repl

    def _get_command_completions(self, text):
        content = text.strip().split("  ")[-1].lower().strip()
        suffix_len = len(text) - len(text.rstrip())
        return (
            Completion(
                f"{name}{' ' * suffix_len}",
                -len(content),
                display=self.displays.get(name, ""),
                display_meta=self.display_metas.get(name, ""),
            )
            for name in self.names
            if (
                (
                    ("." not in name and "." not in text)  # root level
                    or ("." in name and "." in text)
                )  # library level
                and normalize_kw(name).startswith(normalize_kw(content))
            )
        )

    def _get_resource_completions(self, text):
        return (
            Completion(
                name,
                -len(text.lstrip()),
                display=name,
                display_meta="",
            )
            for name in [
                "*** Settings ***",
                "*** Variables ***",
                "*** Keywords ***",
            ]
            if (name.lower().strip().startswith(text.strip()))
        )

    def get_completions(self, document, complete_event):
        """Compute suggestions."""
        # RobotFrameworkLocalLexer().parse_doc(document)
        text = document.current_line_before_cursor
        variables, keyword, args = parse_keyword(text.strip())
        if "FOR".startswith(text):
            yield from [
                Completion(
                    "FOR    ${var}    IN    @{list}\n    Log    ${var}\nEND",
                    -len(text),
                    display="FOR IN",
                    display_meta="For-Loop over all items in a list",
                ),
                Completion(
                    "FOR    ${var}    IN RANGE    5\n    Log    ${var}\nEND",
                    -len(text),
                    display="FOR IN RANGE",
                    display_meta="For-Loop over a range of numbers",
                ),
                Completion(
                    "FOR    ${index}    ${var}    IN ENUMERATE"
                    "    @{list}\n    Log    ${index} - ${var}n\nEND",
                    -len(text),
                    display="FOR IN ENUMERATE",
                    display_meta="For-Loop over all items in a list with index",
                ),
            ]
        elif "IF".startswith(text):
            yield from [
                Completion(
                    "IF    <py-eval>    Log    None",
                    -len(text),
                    display="IF (one line)",
                    display_meta="If-Statement as one line",
                ),
                Completion(
                    "IF    <py-eval>\n    Log    if-branche\nEND",
                    -len(text),
                    display="IF (multi line)",
                    display_meta="If-Statement as multi line",
                ),
            ]
        elif re.fullmatch(r"style {2,}.*", text):
            yield from _get_style_completions(text.lower())
        elif text.startswith("*"):
            yield from self._get_resource_completions(text.lower())
        elif keyword:
            if not args:
                yield from self._get_command_completions(text.lower())

