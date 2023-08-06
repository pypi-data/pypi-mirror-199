import sys
from .data_access import data_access

sys.path.append('download_repo')
from mycode import MyCode


def get_mycode_instance():
    return MyCode(data_access())
