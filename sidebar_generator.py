"""
Generates a _Sidebar.md that shows a tree of the wiki.
This is mostly useful for gitlab wiki (Gollum) based wikis.
"""

import argparse, os
import logging
from typing import List, Tuple

logging.basicConfig(level=logging.DEBUG)


def parse_args() -> Tuple[List[str], int, List[int], str]:
    """
    Parse external arguments
    :return: tuple of relevant args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs='+',
                        help='list of directories names to exclude. Includes all subdirectories. Defaults to config '
                             'file exclusions')
    parser.add_argument("--max-depth", help="maximum depth to build tree", default=3, type=int)
    parser.add_argument("--hide-files", action="store_true",
                        help="Only build the sidebar using directories, hiding files")
    parser.add_argument(help="wiki root directory", dest="wiki_root")
    args = parser.parse_args()

    # convert relative paths to absolute path
    root_dir = os.path.abspath(os.path.expanduser(args.wiki_root))

    # todo need to split out? or just return (modified) Namespace object from parse_args?
    return args.exclude, args.max_depth, args.hide_files, root_dir


def exclude_directories(dirs: List[str], excludes: List[str]) -> List[str]:
    """
    Exclude a set of directories from the original list
    :param dirs: list of directories
    :param excludes: list of directories to exclude
    :return: list with excluded directories
    """
    return [d for d in dirs if d not in excludes]


def get_directories(root: str) -> Tuple[Tuple[str, List[str], List[str]]]:
    """
    :return immutable list of 3 element tuples representing the directory, directory folders and directory files for each
    sub-directory within the root directory.
    :param root: directory where to start the recursive search from
    """

    # TODO this is quite imperative - how to do in a functional style?
    dirs = []
    for item in os.walk(root):
        dirs.append(item)

    return tuple(dirs)


def main():
    # get args
    excludes, max_depth, hide_files, root_dir = parse_args()

    # log information message for root dir
    logging.info(f"Creating sidebar starting from {root_dir}")

    # get directories
    dirs: tuple = get_directories(root_dir)

    # exclude directories that have an "excluded directory" in them
    dirs_filtered = list(filter(lambda x: not any(os.sep + _dir in x[0] for _dir in excludes), dirs))

    for i in dirs_filtered:
        print(i[0])

if __name__ == '__main__':
    main()