import os
import upload
from base import make_output
import click


@click.command()
@click.option(
    '--path', '-p', default='.', show_default=True,
    help='Enter the path to the directory',
    type=click.Path(exists=True, dir_okay=True, readable=True)
)
@click.option(
    '--output', '-o', default=('csv', 'output.csv'), show_default=True,
    help="Output to file", type=(str, str)
)
def main(path, output):
    directory = os.path.abspath(path)
    out = make_output(directory)
    if output[0] == 'csv':
        upload.to_csv(out, output[1])
    elif output[0] == 'json':
        upload.to_json(out, output[1])
    elif output[0] == 'sqlite3':
        upload.to_sqlite3(out, output[1])
    print()


if __name__ == '__main__':
    main()
