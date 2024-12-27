import json
import random


class Edition:
    def __init__(self, *, edition_nr: str, links: list):
        self._edition_nr = int(edition_nr)
        self._links = links

    def render(self, *, max_edition_nr_length: int, max_links: int, bar_symbol_code: int = 9608, color: int = 7) -> str:
        format_code = f"0{max_edition_nr_length}d"
        filled_bars = int(len(self._links) / max_links * 10)
        bar = f"\033[3{color}m{chr(bar_symbol_code) * filled_bars}\033[0m" + " " * (10 - filled_bars)
        return f"{self._edition_nr:{format_code}}: {bar} ({len(self._links)})"


class ASCIIBarchart:
    def __init__(self, line_length: int = 3):
        self._lines = [[]]
        self._line_length = line_length
        self._max_links = 0
        self._max_edition_nr_length = 0

    def load_newsletter_archive(self, *, file_path: str = None) -> None:
        with open(file_path) as infile:
            editions = json.load(infile)
        for edition_nr in editions:
            if edition_nr != "total":
                self._add_edition(edition_nr=edition_nr, links=editions[edition_nr]["links"])

    def _add_edition(self, *, edition_nr: str = None, links: list = None) -> None:
        if len(self._lines[-1]) == self._line_length:
            self._lines.append([])
        self._max_edition_nr_length = max(len(edition_nr), self._max_edition_nr_length)
        self._max_links = max(len(links), self._max_links)
        edition = Edition(edition_nr=edition_nr, links=links)
        self._lines[-1].append(edition)

    @staticmethod
    def _get_bar_color(fun_mode: bool = False):
        if fun_mode:
            return random.randint(0, 7)
        else:
            return 7

    def render(self, bar_symbol_code: int = 9608, separator: str = " | ", fun_mode: bool = False) -> None:
        print("DevDigest 2024 Links content" + (" (the fun way!)" if fun_mode else ""))
        for line in self._lines:
            line_repr = separator.join([edition.render(max_edition_nr_length=self._max_edition_nr_length,
                                                       max_links=self._max_links,
                                                       bar_symbol_code=bar_symbol_code,
                                                       color=self._get_bar_color(fun_mode))
                                        for edition in line])
            print(line_repr)
        print()


ascii_barchart = ASCIIBarchart()
ascii_barchart.load_newsletter_archive(file_path="newsletterarchive2024.json")
# Basic usage
ascii_barchart.render()
# Extended usage
ascii_barchart.render(bar_symbol_code=9612, separator=" § ", fun_mode=True)
