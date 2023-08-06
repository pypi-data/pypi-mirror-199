#!/usr/bin/env python3

import json
import logging
import os
import pathlib
from pathlib import Path
import re


def is_identical(fpath_1: str, fpath_2: str) -> bool:
    file_contents = []
    for i, fpath in enumerate([fpath_1, fpath_2]):
        try:
            with open(fpath, "rb") as f:
                file_contents.append(f.read())
        except FileNotFoundError:
            print(f"Could not find file {fpath}")
        except UnicodeError:
            print(f"Unicode error while trying to read {fpath}")
        except Exception as e:
            print(f"Could not read file {fpath}: {e}")

    if len(file_contents) == 2:
        return file_contents[0] == file_contents[1]
    return False


def load_json(fpath: str) -> dict:
    with open(fpath, "r") as f:
        data = json.load(f)
    return data


def get_fpaths(fdir_root, recursive=True, file_exts: tuple[str] = None):
    if file_exts:
        file_exts = (e.lower() for e in file_exts)
        if recursive:
            fpaths = [str(path) for path in Path(fdir_root).rglob('*') if path.suffix.lower() in file_exts]
        else:
            fpaths = [os.path.join(fdir_root, fname) for fname in sorted(os.listdir(fdir_root)) if fname.endswith(file_exts)]
    else:  # No file exts
        if recursive:
            fpaths = [str(path) for path in Path(fdir_root).rglob('*')]
        else:
            fpaths = [os.path.join(fdir_root, fname) for fname in sorted(os.listdir(fdir_root))]
    return fpaths


def get_all_fpaths_by_extension(root_fdir: str, exts: tuple[str, ...], recursive=True) -> list[str]:
    """Kept for package backwards compatibility"""
    fpaths = get_fpaths(fdir_root=root_fdir, recursive=recursive, file_exts=exts)
    return sorted(fpaths)


def add_numbering_to_mp3splt_files(fdir):
    files: list[str] = sorted(os.listdir(fdir))
    timestamp_pattern = re.compile(r"_\d{3}m_\d\ds__\d{3}m_\d\ds(_\d\dh)?")
    for i, fname in enumerate(files):
        print(f"Processing {fname}.")
        file_timestamp = timestamp_pattern.search(string=fname).group()
        fname_new = f"{i + 1:02} - {fname.replace(file_timestamp, '')}"
        src = pathlib.Path(fdir, fname)
        dst = pathlib.Path(fdir, fname_new)
        src.rename(dst)  # No need to read/write as binary with "with open()" etc.


def get_fpaths_by_mod_date(fdir, recursive=False, file_exts: tuple[str] = None, old_to_new=True) -> list[str]:
    fpaths = get_fpaths(fdir_root=fdir, recursive=recursive, file_exts=file_exts)
    if old_to_new:
        fpaths_sorted = sorted(fpaths, key=lambda t: os.stat(t).st_mtime)
    else:
        fpaths_sorted = sorted(fpaths, key=lambda t: -os.stat(t).st_mtime)
    return fpaths_sorted


def number_files_by_mod_date(fdir, old_to_new=True, file_exts: tuple[str] = None, start_number=1, dry_run=False):
    fpaths = get_fpaths_by_mod_date(fdir=fdir, recursive=False, old_to_new=old_to_new, file_exts=file_exts)
    n_digits = len(str(len(fpaths)))
    logging.debug(f"{n_digits=}")
    for i, old_path in enumerate(fpaths):
        old_path = pathlib.Path(old_path)
        file_number = str(i + start_number).rjust(n_digits, "0")
        new_name = f"{file_number} - {old_path.name}"
        new_path = old_path.parent / new_name
        logging.info(f"Old path: {old_path}")
        logging.info(f"New path: {new_path}")
        if not dry_run:
            old_path.rename(new_path)



if __name__ == "__main__":
    # fpath_1 = "/media/findux/DATA/potholes/Potholes Dataset-20230123T145709Z-007b.zip"
    # fpath_2 = "/media/findux/DATA/potholes/Potholes Dataset-20230123T145709Z-007.zip"
    # # print(is_identical(fpath_1, fpath_2))
    # add_numbering_to_mp3splt_files("/home/findux/Desktop/DMI/test1/")

    loglvl = logging.DEBUG
    logmsg = "[ %(levelname)s ]\t%(funcName)s:  %(message)s"
    logging.basicConfig(level=loglvl, format=logmsg)

    fpath = "/media/findux/DATA/Videos/MySQL_Advanced_Topics/"
    number_files_by_mod_date(fdir=fpath)

