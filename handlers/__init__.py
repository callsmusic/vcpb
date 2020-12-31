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
all_help = []

for i in a:
    handler = importlib.import_module("handlers." + i)
    all_handlers += handler.__handlers__
    try:
        all_help.append(handler.__help__)
    except:
        pass
