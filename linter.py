from SublimeLinter.lint import Linter, util


def utf16_offset_to_index(text, offset):
    """Return the index in `text` of the character at UTF-16 code unit `offset`."""
    units = 0
    for index, char in enumerate(text):
        if units >= offset:
            return index
        units += 2 if ord(char) > 0xFFFF else 1

    return len(text)


class Javac(Linter):
    regex = (
        r'^(?P<filename>.+?):(?P<line>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning)): '
        r'(?:\[.+?\] )?(?P<message>[^\r\n]+)\r?\n'
        r'[^\r\n]+\r?\n'
        r'(?P<col>[^\^]*)\^'
    )
    multiline = True
    tempfile_suffix = '-'
    error_stream = util.STREAM_STDERR
    defaults = {
        'lint': '',
        '-classpath::': [],
        'selector': 'source.java'
    }

    def reposition_match(self, line, col, m, vv):
        if col is not None:
            # javac pads the caret line in UTF-16 code units, a character
            # outside the Basic Multilingual Plane, e.g. an emoji, counts as
            # two. Sublime counts characters.
            col = utf16_offset_to_index(vv.select_line(line), col)

        return super().reposition_match(line, col, m, vv)

    def cmd(self):
        """
        Return the command line to execute.

        We override this because we have to munge the -Xlint argument
        based on the 'lint' setting.

        """

        xlint = '-Xlint'
        settings = self.get_view_settings()
        options = settings.get('lint')

        if options:
            xlint += ':' + options

        return ('javac', xlint, '-encoding', 'UTF8', '${args}')
