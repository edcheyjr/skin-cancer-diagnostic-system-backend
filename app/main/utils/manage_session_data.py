import os
from ..config import basedir


def create_session_file(filename, mode='w'):
    """create file"""
    filepath = os.path.join(basedir, filename)
    # check if the file
    arr = filename.split('.')
    if arr[1] == "txt":
        # if not os.path.exists(filepath):
        # os.mkdir(filepath)
        with open(filepath, mode) as fp:
            pass
            print("=======================")
            print("created file", filename)
            print("=======================")
    else:
        print("only txt extension accepted")


def write_on_session_file(filename, session_data, mode='a+'):
    """write on session file"""
    filepath = os.path.join(basedir, filename)
    if mode == 'a+' or mode == 'a':
        with open(filepath, mode) as f:
            f.write(session_data)
            f.close()
        print("=============session data===============")
        print("successfully add data", session_data)
        print("========================================")


def get_session_data(filename, mode='r'):
    """read from session file"""

    filepath = os.path.join(basedir, filename)
    if mode == 'r+' or mode == 'r':
        with open(filepath, mode) as f:
            lines = f.readlines()
    return lines


def truncate_session_file(filename, lineNumber, mode='r+'):
    """delete/truncate a line from session file"""
    filepath = os.path.join(basedir, filename)
    with open(filepath, mode)as f:
        f.truncate(lineNumber)
