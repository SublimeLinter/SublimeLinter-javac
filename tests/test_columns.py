import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


Linter = importlib.import_module('SublimeLinter-javac.linter').Javac

# Captured javac 25.0.3 output. Caret prefixes preserve tabs and count UTF-16 units.
SOURCE = (
    'import java.util.*;\n'
    'public class Main {\n'
    '\tstatic String s = "é😀";\n'
    '\tpublic static void main(String[] a) {\n'
    '\t\tint x = "str";\n'
    '\t\tString t = "é😀" + undefinedVar;\n'
    '\t\tList l = new ArrayList(); l.add(1);\n'
    '\t}\n'
    '}\n'
)
OUTPUT = (
    'Main.java:5: error: incompatible types: String cannot be converted to int\n'
    '\t\tint x = "str";\n'
    '\t\t        ^\n'
    'Main.java:6: error: cannot find symbol\n'
    '\t\tString t = "é😀" + undefinedVar;\n'
    '\t\t                   ^\n'
    '  symbol:   variable undefinedVar\n'
    '  location: class Main\n'
    'Main.java:7: warning: [rawtypes] found raw type: List\n'
    '\t\tList l = new ArrayList(); l.add(1);\n'
    '\t\t^\n'
    '  missing type arguments for generic class List<E>\n'
)


class TestColumns(unittest.TestCase):
    def test_captured_ascii_and_unicode_diagnostics(self):
        self.assertDiagnostics(OUTPUT)

    def test_windows_diagnostic_line_endings(self):
        self.assertDiagnostics(OUTPUT.replace('\n', '\r\n'))

    def assertDiagnostics(self, output):
        linter = Linter(sublime.View(0), {})
        vv = VirtualView(SOURCE)
        matches = list(linter.find_errors(output))
        expected = [(4, '"'), (5, 'undefinedVar'), (6, 'List')]
        self.assertEqual(len(matches), len(expected))
        for match, (line, text) in zip(matches, expected):
            match['filename'] = None  # supplied source is the main buffer
            error = linter.process_match(match, vv)
            self.assertIsNotNone(error)
            col = SOURCE.splitlines()[line].index(text)
            begin = vv.full_line(line)[0] + col
            self.assertEqual({k: error[k] for k in ('line', 'start', 'region', 'offending_text')}, {
                'line': line, 'start': col, 'region': sublime.Region(begin, begin + len(text)),
                'offending_text': text,
            })
