from SublimeLinter.lint import Linter, util


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
