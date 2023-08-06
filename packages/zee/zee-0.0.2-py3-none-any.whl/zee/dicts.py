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


from typing import Any


def update_dict_by_string(target: dict, path: str, value: Any = None):
    """Update a target dict by a path separated by dot

    Args:
        target (dict): target dict need to be updated
        path (str): a string with the form of 'a.b.c'
        value (Any, optional): value to be set to the target.
    """
    try:
        key, path = path.split('.', 1)  # ValueError
        if isinstance(target, dict):
            target = target[key]  # KeyError
        else:
            return print(f'{target} is not a dict!')
    except ValueError as e:
        # path is key
        pass
    except KeyError as e:
        # add new key
        target[key] = {}
        target = target[key]

    if path.count('.') > 0:
        update_dict_by_string(target, path, value)
    else:
        target[path] = value


def string_to_dict(path: str, value: Any = None):
    """Convert a string separated by dot to a dict

    Args:
        path (str): a string with the form of 'a.b.c'
    """
    d = {}
    *keys, last = path.split('.')
    output = d
    for key in keys:
        output = output.setdefault(key, {})
    output[last] = value
    return d


def merge_dict(target: dict, source: dict):
    """Merge source to target

    Args:
        target (dict): dict to be merged to
        source (dict): dict to be merged from

    Raises:
        KeyError: if key in target conflicts with source

    Yields:
        tuple: a tuple contains the key and value
    """
    for k in set(target.keys()) | set(source.keys()):
    # for k in sorted(set(target.keys()) | set(source.keys())):
        if k in target and k in source:
            if isinstance(target[k], dict) and isinstance(source[k], dict):
                yield (k, dict(merge_dict(target[k], source[k])))
            else:
                # yield (k, source[k])
                raise KeyError(f'Key {k} Conflicts!')
        elif k in target:
            yield (k, target[k])
        else:
            yield (k, source[k])


def query_dict_from_string(path: str, source: dict = {}):
    """get value from dict with path

    Args:
        path (str): a string with the form of a.b.c
        source (dict, optional): source to be queried. Defaults to {}.

    Raises:
        KeyError: if path not found

    Returns:
        _type_: value from path
    """
    keys = path.split('.')
    keys.reverse()
    while keys:
        key = keys.pop()
        try:
            source = source[key]
        except KeyError as e:
            raise KeyError(f'{path} not found!')
    
    return source
        # if not isinstance(source, dict):
        #     return source

        