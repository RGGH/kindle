#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+#
'''|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|'''
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+#
''' Converts ePUB to MOBI ready for your KINDLE'''
# This uses Calibre
# https://calibre-ebook.com
# You need to INSTALL CALIBRE for this code to work
# https://calibre-ebook.com/download
# Please support the project if you find it useful

# run this script with 'sudo python3 ep2kin.py'

from os import listdir, rename, makedirs
from os.path import isfile, join, exists
import subprocess
from tqdm import tqdm

# list of extensions that needs to be ignored.
ignored_extensions = ["pdf"]

# Set path to your Downloads Dir"
machine_path = "/home/rag/Downloads/"

print("Hello, just put the epubs to convert in the ebooks dir inside your 'Downloads' Dir")

# Check all Directories are present - if not, make them for user
# here all the downloaded files are kept
mypath = machine_path + "ebooks/"
print(f"Put books to convert HERE: {mypath}")
if not exists(mypath):
    print("Folder - 'ebooks' - does not exist, making it for you")
    print("put epubs here and run script again")
    makedirs(mypath)

# path where converted files are stored
mypath_converted = machine_path + "ebooks/kindle/"
print(f"Converted MOBI > {mypath_converted}")
if not exists(mypath_converted):
    print("Folder - 'ebooks/kindle' - does not exist, making it for you")
    makedirs(mypath_converted)

# path where processed files will be moved to, clearing the downloaded folder
mypath_processed = machine_path + "ebooks/processed/"
print(f"ePUB Archived to > {mypath_processed}")
if not exists(mypath_processed):
    print("Folder - 'ebooks/processed/' - does not exist, making it for you")
    makedirs(mypath_processed)
#
raw_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
converted_files =  [f for f in listdir(mypath_converted) if isfile(join(mypath_converted, f))]
#
# return file extension. pdf or epub or mobi
def get_file_extension(f):
    return f.split(".")[-1]
# return name of file to be kept after conversion.
# we are just changing the extension. azw3 here.
def get_final_filename(f):
    f = f.split(".")
    filename = ".".join(f[0:-1])
    #processed_file_name = filename+".azw3"
    processed_file_name = filename+".mobi"
    return processed_file_name
#
def convert_files():
    for f in tqdm(raw_files):
        final_file_name = get_final_filename(f)
        extension = get_file_extension(f)
        if final_file_name not in converted_files and extension not in ignored_extensions:
            print("Converting : "+f)
            try:
                subprocess.call(["ebook-convert",mypath+f,mypath_converted+final_file_name])
                s = rename(mypath+f, mypath_processed+f)
                print(s)
            except Exception as e:
                print(e)
        else:
            print("Already exists : "+final_file_name)

# Main Driver
if __name__ == "__main__":
    # convert any suitable files not already converted
    srcfiles = ([f for f in listdir(mypath) if isfile(join(mypath, f))])
    if srcfiles:
        convert_files()
    else:
        print("No files to convert")
