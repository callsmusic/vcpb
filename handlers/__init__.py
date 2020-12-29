from os.path import dirname, basename, isfile, join
import glob
import importlib

modules = glob.glob(
    join(
        dirname(
            __file__
        ),
        "*.py"
    )
)
a = [
    basename(f)[:-3] for f in modules if isfile(f)
    and not f.endswith("__init__.py")
]

all_handlers = []

for i in a:
    all_handlers += importlib.import_module("handlers." + i).__handlers__