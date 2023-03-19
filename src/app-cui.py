from base import make_output, straighten_dict
from cui.base import MainMenu
from cui.input_path import input_path
import os


def main():
    directory = os.path.abspath(input_path())
    out = make_output(directory)
    data = []
    parent_id = -1
    straighten_dict(out, data, parent_id)
    curr_menu = MainMenu(data)
    curr_menu.run()


if __name__ == '__main__':
    main()
