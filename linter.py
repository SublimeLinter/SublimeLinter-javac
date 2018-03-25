from SublimeLinter.lint import Linter, util


class Javac(Linter):
    regex = (
        r'^(?P<file>.+?):(?P<line>\d+): '
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
        'selector': 'source.java'
    }

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

        return (self.executable_path, xlint, '-encoding', 'UTF8', '*')

    def split_match(self, match):
        """
        Return the components of the match.

        We override this because javac lints all referenced files,
        and we only want errors from the linted file.

        """

        if match:
            if match.group('file') != self.filename:
                return None

        return super().split_match(match)
