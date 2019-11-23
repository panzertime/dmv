import argparse
from os import listdir, rename
from os.path import getsize
from subprocess import check_output, CalledProcessError

parser = argparse.ArgumentParser(description='Find duplicate files (by size, then hash)')
parser.add_argument('indir', metavar="input", type=str,
                    help='directory to scan for dupes')
parser.add_argument('outdir', metavar="output", type=str,
                    help='directory to put found dupes in')

args = parser.parse_args()

size_table = dict()

for filename in listdir(args.indir):
    size = getsize(args.indir + "/" + filename)
    row = size_table.get(size, [])
    row.append(filename)
    size_table[size] = row

for size, files in size_table.items():
    if len(files) > 1:
        hashes = list()
        for filename in files:
            try:
                output = check_output(["md5sum", 
                                        args.indir + "/" + filename])
                md5 = output.split()[0]
                if md5 in hashes:
                    print("DUPE FOUND!")
                    # move to dest folder
                    try:
                        print("in first try block")
                        rename(args.indir + "/" + filename, 
                                    args.outdir + "/" + filename)
                    except Error as e:
                        print(e)
                else:
                    hashes.append(md5)
            except CalledProcessError as e:
                print("some error doing the md5:")
                print(e.returncode)
                print(e.output)


# get list of all files in in-dir
# make hash map where key is size in B, val is list of files with that size
# then for each key in that map where size(val) > 1,
# hash each file, adding to a list, if we find a dupe move to out-dir
