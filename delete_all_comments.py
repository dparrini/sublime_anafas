import re
import sublime
import sublime_plugin

class DeleteAllCommentsCommand(sublime_plugin.TextCommand):
    DEBUG_MESSAGES = False
    COMMENT_CHARACTER = "("

    def run(self, edit):
        chars = self.view.size()
        allfile = sublime.Region(0, chars)

        iline = 0
        total_lines, _ = self.view.rowcol(allfile.end())
        if self.DEBUG_MESSAGES:
            print("File with", total_lines, "lines.")
        
        while iline <= total_lines:
            at_point = self.view.text_point(iline, 0)
            at_region = self.view.full_line(at_point)
            content = self.view.substr(at_region)
            if content[0] == self.COMMENT_CHARACTER:
                if self.DEBUG_MESSAGES:
                    print("Found a comment!", content)
                self.view.erase(edit, at_region)
                total_lines = total_lines - 1
            else:
                iline = iline + 1

