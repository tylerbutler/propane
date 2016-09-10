# coding=utf-8
from __future__ import absolute_import, print_function

import errno
import filecmp
import logging

from path import Path
from propane.collections import wrap_list


__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def diff_dir(dir_cmp, left_path=True):
    """
    A generator that, given a ``filecmp.dircmp`` object, yields the paths to all files that are different. Works
    recursively.

    :param dir_cmp: A ``filecmp.dircmp`` object representing the comparison.
    :param left_path: If ``True``, paths will be relative to dircmp.left. Else paths will be relative to dircmp.right.
    """
    for name in dir_cmp.diff_files:
        if left_path:
            path_root = dir_cmp.left
        else:
            path_root = dir_cmp.right
        yield Path.joinpath(path_root, name)
    for sub in dir_cmp.subdirs.values():
        # Need to iterate over the recursive call to make sure the individual values are yielded up the stack
        for the_dir in diff_dir(sub, left_path):
            yield the_dir


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


def mirror_folder(source, target, delete_orphans=True, recurse=True, ignore_list=None, _level=0, logger=None):
    """Mirrors a folder *source* into a target folder *target*."""

    logger = logger or logging.getLogger(__name__)

    def expand_tree(p):
        tree = []
        for node in Path(p).walk():
            tree.append(node)
        return tree

    report = {
        'deleted': set([]),
        'overwritten': set([]),
        'new': set([])
    }
    d1 = source
    d2 = target
    logger.debug("Mirroring %s ==> %s" % (d1, d2))
    if not d2.exists():
        d2.makedirs()
    compare = filecmp.dircmp(d1, d2)

    # Expand the ignore list to be full paths
    if ignore_list is None:
        ignore_list = []
    else:
        ignore_list = [Path(d2 / i).normpath() for i in ignore_list]
        ignore_files = [f for f in ignore_list if f.isfile()]
        ignore_list.extend(expand_path(ignore_files, root_path=d2))

    # Delete orphan files/folders in the target folder
    if delete_orphans:
        for item in compare.right_only:
            fullpath = Path(d2 / item).normpath()
            if fullpath in ignore_list:
                logger.debug(
                    "%s ==> Ignored - path is in ignore list" % fullpath)
                continue

            if fullpath.isdir() and recurse:
                logger.debug(
                    "%s ==> Deleted - doesn't exist in source" % fullpath)
                report['deleted'].add(fullpath)
                if len(fullpath.listdir()) > 0:
                    report['deleted'].update(expand_tree(fullpath))

                # noinspection PyArgumentList
                fullpath.rmtree()
            elif fullpath.isfile():
                logger.debug(
                    "%s ==> Deleted - doesn't exist in source" % fullpath)
                report['deleted'].add(fullpath)
                fullpath.remove()

    # Copy new files and folders from the source to the target
    for item in compare.left_only:
        fullpath = d1 / item
        if fullpath.isdir() and recurse:
            logger.debug(
                "Copying new directory %s ==> %s" % (fullpath, (d2 / item)))
            fullpath.copytree(d2 / item)
            report['new'].add(d2 / item)
            report['new'].update(expand_tree(d2 / item))
        elif fullpath.isfile():
            logger.debug("Copying new file %s ==> %s" % (fullpath, (d2 / item)))
            fullpath.copy2(d2)
            report['new'].add(d2 / item)

    # Copy modified files in the source to the target, overwriting the target file
    for item in compare.diff_files:
        logger.debug(
            "Overwriting existing file %s ==> %s" % ((d1 / item), (d2 / item)))
        (d1 / item).copy2(d2)
        report['overwritten'].add(d2 / item)

    # Recurse into subfolders that exist in both the source and target
    if recurse:
        for item in compare.common_dirs:
            rpt = mirror_folder(d1 / item, d2 / item, delete_orphans, _level=_level + 1)
            report['new'].update(rpt['new'])
            report['overwritten'].update(rpt['overwritten'])
            report['deleted'].update(rpt['deleted'])
    return report
