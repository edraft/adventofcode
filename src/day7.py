import json
from functools import reduce
from typing import Optional

from cpl_core.console import Console
from cpl_core.utils import String
from cpl_query.enumerable import Enumerable
from cpl_query.extension import List
from cpl_core.pipes import *

from aoc.aoc import get_input

# global vars
day = 7
aoc_input = get_input(2022, day)
aoc_input1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Dir:

    def __init__(self, name: str, parent: Optional['Dir'] = None):
        self._name = name
        self._parent = parent
        self._files = List(any)
        self._dirs = List(Dir)

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> 'Dir':
        return self._parent

    @property
    def files(self) -> List[str]:
        return self._files

    @property
    def dirs(self) -> List['Dir']:
        return self._dirs

    @property
    def size(self) -> int:
        total_size = 0

        for file, size in self._files:
            total_size += size

        for directory in self._dirs:
            total_size += directory.size

        return total_size

    @property
    def size_small_files(self) -> int:
        total_size = 0

        # for file, size in self._files:
        #     total_size += size

        file_size = self.size
        if file_size > 100000:
            file_size = 0

        total_size += file_size

        for directory in self._dirs:
            d_size = directory.size_small_files
            total_size += d_size

        return total_size

    def add_dir(self, dir: 'Dir'):
        self._dirs.append(dir)

    def add_file(self, name: str, size: int):
        self._files.append((name, size))


def main():
    root = Dir('/', None)
    pwd = root
    is_ls = True
    for line in aoc_input.splitlines():
        s_line = line.split()
        if line.startswith('$'):
            if s_line[1] == 'ls':
                is_ls = True
                continue

            if s_line[2] == '..':
                pwd = pwd.parent
            elif pwd.name != s_line[2]:
                Console.write_line(s_line[2], pwd.name, pwd.dirs.select(lambda x: x.name))
                pwd = pwd.dirs.where(lambda d: d.name == s_line[2]).single()

            continue

        p1 = s_line[0]
        p2 = s_line[1]
        if p1 == 'dir':
            Console.write_line(pwd.name, p2)
            pwd.add_dir(Dir(p2, pwd))
        else:
            pwd.add_file(p2, int(p1))

    # def get_dirs(pwd: Dir, dirs=None):
    #     if dirs is None:
    #         dirs = []
    #
    #     for d in pwd.dirs:
    #         dirs.append(d.name)
    #         get_dirs(d, dirs)
    #
    #     return dirs

    Console.write_line(root.size_small_files)


if __name__ == '__main__':
    Console.write_line(f'Advent of code day {day}')
    main()
    Console.write_line()
