import sys
from .excel2json import excel2json


def main(wb_path, mode=None):
    excel2json(wb_path, mode)

if __name__ == "__main__":
    mode = None
    if len(sys.argv) > 2:
        mode = sys.argv[2]
    if len(sys.argv) > 1:
        wb_path = sys.argv[1]
        main(wb_path, mode)
    else:
        print("Please provide an Excel file as an argument")