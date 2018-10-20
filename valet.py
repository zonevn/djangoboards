import argparse
import os
import pickle
import webbrowser

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'valet.prop'
prop = {}


def singleton(klaz):
    import functools
    inst = {}
    functools.wraps(klaz)

    def new_function(*arg, **kwargs):
        if klaz not in inst:
            inst[klaz] = klaz(*arg, **kwargs)
        return inst[klaz]

    return new_function


def parse(args):
    delimiter = '='
    arr = {}
    for elem in args:
        if delimiter in elem:
            key_val = elem.split(delimiter, 1)
            arr[key_val[0]] = key_val[1]
    return arr


# Load & Save Properties
def load_prop():
    global prop
    try:
        fopen = open(DATABASE, 'rb')
        prop = pickle.load(fopen)
        fopen.close()
    except:
        save_prop()


def save_prop():
    fopen = open(DATABASE, 'wb')
    pickle.dump(prop, fopen)
    fopen.close()


@singleton
class InputOption:
    def setup(self, args):
        if args is None:
            return
        self.__dict__.update(parse(args))


# Commands
def forget(args):
    global prop
    prop = {}
    save_prop()


def arrive():
    print(prop)


def test():
    prop['path'] = ROOT_DIR


def new():
    desc = "Usage: valet new -d name"
    option = InputOption()

    assert hasattr(option, 'name'), '\n'.join(['Output File not yet named.', desc])

    path = prop.get('path')

    f_name = getattr(option, 'name')

    f_name = '.'.join([f_name, 'py']) if '.' not in f_name else f_name
    f_path = os.path.join(path, f_name)

    if os.path.exists(f_path):
        print('{0} is already exist.'.format(f_name))
        return

    open(f_path, 'w').close()
    prop['path'] = path


def clone():
    desc = "Usage: valet clone -d from name"
    option = InputOption()

    assert hasattr(option, 'from'), '\n'.join(["Nothing to clone", desc])
    assert hasattr(option, 'name'), '\n'.join(["Output File not yet named.", desc])

    path = prop.get('path')

    origin = getattr(option, 'from')

    if not os.path.exists(os.path.join(path, origin)):
        raise Exception('Parent not found.')

    ins = open(os.path.join(path, origin), 'r')
    contents = ins.readlines()
    ins.close()

    target = getattr(option, 'name')
    outs = open(os.path.join(path, target), 'w')
    outs.writelines(contents)
    outs.close()


def listdir():
    desc = "Usage: valet listdir"
    path = prop.get('path')

    print(path)
    for dir in os.listdir(path):
        print(dir)


#  Main
def main():
    try:
        parser = argparse.ArgumentParser(prog='tutorial')
        parser.add_argument('command', help='Command helper',
                            choices=['forget', 'new', 'clone', 'listdir', 'arrive', 'test', ])
        parser.add_argument('-d', '--data', help='data helper', nargs='*', default=None)
        parser.add_argument('-at', '--path', default=None)
        args = parser.parse_args()
        method = args.command

        load_prop()

        path = prop.get('path') if args.path is None else os.path.join(ROOT_DIR, args.path)
        assert os.path.isdir(path), '"{}" not found.'.format(path)
        prop['path'] = path

        option = InputOption()
        option.setup(args.data)

        globals()[method]()

        save_prop()

    except Exception as e:
        print('Error: ', e)


if __name__ == '__main__':
    main()
