import argparse
import os
import sys


class BaseCommand:
    _help = ''

    def create_parser(self, prog_name, sub_cmd):
        parser = argparse.ArgumentParser(
            prog='{} {}'.format(os.path.basename(prog_name), sub_cmd),
            description=self._help or None,
        )

        self.add_args(parser)
        return parser

    def add_args(self, parser):
        pass

    def run(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        options_cmd = vars(options)
        args = options_cmd.pop('args', ())
        self.handle(*args, **options_cmd)

    def handle(self, *args, **kwargs):
        raise NotImplementedError('Subclasses of BaseCommand must provide a handle() method')


class Newfile(BaseCommand):
    def add_args(self, parser):
        parser.add_argument('outfile')
        parser.add_argument('-at', '--path')

    def handle(self, *args, **kwargs):
        outfile = kwargs.pop('outfile')
        pkg = kwargs.pop('path').replace('.', '\\')

        assert outfile is not None and pkg is not None, "Outfile or path not found"

        file_dir = os.path.join(sys.path[0], pkg)
        if not os.path.isdir(file_dir):
            raise '"{}" not found.'.format(file_dir)

        filepath = os.path.join(file_dir, outfile)
        if os.path.isfile(filepath):
            raise '"{}" exists ready.'.format(filepath)

        open(os.path.join(file_dir, outfile), 'w').close()


def execute_from_argv():
    try:
        sub_cmd = sys.argv[1]
    except IndexError:
        sub_cmd = 'help'

    cmd = globals()[sub_cmd.capitalize()]()
    cmd.run(sys.argv)


if __name__ == '__main__':
    execute_from_argv()
