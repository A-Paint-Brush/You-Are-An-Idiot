import os.path as path
import sys


def fix_path(relative_path):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return path.normpath(path.join(getattr(sys, "_MEIPASS"), relative_path))
    else:
        return path.normpath(relative_path)
