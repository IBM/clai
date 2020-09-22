#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=invalid-name
import io
import os
import platform


def is_windows():
    return platform.system() == "Windows"


def is_mac():
    return platform.system() == "Darwin"


def is_zos():
    return platform.system().lower() in ('zos', 'os390')


def is_rw_with_EBCDIC(file):
    # Assume that the file is read/writen with IBM-1047 on z/OS when
    #    not exist before creating  or
    #    not tagged / tagged with IBM-1047 and textflag off
    is_EBCDIC = False
    file_path_complete = os.path.expanduser(file)
    if is_zos():
        if not os.path.exists(file_path_complete):
            is_EBCDIC = True
        else:
            cmd = "chtag -p " + file_path_complete + " | cut -d ' ' -f 2,6 "
            pfile = os.popen(cmd, "r")
            output = pfile.read().strip()
            if output in ("untagged T=off", "IBM-1047 T=off"):
                is_EBCDIC = True
            pfile.close()
    return is_EBCDIC


def get_rc_file(system=False):
    if system:
        return "/etc/profile"
    return "~/.bashrc"


def get_rc_files(system=False):
    if system:
        return ["/etc/profile"]

    return ["~/.bash_profile", "~/.bashrc"]


def get_setup_file():
    return "~/.clairc"


def append_to_file(file_path, value_to_append, codeset="utf-8"):
    file_path_complete = os.path.expanduser(file_path)
    print("append to file %s" % file_path_complete)
    with open(os.path.expanduser(file_path_complete), "a+", encoding=codeset) as file:
        file.write(value_to_append)


def get_history_file_name():
    return os.environ.get("HISTFILE",
                          os.path.expanduser('~/.bash_history'))


def read_history():
    history_file_name = get_history_file_name()
    if os.path.isfile(history_file_name):
        return io.open(
            history_file_name, "r", encoding="utf-8", errors="ignore"
        ).readlines()
    return []
