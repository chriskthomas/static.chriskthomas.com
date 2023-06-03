#!/usr/bin/python3

# Utility script for saving and restore the modification times,
# owners and mode for all files in a tree.

import argparse
import json
import os
import sys

def collect_file_attrs(path):
    dirs = os.walk(path)
    file_attrs = {}
    for (dirpath, dirnames, filenames) in dirs:
        files = dirnames + filenames
        for file in files:
            path = os.path.join(dirpath, file)
            file_info = os.lstat(path)
            file_attrs[path] = {
                "mtime": file_info.st_mtime,
                "atime": file_info.st_atime,
            }
    return file_attrs


def apply_file_attrs(attrs):
    for path in sorted(attrs):
        attr = attrs[path]
        if os.path.lexists(path):
            atime = attr["atime"]
            mtime = attr["mtime"]

            current_file_info = os.lstat(path)
            mtime_changed = current_file_info.st_mtime != mtime

            if mtime_changed:
                print("Updating mtime for %s" % path, file=sys.stderr)
                os.utime(path, (atime, mtime))
        else:
            print("Skipping non-existent file %s" % path, file=sys.stderr)


def main():
    ATTR_FILE_NAME = ".saved-file-attrs"
    FOLDER_NAME = "www"

    parser = argparse.ArgumentParser(
        "Save and restore file attributes in a directory tree"
    )
    subparsers = parser.add_subparsers(dest="mode", help="Select the mode of operation")
    save_parser = subparsers.add_parser(
        "save", help="Save the attributes of files in the directory tree"
    )
    restore_parser = subparsers.add_parser(
        "restore", help="Restore saved file attributes"
    )
    args = parser.parse_args()

    if args.mode == "save":
        attr_file = open(ATTR_FILE_NAME, "w")
        attrs = collect_file_attrs(FOLDER_NAME)
        json.dump(attrs, attr_file, indent=2)
    elif args.mode == "restore":
        if not os.path.exists(ATTR_FILE_NAME):
            print(
                "Saved attributes file '%s' not found" % ATTR_FILE_NAME, file=sys.stderr
            )
            sys.exit(1)
        attr_file = open(ATTR_FILE_NAME, "r")
        attrs = json.load(attr_file)
        apply_file_attrs(attrs)


if __name__ == "__main__":
    main()
