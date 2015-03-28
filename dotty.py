#!/bin/python

# Copyright (C) 2015 Vibhav Pant <vibhavp@gmail.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import json
import os
import shutil
from sys import stderr
import argparse

def ask_user(prompt):
    valid = {"yes":True, 'y':True, "no":False, 'n':False}
    while True:
        print(prompt+" ",end="")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        elif choice == '':
            return True;
        else:
            print("Enter a correct choice.", file=stderr)

def create_directory(path):
    exp = os.path.expanduser(path)
    if (not os.path.isdir(exp)):
        print(exp+" doesnt exist, creating.")
        os.makedirs(exp)

def create_symlink(src, dest, replace):
    dest = os.path.expanduser(dest)
    src = os.path.abspath(src)
    if os.path.exists(dest):
        if not replace and ask_user(dest+" exists, delete it? [Y/n]"):
            if os.path.isfile(dest):
                os.remove(dest)
            else:
                shutil.rmtree(dest)
        else:
            return
    print("Linking %s -> %s" % (dest, src))
    os.symlink(src, dest)

def copy_path(src, dest):
    dest = os.path.expanduser(copy[src])
    src = os.path.abspath(src)
    if os.path.exists(dest):
        if ask_user(dest+ " exists, delete it? [Y/n]"):
            if os.path.isfile(dest):
                os.remove(dest)
            else:
                shutil.rmtree(dest)
        else:
            return
    print("Copying %s -> %s" % (src, dest))
    shutil.copy(src, dest)

def run_command(command):
    os.system(command)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="the JSON file you want to use")
    parser.add_argument("-r", "--replace", action="store_true",
                        help="replace files/folders if they already exist")
    args = parser.parse_args()
    js = json.load(open(args.config))
    os.chdir(os.path.expanduser(os.path.abspath(os.path.dirname(args.config))))

    directories  = js.get("directories")
    links = js.get("link")
    copy = js.get("copy")
    commands = js.get("commands")

    [create_directory(path) for path in directories if directories]

    [create_symlink(src, links[src], args.replace) for src in links if links]

    [copy_path(src, copy[src]) for src in copy if copy]

    [run_command(command) for command in commands if commands]

    print("Done!")

if __name__ == "__main__":
    main()
