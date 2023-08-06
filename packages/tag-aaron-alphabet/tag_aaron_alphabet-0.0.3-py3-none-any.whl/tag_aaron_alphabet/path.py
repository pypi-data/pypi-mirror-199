import os as _os

def files(*inputs):
    for target in inputs:
        if _os.path.isfile(target):
            yield target
        elif _os.path.isdir(target):
            for root, dirs, filenames in _os.walk(target, topdown=False):
                for filename in filenames:
                    file = _os.path.join(root, filename)
                    yield file
        else:
            raise FileNotFoundError()
