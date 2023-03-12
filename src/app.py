import os
import sys
import upload
from base import make_output


def main():
    if len(sys.argv) > 1:
        directory = os.path.abspath(sys.argv[1])
    else:
        directory = os.path.abspath('.')

    out = make_output(directory)
    upload.to_json(out)
    upload.to_csv(out)
    upload.to_sqlite3(out)
    print()


if __name__ == '__main__':
    main()
