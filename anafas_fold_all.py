import re
import sublime
import sublime_plugin



# card names
CARD_TIPO = "TIPO"
CARD_TITU = "TITU"
CARD_CMNT = "CMNT"
CARD_BASE = "BASE"
CARD_DMUT = "DMUT"
CARD_DMOV = "DMOV"
CARD_DSHL = "DSHL"
CARD_DEOL = "DEOL"
CARD_DARE = "DARE"
CARD_DREB = "DREB"
CARD_DBAR = "DBAR"
CARD_DCIR = "DCIR"
CARD_FIM  = "FIM"


class AnafasFoldAllCommand(sublime_plugin.TextCommand):
    DEBUG_MESSAGES = True
    COMMENT_CHARACTER = "("

    foldable_start = [
        "(?i)^(" + CARD_DMUT + "| 39)\\s*$",
        "(?i)^(" + CARD_DMOV + "| 36)\\s*$",
        "(?i)^(" + CARD_DSHL + "| 35)\\s*$",
        "(?i)^(" + CARD_DEOL + ")\\s*$",
        "(?i)^(" + CARD_DARE + ")\\s*$",
        "(?i)^(" + CARD_DREB + ")\\s*$",
        "(?i)^(" + CARD_DBAR + "| 38)\\s*$",
        "(?i)^(" + CARD_DCIR + "| 37)\\s*$"
    ]

    foldable_end = "(?i)^(99999|F)\\s*$"

    def run(self, edit):
        chars = self.view.size()
        allfile = sublime.Region(0, chars)

        iline = 0
        total_lines, _ = self.view.rowcol(allfile.end())

        # which regions to fold
        regions = []

        # regular expressions for start and end of foldable region
        start_re = list(map(lambda x : re.compile(x), self.foldable_start))
        end_re = re.compile(self.foldable_end)

        start_char = 0
        end_char = 0
        inside_card = False
        if self.DEBUG_MESSAGES:
            print("Running fold all:", total_lines, "lines")
        while iline <= total_lines:

            at_line = self.view.line(self.view.text_point(iline, 0))
            contents = self.view.substr(at_line)

            if not inside_card:
                for icard_re in start_re:
                    if icard_re.match(contents) is not None:
                        if self.DEBUG_MESSAGES:
                            print("Found a card:", contents[0:3])
                        x = at_line.end()
                        start_char = sublime.Region(x, x)
                        inside_card = True
            else:
                if end_re.match(contents) is not None:
                    x = at_line.end()
                    end_char = sublime.Region(x, x)
                    inside_card = False
                    regions.append(start_char.cover(end_char))

                    if self.DEBUG_MESSAGES:
                        print("Found its ending:", contents)

            iline = iline + 1

        if self.DEBUG_MESSAGES:
            print("Got", len(regions), "regions to fold")

        self.view.fold(regions)






