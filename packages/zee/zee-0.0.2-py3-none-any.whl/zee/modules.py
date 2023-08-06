# Copyright <2023> <YL Feng>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType


def load_module(modname: str, location: str = '', verbose: bool = True) -> ModuleType:
    """Load a module from a file location

    Args:
        modname (str): module file path relative to location like a/c/c.py
        location (str): root path of the module. If the module has relative
            imports like from . import, location must be specified!

    Returns:
        mudule
    """
    try:
        # from file location
        name = modname.removeprefix('./').removesuffix('.py').replace('/', '.')
        if not location:
            path = Path.cwd()/modname
        else:
            path = Path(location)/modname
        if verbose:
            print('loading', path)
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except (ModuleNotFoundError, AttributeError, ImportError) as e:
        # when module is relatively imported
        print('#############', e, f'import {name} failed')
        # package, name = name.rsplit('.', 1)
        module = import_module(name)
    return module

