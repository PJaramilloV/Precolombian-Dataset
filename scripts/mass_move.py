from argparse import ArgumentParser
from tqdm import tqdm
import shutil
import glob
import os

parser = ArgumentParser(description="Move files from one directory to another")
parser.add_argument("source",      help="Source directory")
parser.add_argument("destination",  help="Destination directory")
parser.add_argument("-p", "--pattern", type=str, default='', help="Pattern to match files to move")
parser.add_argument("-e", "--exclude", type=str, default='', help="Pattern to exclude files to move")
args = parser.parse_args()

src = args.source
dst = args.destination
ptn = args.pattern
exc = args.exclude

def get_files(src, ptn, exc):
    pattern = os.path.join(src, ptn)
    files = glob.glob(pattern)
    files = [f.replace('\\', '/') for f in files]
    if exc:
        exclude = os.path.join(src, exc)
        exclude_files = glob.glob(exclude)
        files = [f for f in files if f not in exclude_files]
    file_names = [f.replace(src, '').lstrip('/') for f in files]
    return files, file_names

def move_files(files, names, destination):
    for file, name in tqdm(zip(files, names), total=len(files)):
        shutil.move(file, os.path.join(destination, name))


if __name__ == '__main__':
    if not ptn:
        ptn = '*'

    src = src.replace('\\', '/').rstrip('/')
    dst = dst.replace('\\', '/').rstrip('/')
    ptn = ptn.replace('\\', '/').lstrip('/')
    exc = exc.replace('\\', '/').lstrip('/')

    files, names = get_files(src, ptn, exc)
    move_files(files, names, dst)


