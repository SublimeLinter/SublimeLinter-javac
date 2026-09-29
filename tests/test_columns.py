import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


LinterModule = importlib.import_module('SublimeLinter-javac.linter')
Linter = LinterModule.Javac


# Real output of `javac -Xlint -encoding UTF8 Main.java` (javac 25.0.3) for this source.
# javac pads the caret line in UTF-16 code units, so the emoji (U+1F600) before the error on
# line 6 counts as two. It keeps tabs of the source line in the caret line.
SOURCE = (
    'import java.util.*;\n'
    'public class Main {\n'
    '\tstatic String s = "é\U0001f600";\n'
    '\tpublic static void main(String[] a) {\n'
    '\t\tint x = "str";\n'
    '\t\tString t = "é\U0001f600" + undefinedVar;\n'
    '\t\tList l = new ArrayList(); l.add(1);\n'
    '\t}\n'
    '}\n'
)
OUTPUT = (
    'Main.java:5: error: incompatible types: String cannot be converted to int\n'
    '\t\tint x = "str";\n'
    '\t\t        ^\n'
    'Main.java:6: error: cannot find symbol\n'
    '\t\tString t = "é\U0001f600" + undefinedVar;\n'
    '\t\t                   ^\n'
    '  symbol:   variable undefinedVar\n'
    '  location: class Main\n'
    'Main.java:7: warning: [rawtypes] found raw type: List\n'
    '\t\tList l = new ArrayList(); l.add(1);\n'
    '\t\t^\n'
    '  missing type arguments for generic class List<E>\n'
)


class TestColumns(unittest.TestCase):
    def resolve(self, output):
        linter = Linter(sublime.View(0), {})
        vv = VirtualView(SOURCE)
        return [
            (m['line'], linter.reposition_match(m['line'], m['col'], m, vv)[1])
            for m in linter.find_errors(output)
        ]

    def expected(self):
        lines = SOURCE.split('\n')
        return [
            (4, lines[4].index('"str"')),
            (5, lines[5].index('undefinedVar')),   # after the emoji
            (6, lines[6].index('List')),
        ]

    def test_columns_after_an_emoji_are_characters(self):
        self.assertEqual(self.resolve(OUTPUT), self.expected())

    def test_windows_line_endings(self):
        self.assertEqual(self.resolve(OUTPUT.replace('\n', '\r\n')), self.expected())

    def test_offsets_before_any_emoji_are_unchanged(self):
        f = LinterModule.utf16_offset_to_index
        self.assertEqual(f('abc', 0), 0)
        self.assertEqual(f('abc', 2), 2)
        self.assertEqual(f('\téx', 2), 2)

    def test_emoji_counts_as_two_units(self):
        f = LinterModule.utf16_offset_to_index
        text = 'a\U0001f600b'
        self.assertEqual(f(text, 1), 1)  # the emoji itself
        self.assertEqual(f(text, 3), 2)  # `b`, after the two units of the emoji
        self.assertEqual(f(text, 4), 3)  # end of line

    def test_offset_past_the_end_is_the_end_of_the_line(self):
        f = LinterModule.utf16_offset_to_index
        self.assertEqual(f('ab', 5), 2)
        self.assertEqual(f('', 0), 0)
