from argparse import ArgumentParser
from . import path
from . import iterable
from .TaggedFile import TaggedFile


parser = ArgumentParser(
    fromfile_prefix_chars="@",
    allow_abbrev=False,
)
parser.add_argument('filter', nargs='?', default="")
parser.add_argument('-i', '--interactive', dest='i', action='store_true', default=False)
parser.add_argument('-v', '--verbose', dest='v', action='store_true', default=False)
parser.add_argument('-c', '--change', dest='c')
parser.add_argument('-x', '--exec', dest='x')
parser.add_argument('-I', '--inputs', dest='I', default=['.'], nargs='+')


def run(*, I, **kwargs):
    files = path.files(*I)
    files = iterable.unique_list(files)
    for file in files:
        if TaggedFile(file).go(**kwargs):
            break

        
def main():
    ns = parser.parse_args()
    run(**vars(ns))


if __name__ == '__main__':
    main()
