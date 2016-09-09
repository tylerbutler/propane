# coding=utf-8
from __future__ import absolute_import, print_function

import errno

from path import Path
from propane.collections import wrap_list


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def ensure_exists(p, assume_dirs=False):
    """
    Ensures a given path *p* exists.

    If a path to a file is passed in, then the path to the file will be checked. This can be overridden by passing a
    value of ``True`` to ``assume_dirs``, in which case the paths will be assumed to be to directories, not files.
    """
    if Path(p).ext and not assume_dirs:
        Path(p).dirname().makedirs_p()
    else:
        Path(p).makedirs_p()
    return p


def expand_path(path_list, root_path=None):
    """
    Given a list of paths, returns a list of all parent paths (including the original paths).
    If provided, ``root_path`` is used as the outermost path when expanding parent paths. If path_list contains
    paths to files, only the directories where those files exist will be returned. This function only returns paths
    to directories.

    Example:

        expand_path(['/tmp/foo/bar', '/tmp/foo/baz/file.txt' '/tmp/bar'], root_path='/tmp')

    This call would return the following:

        ['/tmp/foo/bar/',
         '/tmp/foo',
         '/tmp/foo/baz/',
         '/tmp/bar/']

    If the ``root_path`` argument were ommitted in the above example,


    """
    to_return = set()
    path_list = wrap_list(path_list)

    # expand ignore list to include all directories as individual entries
    for p in path_list:
        p = Path(p)
        if p.isdir():
            to_return.add(p)
        head, tail = p.splitpath()
        while head and tail:
            if root_path is not None and head == root_path:
                break
            to_return.add(head)
            head, tail = head.splitpath()
    return list(to_return)


def has_files(the_path):
    """Given a path, returns whether the path has any files in it or any subfolders. Works recursively."""
    the_path = Path(the_path)
    try:
        for _ in the_path.walkfiles():
            return True
        return False
    except OSError as ex:
        if ex.errno == errno.ENOENT:
            # ignore
            return False
        else:
            raise
